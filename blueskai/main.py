"""
Main module for Blueskai agent.

This module provides functionality to process markdown instructions
using an AI agent. It includes CLI support for reading instructions
from a file and processing them.
"""

import logging
from argparse import ArgumentParser
from pathlib import Path
from typing import Any

from agents import Agent, Runner

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_instruction(instruction: str) -> dict[str, Any]:
    """Process a single markdown instruction using an Agent.

    Args:
        instruction: The markdown instruction to process.

    Returns:
        Dict containing the agent's response.
    """
    try:
        # Create an agent
        # Uses environment variable OPENAI_API_KEY
        agent = Agent(
            name="Blueskai Processor",
            instructions="You process a single markdown instruction and provide a thoughtful response.",
            model="gpt-4.1-nano-2025-04-14",
        )

        # Use Runner to process the instruction
        logger.info("Processing instruction with agent")
        response = Runner.run_sync(agent, instruction).final_output

        return {"success": True, "response": response}
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"success": False, "error": str(e)}


def main(filepath: Path) -> None:
    """Process a markdown instruction from file or use default.

    Args:
        filepath: Path to markdown instruction file (required).

    Returns:
        Dict containing the processing result.
    """
    # Get instruction from file or use default
    with filepath.open("r") as file:
        instruction = file.read()

    print(process_instruction(instruction))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "filepath",
        type=Path,
        help="Path to the markdown instruction file (required).",
    )
    args = parser.parse_args()

    main(filepath=args.filepath)
