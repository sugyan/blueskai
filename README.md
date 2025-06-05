# BlueskAI

AI agent that processes markdown instructions and generates thoughtful responses.

## Features

- Process single markdown instructions
- Autonomous thinking and response generation
- Simple command-line interface

## Getting Started

```bash
# Install dependencies
uv sync

# Run with instruction file
python -m blueskai.main --profile 3 --instruction path/to/instruction.md
```

## Development

```bash
# Install dev dependencies
uv add --dev ruff pytest

# Lint and format
ruff check .
ruff format .

# Run tests
uv run pytest
```