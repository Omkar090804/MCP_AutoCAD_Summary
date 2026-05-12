# AutoCAD Drawing Summary MCP Server

This project is a simple MCP server that connects to AutoCAD and returns a summary of the currently opened drawing.

The server reads objects from the active AutoCAD DWG file and counts common drawing entities such as lines, circles, arcs, polylines, and text objects.

## Project Structure

```text
MCP_SUMMARY/
|-- autocad_service.py
|-- server.py
|-- requirements.txt
`-- claude_desktop_config.json
```

## What It Does

The MCP tool `get_drawing_summary` returns a text summary like:

```text
Drawing Summary

Lines: 10
Circles: 4
Arcs: 2
Polylines: 6
Text Objects: 3

Total Objects: 25
```

## Files

### `server.py`

Creates the MCP server using `FastMCP`.

It exposes one MCP tool:

```python
get_drawing_summary()
```

This tool calls the AutoCAD service and returns the drawing summary.

### `autocad_service.py`

Connects to AutoCAD using `pyautocad`.

It loops through objects in the active drawing and counts:

- Lines
- Circles
- Arcs
- Polylines
- Text and MText objects

If AutoCAD cannot be opened or accessed, it returns an AutoCAD connection error message.

### `requirements.txt`

Contains the required Python packages:

```text
mcp
pyautocad
pywin32
```

## Requirements

- Windows
- Python installed
- AutoCAD installed
- An AutoCAD drawing opened before running the tool

## Setup

Open PowerShell in the project folder:

```powershell
cd C:\Users\Dell\Desktop\MCP_SUMMARY
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Run the MCP Server

```powershell
python server.py
```

The server runs as an MCP server and waits for an MCP client to call its tool.

## Claude Desktop Configuration

Add this server to your Claude Desktop MCP configuration:

```json
{
  "mcpServers": {
    "autocad-summary": {
      "command": "python",
      "args": [
        "C:\\Users\\Dell\\Desktop\\MCP_SUMMARY\\server.py"
      ]
    }
  }
}
```

After updating the configuration, restart Claude Desktop.

## Usage

1. Open AutoCAD.
2. Open the DWG file you want to summarize.
3. Start or restart your MCP client.
4. Ask the client to use the `get_drawing_summary` tool.

## Notes

- The current code uses `Autocad(create_if_not_exists=True)`, so it can open AutoCAD if AutoCAD is not already running.
- The service waits 3 seconds before reading objects to give AutoCAD time to stabilize.
- Some unsupported or unreadable objects may be skipped.
