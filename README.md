# Voyager-MCP

A Voyager-inspired MCP server that enables coding agents to build and immediately use CLI tools without restarting sessions.

## Features

- **Single Tool**: The tool exposes a single tool `run_shell_command`.
- **Skill library**: Agents can add new commands in `~/.voyager/bin/`.
- **Dynamic schema**: The `run_shell_command` tool description can be configured from `~/.voyager/prompt.txt`, and it also dynamically loads available executables in `~/.voyager/bin/`.
- **Configurable**: Each executable can provide a `.desc` file, which will be included in the `run_shell_command` tool description.
- **Secure Execution**: Uses subprocess with argument lists to prevent shell injection.

## Installation

```bash
# add it to claude code
claude mcp add voyager uvx voyager-mcp

# try it with mcp inspector
npx -y @modelcontextprotocol/inspector uvx voyager-mcp
```

## LICENSE

MIT

## Citation
```
@article{wang2023voyager,
  title   = {Voyager: An Open-Ended Embodied Agent with Large Language Models},
  author  = {Guanzhi Wang and Yuqi Xie and Yunfan Jiang and Ajay Mandlekar and Chaowei Xiao and Yuke Zhu and Linxi Fan and Anima Anandkumar},
  year    = {2023},
  journal = {arXiv preprint arXiv: Arxiv-2305.16291}
}
```
