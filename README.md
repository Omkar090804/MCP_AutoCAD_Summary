# AutoCAD Summary MCP Server

Production-ready MCP server that reads the active AutoCAD drawing and returns a concise object summary for MCP clients such as Claude Desktop.

## Features

- Counts lines, circles, arcs, polylines, and text objects from the active DWG.
- Exposes both human-readable and structured JSON MCP tools.
- Reports unsupported and skipped objects instead of silently hiding them.
- Avoids launching AutoCAD by default, so production clients do not unexpectedly start desktop software.
- Includes typed service code, focused tests, lint configuration, and a Claude Desktop config example.

## Tools

| Tool | Output | Use case |
| --- | --- | --- |
| `get_drawing_summary` | Text | Quick readable drawing report |
| `get_drawing_summary_json` | JSON | Automation, dashboards, and downstream processing |
| `health_check` | JSON | Client setup and readiness checks |

## Requirements

- Windows
- Python 3.11 or newer
- AutoCAD installed and available through COM automation
- An open AutoCAD drawing before calling the summary tools

## Setup

```powershell
cd C:\Users\Dell\Desktop\MCP_SUMMARY
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

For development:

```powershell
python -m pip install -r requirements-dev.txt
```

## Run Locally

```powershell
python server.py
```

The server uses stdio transport through `FastMCP`, which is the transport expected by desktop MCP clients.

## Claude Desktop Configuration

Use `claude_desktop_config.example.json` as the template for your Claude Desktop MCP config. Update the Python path if you use a virtual environment:

```json
{
  "mcpServers": {
    "autocad-summary": {
      "command": "C:\\Users\\Dell\\Desktop\\MCP_SUMMARY\\.venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\Dell\\Desktop\\MCP_SUMMARY\\server.py"],
      "env": {
        "AUTOCAD_CREATE_IF_NOT_EXISTS": "false",
        "AUTOCAD_STARTUP_DELAY_SECONDS": "0.5"
      }
    }
  }
}
```

## Configuration

| Environment variable | Default | Description |
| --- | --- | --- |
| `AUTOCAD_CREATE_IF_NOT_EXISTS` | `false` | Set to `true` if the server may launch AutoCAD when it is not already running. |
| `AUTOCAD_STARTUP_DELAY_SECONDS` | `0.5` | Delay after connecting to AutoCAD before reading objects. |

## Testing

Tests mock the AutoCAD COM object, so they can run without AutoCAD.

```powershell
pytest
ruff check .
```

## Production Notes

- Run this server only on a trusted Windows workstation because it automates local desktop software.
- Keep AutoCAD open with the target drawing loaded before invoking the tools.
- Prefer `get_drawing_summary_json` when another agent or process needs reliable fields.
- Keep generated reports, logs, and local environment files out of version control.
