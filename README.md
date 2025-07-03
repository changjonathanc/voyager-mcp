# Voyager-MCP

A Voyager-inspired MCP server that enables coding agents to build and immediately use CLI tools without restarting sessions.

## Features

- **MCP as CLI wrapper**: simply allows agent to execute CLI commands, so tools are instantly available.
- **Memory**: Tools with `.desc` files get descriptions loaded automatically in MCP tool schema in the next session.
- **Secure Execution**: Uses subprocess with argument lists to prevent shell injection.
- **Configurable**: Tool description can be configured from `~/.voyager/prompt.txt`

## Installation

The script includes embedded dependencies and can be run directly with uv:

```bash
claude mcp add voyager uv run
```

## MIT LICENSE

## Citation
```
@article{wang2023voyager,
  title   = {Voyager: An Open-Ended Embodied Agent with Large Language Models},
  author  = {Guanzhi Wang and Yuqi Xie and Yunfan Jiang and Ajay Mandlekar and Chaowei Xiao and Yuke Zhu and Linxi Fan and Anima Anandkumar},
  year    = {2023},
  journal = {arXiv preprint arXiv: Arxiv-2305.16291}
}
```
