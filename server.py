from mcp.server.fastmcp import FastMCP
from autocad_service import generate_drawing_summary

mcp = FastMCP("autocad-summary")

@mcp.tool()
def get_drawing_summary() -> str:
    """
    Get summary of the currently opened AutoCAD drawing.

    Counts:
    - lines
    - circles
    - arcs
    - polylines
    - text objects

    Reads directly from the active AutoCAD DWG file.
    """

    return generate_drawing_summary()

if __name__ == "__main__":
    mcp.run()
