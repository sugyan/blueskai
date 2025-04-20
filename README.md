# Blueskai

AI agent that processes markdown instructions and generates thoughtful responses.

## Features

- Process single markdown instructions
- Autonomous thinking and response generation
- Simple command-line interface

## Getting Started

```bash
# Install dependencies
uv sync

# Run with default instruction
python -m blueskai.main

# Run with custom instruction file
python -m blueskai.main path/to/instruction.md
```

See [usage documentation](docs/usage.md) for detailed instructions.

## Development

```bash
# Install dev dependencies
uv add --dev ruff pytest

# Lint and format
ruff check .
ruff format .

# Run tests
pytest
```