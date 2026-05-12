# AutoCAD Drawing Summary MCP Server

## Summary

This project is a simple MCP server that connects to AutoCAD and generates a summary of the currently opened drawing.

It reads objects directly from the active AutoCAD DWG file and counts common drawing entities such as lines, circles, arcs, polylines, and text objects. The result is returned as a readable text summary through an MCP tool.

## Tools and Tech Stack Used

- Python
- MCP Python SDK
- FastMCP
- pyautocad
- pywin32
- AutoCAD
- Claude Desktop or any MCP-supported client
- Windows PowerShell

## Purpose

The purpose of this project is to allow an MCP client to interact with AutoCAD and quickly get a basic object summary of the active drawing.

Instead of manually checking drawing contents inside AutoCAD, the MCP tool can automatically count important object types and return the result in a simple format.

## Project Requirements

To run this project on a system, the system should have:

- Windows operating system
- Python installed
- AutoCAD installed
- AutoCAD accessible through Windows COM automation
- A DWG file opened in AutoCAD
- Internet connection for installing Python packages
- Claude Desktop or another MCP-compatible client

Python packages required:

```text
mcp
pyautocad
pywin32
```

## Project Files

```text
MCP_SUMMARY/
|-- autocad_service.py
|-- server.py
|-- requirements.txt
`-- claude_desktop_config.json
```

### `autocad_service.py`

This file contains the AutoCAD connection logic.

It uses `pyautocad` to connect to AutoCAD, reads the active drawing, loops through drawing objects, and counts:

- Lines
- Circles
- Arcs
- Polylines
- Text objects

### `server.py`

This file creates the MCP server using `FastMCP`.

It exposes one MCP tool:

```python
get_drawing_summary()
```

This tool calls the AutoCAD service and returns the drawing summary.

### `requirements.txt`

This file contains the dependencies needed to run the project.

## Setup

### Step 1: Install Python

Install Python from:

```text
https://www.python.org/downloads/
```

During installation, enable:

```text
Add Python to PATH
```

To verify Python is installed, open PowerShell and run:

```powershell
python --version
```

### Step 2: Install AutoCAD

Install AutoCAD on the Windows system.

Open AutoCAD once manually to make sure it starts correctly.

### Step 3: Open the Project Folder

Open PowerShell and move into the project folder:

```powershell
cd C:\Users\Dell\Desktop\MCP_SUMMARY
```

### Step 4: Install Python Dependencies

Run:

```powershell
pip install -r requirements.txt
```

This installs:

- `mcp`
- `pyautocad`
- `pywin32`

### Step 5: Open a Drawing in AutoCAD

Before using the MCP tool:

1. Open AutoCAD.
2. Open the DWG file that you want to summarize.
3. Keep AutoCAD running.

### Step 6: Run the MCP Server

From the project folder, run:

```powershell
python server.py
```

The server starts and waits for an MCP client to call the tool.

### Step 7: Configure Claude Desktop

Open your Claude Desktop configuration file and add this MCP server:

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

After saving the configuration, restart Claude Desktop.

## Detailed Working Steps

1. The MCP client starts the server using `server.py`.
2. `server.py` creates an MCP server named `autocad-summary`.
3. The MCP server exposes the tool `get_drawing_summary`.
4. When the tool is called, it runs the function `generate_drawing_summary`.
5. `generate_drawing_summary` connects to AutoCAD using `pyautocad`.
6. The code waits for 3 seconds so AutoCAD can stabilize.
7. It loops through all objects in the active drawing.
8. For each object, it checks the AutoCAD object name.
9. It increases the count for matching object types.
10. It creates a final text summary.
11. The summary is returned to the MCP client.

## Usage

After setup is complete:

1. Open AutoCAD.
2. Open your DWG drawing.
3. Start Claude Desktop or another MCP client.
4. Ask the client to get the drawing summary.
5. The MCP tool returns a result similar to:

```text
Drawing Summary

Lines: 12
Circles: 5
Arcs: 3
Polylines: 8
Text Objects: 4

Total Objects: 32
```

This output gives a quick overview of the main object types present in the active AutoCAD drawing.
