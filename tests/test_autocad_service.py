from __future__ import annotations

import pytest

from autocad_service import AutoCADSettings, AutoCADSummaryError, generate_drawing_summary


class FakeObject:
    def __init__(self, object_name: str) -> None:
        self.ObjectName = object_name


class BrokenObject:
    @property
    def ObjectName(self) -> str:
        raise RuntimeError("COM object is unavailable")


class FakeDocument:
    Name = "sample.dwg"


class FakeAutoCAD:
    doc = FakeDocument()

    def __init__(self, objects: list[object]) -> None:
        self._objects = objects

    def iter_objects(self) -> list[object]:
        return self._objects


def test_generate_drawing_summary_counts_supported_and_other_objects() -> None:
    objects = [
        FakeObject("AcDbLine"),
        FakeObject("AcDbCircle"),
        FakeObject("AcDbArc"),
        FakeObject("AcDbPolyline"),
        FakeObject("AcDb2dPolyline"),
        FakeObject("AcDbText"),
        FakeObject("AcDbMText"),
        FakeObject("AcDbBlockReference"),
        BrokenObject(),
    ]

    summary = generate_drawing_summary(
        settings=AutoCADSettings(startup_delay_seconds=0),
        autocad_factory=lambda **_: FakeAutoCAD(objects),
    )

    assert summary.to_dict() == {
        "lines": 1,
        "circles": 1,
        "arcs": 1,
        "polylines": 2,
        "text_objects": 2,
        "skipped_objects": 1,
        "unsupported_objects": {"AcDbBlockReference": 1},
        "drawing_name": "sample.dwg",
        "counted_objects": 7,
        "total_seen_objects": 9,
    }


def test_generate_drawing_summary_wraps_connection_errors() -> None:
    def fail_to_connect(**_: object) -> object:
        raise RuntimeError("AutoCAD is not running")

    with pytest.raises(AutoCADSummaryError, match="Could not connect to AutoCAD"):
        generate_drawing_summary(
            settings=AutoCADSettings(startup_delay_seconds=0),
            autocad_factory=fail_to_connect,
        )
