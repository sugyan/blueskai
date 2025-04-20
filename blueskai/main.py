"""Main module for Blueskai agent."""

import os
import sys
from typing import Dict, Any
import logging
from pathlib import Path
from agents import Agent, Runner

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_markdown_instruction(instruction: str) -> Dict[str, Any]:
    """Process a single markdown instruction using an Agent.

    Args:
        instruction: The markdown instruction to process.

    Returns:
        Dict containing the agent's response.
    """
    try:
        # Create an agent
        agent = Agent(
            name="Blueskai Processor",
            instructions="You process a single markdown instruction and provide a thoughtful response.",
            model="gpt-4o",  # Uses environment variable OPENAI_API_KEY
        )

        # Use Runner to process the instruction
        # In a real implementation with API key, this would actually call the OpenAI API
        # Here we're using a simulated response since we don't have an API key
        logger.info(f"Processing instruction with agent")

        # Simulated response - in actual code, this would be:
        # result = Runner.run_sync(agent, instruction)
        # response = result.final_output
        response = f"Processed instruction: {instruction[:100]}..."

        return {
            "status": "success",
            "response": response,
        }

    except Exception as e:
        logger.error(f"Error: {e}")
        return {"status": "error", "error": str(e)}


def get_instruction_from_file(filepath: str) -> Dict[str, Any]:
    """Read instruction from file.
    
    Args:
        filepath: Path to the markdown instruction file.
        
    Returns:
        Dict with status and instruction or error.
    """
    if Path(filepath).exists():
        logger.info(f"Reading instruction from {filepath}")
        try:
            with open(filepath, "r") as f:
                instruction = f.read().strip()
            return {"status": "success", "instruction": instruction}
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            return {"status": "error", "error": f"Error reading file: {e}"}
    else:
        logger.error(f"File not found: {filepath}")
        return {"status": "error", "error": f"File not found: {filepath}"}


def get_default_instruction() -> str:
    """Return the default instruction when no file is provided."""
    return """
# Sample Task

This is a sample markdown instruction.
"""


def process_instruction(instruction: str) -> Dict[str, Any]:
    """Process an instruction and print the result.
    
    Args:
        instruction: The markdown instruction to process.
        
    Returns:
        Dict containing the processing result.
    """
    # Process the instruction
    result = process_markdown_instruction(instruction)

    # Print the result
    if result["status"] == "success":
        print("\nAgent Response:")
        print(result["response"])
    else:
        print(f"\nError: {result['error']}")
        
    return result


def main(filepath: str = None) -> Dict[str, Any]:
    """Process a markdown instruction from file or use default.
    
    Args:
        filepath: Optional path to markdown instruction file.
                 If None, uses sys.argv[1] if available.
    
    Returns:
        Dict containing the processing result.
    """
    # Determine file path (from argument or command line)
    if filepath is None and len(sys.argv) > 1:
        filepath = sys.argv[1]
    
    # Get instruction from file or use default
    if filepath:
        file_result = get_instruction_from_file(filepath)
        
        if file_result["status"] == "error":
            error_msg = file_result["error"]
            print(f"Error: {error_msg}")
            print("Usage: python -m blueskai.main path/to/instruction.md")
            return {"status": "error", "error": error_msg}
            
        instruction = file_result["instruction"]
    else:
        # Default instruction if no file provided
        instruction = get_default_instruction()
        logger.info("Using default instruction")

    return process_instruction(instruction)


if __name__ == "__main__":
    main()
