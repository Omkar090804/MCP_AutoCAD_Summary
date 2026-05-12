from __future__ import annotations

import logging
from typing import Any

from mcp.server.fastmcp import FastMCP

from autocad_service import (
    AutoCADSummaryError,
    generate_drawing_summary_payload,
    generate_drawing_summary_text,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

mcp = FastMCP("autocad-summary")


@mcp.tool()
def get_drawing_summary() -> str:
    """Return a readable summary of the currently opened AutoCAD drawing."""
    try:
        return generate_drawing_summary_text()
    except AutoCADSummaryError as exc:
        return f"AutoCAD summary error: {exc}"


@mcp.tool()
def get_drawing_summary_json() -> dict[str, Any]:
    """Return a structured summary of the currently opened AutoCAD drawing."""
    try:
        return {"ok": True, "summary": generate_drawing_summary_payload()}
    except AutoCADSummaryError as exc:
        return {"ok": False, "error": str(exc)}


@mcp.tool()
def health_check() -> dict[str, str]:
    """Return a lightweight readiness response for MCP client setup checks."""
    return {"status": "ok", "service": "autocad-summary"}


if __name__ == "__main__":
    mcp.run()
