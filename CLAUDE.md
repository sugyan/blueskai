# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BlueskAI is an AI agent that processes markdown instructions and generates responses through multiple personas. The system uses OpenAI's agents library with MCP (Model Context Protocol) servers to interact with external services like Bluesky social network.

## Architecture

The core system consists of:

- **Agent Processing**: Uses `openai-agents` library to create AI agents with specific personas
- **Profile System**: Multiple user profiles (`profiles/00.md`, `profiles/01.md`) that define different personas
- **MCP Integration**: Connects to external services via MCP servers:
  - `bsky-rmcp`: Bluesky social network integration (Rust binary in `bin/`)
  - `expertise`: Remote MCP server for domain expertise
- **Instruction Processing**: Takes markdown instruction files and processes them through the agent

## Key Components

### Settings (`blueskai/settings.py`)
- Configures multiple profiles with Bluesky credentials
- Each profile has specific MCP servers enabled
- Timezone configuration (Asia/Tokyo)
- Environment variables for credentials and MCP URLs

### Main Processing (`blueskai/main.py`)
- `process_instruction()`: Core function that creates agent and processes instructions
- Agent runs with o4-mini-2025-04-16 model
- Supports up to 20 turns of conversation
- Real-time streaming of agent responses

### Profile Management
- Profiles define personas with detailed background, personality, skills
- Located in `profiles/` directory as markdown files
- Used as agent instructions for consistent character behavior

## Development Commands

```bash
# Install dependencies
uv sync

# Install development dependencies
uv sync --dev

# Code quality
ruff check .
ruff format .

# Type checking
mypy .

# Run tests
uv run pytest

# Run the main application
python -m blueskai.main --profile 0 --instruction instructions/post.md
```

## Environment Setup

Required environment variables:
- `OPENAI_API_KEY`: OpenAI API access
- `BLUESKY_IDENTIFIER_0`, `BLUESKY_APP_PASSWORD_0`: Profile 0 Bluesky credentials
- `BLUESKY_IDENTIFIER_1`, `BLUESKY_APP_PASSWORD_1`: Profile 1 Bluesky credentials  
- `EXPERTISE_MCP_URL`: URL for the expertise MCP server

## Typical Workflow

1. Create/modify instruction files in `instructions/` directory
2. Select appropriate profile (0 or 1) based on desired persona
3. Run the agent with specific profile and instruction
4. Agent processes through MCP servers and generates responses
5. Monitor streaming output for tool calls and responses

## File Structure Notes

- `bin/`: Contains the `bsky-rmcp` binary for Bluesky integration
- `instructions/`: Markdown instruction templates (post.md, reply.md, profile.md)
- `profiles/`: Persona definitions as markdown files
- `scripts/`: Utility scripts like `update_schedule.py`