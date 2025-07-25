#!/usr/bin/env python3
# /// script
# dependencies = [
#   "mcp>=1.2.0",
# ]
# requires-python = ">=3.10"
# ///
"""
Voyager-MCP - A Voyager-inspired MCP server for local cli skill library

Enables coding agents to build and immediately use MCP tool without restarting a session or invalidating prompt cache
"""

import os
import subprocess
from pathlib import Path
from typing import List, Dict, Any

from mcp.server.fastmcp import FastMCP, Context

# Constants
EXECUTABLE_PERMISSION = 0o755
DEFAULT_TIMEOUT = 180
CONFIG_DIR_NAME = "voyager"
BIN_DIR_NAME = "bin"
SAMPLE_TOOL_NAME = "hello"

# Configuration using XDG Base Directory Specification
def get_config_dir() -> Path:
    """Get config directory using XDG Base Directory Specification"""
    xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
    if xdg_config_home:
        return Path(xdg_config_home) / CONFIG_DIR_NAME
    return Path.home() / ".config" / CONFIG_DIR_NAME

config_dir = get_config_dir()
bin_dir = config_dir / BIN_DIR_NAME

def get_default_prompt() -> str:
    """Get default prompt with actual directory path"""
    return f"""
Executes helper commands.
This tool supports all cli commands available on the system.

You can create new commands or modify existing tools in {bin_dir}
You can create tool.desc files to include short descriptions that will be loaded in the next session.
"""

def setup_directories() -> None:
    """Create necessary directories and update PATH"""
    config_dir.mkdir(parents=True, exist_ok=True)
    bin_dir.mkdir(exist_ok=True)

    # Add config bin directory to PATH if not already there
    bin_path_str = str(bin_dir)
    current_path = os.environ.get("PATH", "")
    if bin_path_str not in current_path:
        os.environ["PATH"] = f"{bin_path_str}:{current_path}"


def create_sample_tool() -> None:
    """Create sample tool and description file on first run"""
    sample_tool_path = bin_dir / SAMPLE_TOOL_NAME
    sample_desc_path = bin_dir / f"{SAMPLE_TOOL_NAME}.desc"

    if sample_tool_path.exists():
        return

    sample_tool_content = '''#!/usr/bin/env python3
"""
Sample hello tool - demonstrates how to create custom tools
"""
import sys

def main():
    if len(sys.argv) > 1:
        name = " ".join(sys.argv[1:])
        print(f"Hello, {name}!")
    else:
        print("Hello, World!")

    print("This is a sample tool created by Voyager-MCP.")
    print("You can create more tools in your config bin directory.")
    print("Add a .desc file with the same name to provide descriptions.")

if __name__ == "__main__":
    main()
'''

    # Write the sample tool
    sample_tool_path.write_text(sample_tool_content)
    sample_tool_path.chmod(EXECUTABLE_PERMISSION)

    # Create description file
    sample_desc_content = "Sample greeting tool - says hello and demonstrates custom tool creation"
    sample_desc_path.write_text(sample_desc_content)


def get_available_executables() -> List[Dict[str, str]]:
    """Get list of executable files in config bin directory with descriptions"""
    executables = []
    if not bin_dir.exists():
        return executables

    for file in bin_dir.iterdir():
        if not (file.is_file() and os.access(file, os.X_OK)):
            continue

        name = file.name
        desc_file = bin_dir / f"{name}.desc"
        description = ""

        if desc_file.exists():
            try:
                description = desc_file.read_text().strip()
            except Exception:
                description = ""

        executables.append({
            "name": name,
            "description": description
        })

    return sorted(executables, key=lambda x: x["name"])

def build_tool_description() -> str:
    """Build the complete tool description including available executables"""
    prompt_file = config_dir / "prompt.txt"

    if prompt_file.exists():
        base_description = prompt_file.read_text().strip()
    else:
        base_description = get_default_prompt().strip()
        prompt_file.write_text(base_description)

    executables = get_available_executables()
    if not executables:
        return f"{base_description}\n\nCurrently there are no executables found in {bin_dir}."

    tool_list = []
    for tool in executables:
        if tool["description"]:
            tool_list.append(f"{tool['name']}: {tool['description']}")
        else:
            tool_list.append(tool["name"])

    tools_section = "\n".join(f"- {tool}" for tool in tool_list)
    return f"{base_description}\n\nAvailable executables in {bin_dir}:\n{tools_section}"


def create_error_response(message: str) -> Dict[str, str]:
    """Create standardized error response"""
    return {"error": message}


def validate_command(command: List[str]) -> str:
    """Validate command arguments and return error message if invalid"""
    if not command or not isinstance(command, list):
        return "Command must be a non-empty list of strings"

    if not all(isinstance(arg, str) for arg in command):
        return "All command arguments must be strings"

    return ""


# Initialize server
setup_directories()
create_sample_tool()
tool_description = build_tool_description()

server = FastMCP("voyager-mcp")

@server.tool(
    description=tool_description
)
async def run_shell_command(
    command: List[str],
    timeout: int = DEFAULT_TIMEOUT,
    ctx: Context = None,
) -> Dict[str, Any]:
    """Execute shell command with list of arguments for better security

    Args:
        command: List of command arguments (e.g., ["ls", "-la", "/tmp"])
        timeout: Command timeout in seconds (default: 180 = 3 minutes)

    Returns:
        Dictionary containing stdout, stderr, and return_code
    """
    # Validate command
    error_message = validate_command(command)
    if error_message:
        if ctx:
            ctx.error(error_message)
        return create_error_response(error_message)

    try:
        # Execute command with list of arguments (no shell injection possible)
        # PATH includes config bin directory so executables there are available
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,  # Don't raise exception on non-zero exit
            env=os.environ.copy()  # Use updated environment with ~/.config/voyager/bin in PATH
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode,
            "command": command
        }
    except subprocess.TimeoutExpired:
        error_msg = f"Command execution timed out after {timeout} seconds"
        if ctx:
            ctx.error(error_msg)
        return create_error_response(error_msg)
    except Exception as e:
        error_msg = f"Command execution failed: {str(e)}"
        if ctx:
            ctx.error(error_msg)
        return create_error_response(error_msg)


def main():
    """Main entry point for the server"""
    server.run(transport='stdio')

if __name__ == "__main__":
    main()
