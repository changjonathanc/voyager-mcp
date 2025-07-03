# manMCP

A secure MCP (Model Context Protocol) server for safe shell command execution.

## Features

- **Enhanced Security**: Commands must be provided as a list of strings, preventing shell injection
- **Configurable Description**: Tool description loaded from `~/.manMCP/prompt.txt`
- **Timeout Protection**: 30-second execution timeout
- **Structured Output**: Returns stdout, stderr, return code, and executed command

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Run the server:
```bash
python server.py
```

2. Configure your MCP client to connect to this server via stdio transport.

3. Use the `run_shell_command` tool with a list of command arguments:
```json
{
  "command": ["ls", "-la", "/tmp"]
}
```

## Configuration

The tool description is loaded from `~/.manMCP/prompt.txt`. This file is automatically created with a default description if it doesn't exist.

## Security Features

- Commands are executed using `subprocess.run()` with a list of arguments (no shell=True)
- Input validation ensures all arguments are strings
- 30-second timeout prevents hanging processes
- No shell interpretation or expansion

## Examples

Safe command execution:
- `["ls", "-la"]` - List files
- `["git", "status"]` - Check git status
- `["python", "--version"]` - Check Python version

The server will reject unsafe patterns and provide clear error messages.