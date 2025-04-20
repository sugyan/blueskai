# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
- AI Agent using some MCP servers
- Agent processes a single instruction from a markdown prompt
- Agent thinks autonomously and outputs results

## Build/Test Commands
- Install dependencies: `uv sync`
- Install dev dependencies: `uv add --dev ruff pytest`
- Lint: `ruff check .`
- Format: `ruff format .`
- Test all: `pytest`
- Test single file: `pytest path/to/test_file.py::test_function`
- Run: `python -m blueskai.main`
- Run with instruction file: `python -m blueskai.main path/to/instruction.md`

## Code Style Guidelines
- Python with modern project structure
- Use uv for package management
- Use ruff for linting and formatting
- Explicit type hints throughout
- Environment variables for keys and configurations
- Clear error handling and logging
- Follow PEP 8 naming conventions
- Document functions with docstrings