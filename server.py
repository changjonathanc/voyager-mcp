#!/usr/bin/env python3
"""
manMCP - A secure MCP server for shell command execution
"""

import os
import subprocess
from pathlib import Path
from typing import List, Dict, Any

from mcp.server.fastmcp import FastMCP, Context

# Create ~/.manMCP directory
config_dir = Path.home() / ".manMCP"
config_dir.mkdir(exist_ok=True)

# Load tool description from prompt.txt
prompt_file = config_dir / "prompt.txt"
if prompt_file.exists():
    tool_description = prompt_file.read_text().strip()
else:
    tool_description = "Execute shell commands safely with enhanced security"
    # Create default prompt.txt
    prompt_file.write_text(tool_description)

mcp = FastMCP("manMCP")

@mcp.tool(
    title="Shell Command Executor",
    description=tool_description
)
async def run_shell_command(
    command: List[str],
    ctx: Context
) -> Dict[str, Any]:
    """Execute shell command with list of arguments for better security
    
    Args:
        command: List of command arguments (e.g., ["ls", "-la", "/tmp"])
    
    Returns:
        Dictionary containing stdout, stderr, and return_code
    """
    if not command or not isinstance(command, list):
        ctx.error("Command must be a non-empty list of strings")
        return {"error": "Command must be a non-empty list of strings"}
    
    # Validate all arguments are strings
    if not all(isinstance(arg, str) for arg in command):
        ctx.error("All command arguments must be strings")
        return {"error": "All command arguments must be strings"}
    
    try:
        # Execute command with list of arguments (no shell injection possible)
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30,  # 30 second timeout
            check=False  # Don't raise exception on non-zero exit
        )
        
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode,
            "command": command
        }
    except subprocess.TimeoutExpired:
        ctx.error("Command execution timed out after 30 seconds")
        return {"error": "Command execution timed out after 30 seconds"}
    except Exception as e:
        ctx.error(f"Command execution failed: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run(transport='stdio')