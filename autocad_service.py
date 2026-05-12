from __future__ import annotations

import logging
import os
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Callable, Iterable

from pyautocad import Autocad

LOGGER = logging.getLogger(__name__)

POLYLINE_OBJECTS = frozenset({"AcDbPolyline", "AcDb2dPolyline", "AcDb3dPolyline"})
TEXT_OBJECTS = frozenset({"AcDbText", "AcDbMText"})


class AutoCADSummaryError(RuntimeError):
    """Raised when a drawing summary cannot be generated."""


@dataclass(frozen=True)
class AutoCADSettings:
    create_if_not_exists: bool = False
    startup_delay_seconds: float = 0.5

    @classmethod
    def from_env(cls) -> "AutoCADSettings":
        return cls(
            create_if_not_exists=_read_bool("AUTOCAD_CREATE_IF_NOT_EXISTS", False),
            startup_delay_seconds=_read_float("AUTOCAD_STARTUP_DELAY_SECONDS", 0.5),
        )


@dataclass
class DrawingSummary:
    lines: int = 0
    circles: int = 0
    arcs: int = 0
    polylines: int = 0
    text_objects: int = 0
    skipped_objects: int = 0
    unsupported_objects: dict[str, int] = field(default_factory=dict)
    drawing_name: str | None = None

    @property
    def counted_objects(self) -> int:
        return self.lines + self.circles + self.arcs + self.polylines + self.text_objects

    @property
    def total_seen_objects(self) -> int:
        return self.counted_objects + self.skipped_objects + sum(self.unsupported_objects.values())

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["counted_objects"] = self.counted_objects
        data["total_seen_objects"] = self.total_seen_objects
        return data

    def to_text(self) -> str:
        drawing = self.drawing_name or "Active AutoCAD drawing"
        lines = [
            "Drawing Summary",
            "",
            f"Drawing: {drawing}",
            f"Lines: {self.lines}",
            f"Circles: {self.circles}",
            f"Arcs: {self.arcs}",
            f"Polylines: {self.polylines}",
            f"Text Objects: {self.text_objects}",
            "",
            f"Counted Objects: {self.counted_objects}",
            f"Skipped Objects: {self.skipped_objects}",
            f"Total Seen Objects: {self.total_seen_objects}",
        ]

        if self.unsupported_objects:
            lines.extend(["", "Other Object Types:"])
            lines.extend(
                f"- {name}: {count}"
                for name, count in sorted(self.unsupported_objects.items())
            )

        return "\n".join(lines)


def generate_drawing_summary(
    settings: AutoCADSettings | None = None,
    autocad_factory: Callable[..., Any] = Autocad,
) -> DrawingSummary:
    settings = settings or AutoCADSettings.from_env()

    try:
        acad = autocad_factory(create_if_not_exists=settings.create_if_not_exists)
    except Exception as exc:
        raise AutoCADSummaryError(
            "Could not connect to AutoCAD. Open AutoCAD with a drawing loaded, "
            "or set AUTOCAD_CREATE_IF_NOT_EXISTS=true to allow startup."
        ) from exc

    if settings.startup_delay_seconds > 0:
        time.sleep(settings.startup_delay_seconds)

    summary = DrawingSummary(drawing_name=_active_document_name(acad))

    try:
        objects = acad.iter_objects()
    except Exception as exc:
        raise AutoCADSummaryError("Could not read objects from the active AutoCAD drawing.") from exc

    _count_objects(objects, summary)
    return summary


def generate_drawing_summary_text() -> str:
    return generate_drawing_summary().to_text()


def generate_drawing_summary_payload() -> dict[str, Any]:
    return generate_drawing_summary().to_dict()


def _count_objects(objects: Iterable[Any], summary: DrawingSummary) -> None:
    for obj in objects:
        try:
            name = obj.ObjectName
        except Exception:
            summary.skipped_objects += 1
            LOGGER.debug("Skipped AutoCAD object because ObjectName was unavailable.", exc_info=True)
            continue

        if name == "AcDbLine":
            summary.lines += 1
        elif name == "AcDbCircle":
            summary.circles += 1
        elif name == "AcDbArc":
            summary.arcs += 1
        elif name in POLYLINE_OBJECTS:
            summary.polylines += 1
        elif name in TEXT_OBJECTS:
            summary.text_objects += 1
        else:
            summary.unsupported_objects[name] = summary.unsupported_objects.get(name, 0) + 1


def _active_document_name(acad: Any) -> str | None:
    try:
        return str(acad.doc.Name)
    except Exception:
        LOGGER.debug("Active AutoCAD document name was unavailable.", exc_info=True)
        return None


def _read_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _read_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        LOGGER.warning("Invalid float value for %s=%r; using %s.", name, value, default)
        return default
