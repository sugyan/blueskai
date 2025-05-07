"""
Main module for Blueskai agent.

This module provides functionality to process markdown instructions
using an AI agent. It includes CLI support for reading instructions
from a file and processing them.
"""

import asyncio
import logging
import zoneinfo
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path
from typing import Any

from agents import Agent, ItemHelpers, Runner
from agents.mcp import MCPServer, MCPServerStdio

from .settings import Profile, settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def process_instruction(
    mcp_server: MCPServer, profile: str, instruction: str
) -> dict[str, Any]:
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
            instructions=f"""
                You act entirely as the person indicated in the following profile:
                {profile}
            """,
            # model="gpt-4.1-nano-2025-04-14",
            # model="gpt-4.1-mini-2025-04-14",
            model="o4-mini-2025-04-16",
            mcp_servers=[mcp_server],
        )

        # Use Runner to process the instruction
        logger.info("Processing instruction with agent")

        current_time = datetime.now(tz=zoneinfo.ZoneInfo("Asia/Tokyo"))
        result = Runner.run_streamed(
            agent,
            f"""
                <!-- Current date and time: {current_time.strftime("%Y-%m-%d %H:%M:%S (%a)")} -->
                {instruction}
            """,
        )
        async for event in result.stream_events():
            # We'll ignore the raw responses event deltas
            if event.type == "raw_response_event":
                continue
            # When the agent updates, print that
            elif event.type == "agent_updated_stream_event":
                print(f"Agent updated: {event.new_agent.name}")
                continue
            # When items are generated, print them
            elif event.type == "run_item_stream_event":
                if event.item.type == "tool_call_item":
                    print("-- Tool was called")
                elif event.item.type == "tool_call_output_item":
                    print(f"-- Tool output: {event.item.output}")
                elif event.item.type == "message_output_item":
                    print(
                        f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}"
                    )
                else:
                    pass  # Ignore other event types

        return {"success": True}
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"success": False, "error": str(e)}


async def main(profile: Profile, instruction: Path) -> None:
    """Process a markdown instruction from file or use default.

    Args:
        profile: Index of the profile to use.
        instruction: Path to markdown instruction file.

    Returns:
        None. Prints the processing result.
    """
    # Get profile from file
    with profile.file.open("r") as file:
        profile_content = file.read()

    # Get instruction from file or use default
    with instruction.open("r") as file:
        instruction_content = file.read()

    async with MCPServerStdio(
        name="bsky",
        params={
            "command": str(
                (Path(__file__).parent.parent / "bin" / "bsky-rmcp").resolve()
            ),
            "env": {
                "BLUESKY_IDENTIFIER": profile.bsky_identifier,
                "BLUESKY_APP_PASSWORD": profile.bsky_app_password,
                "RUST_LOG": "info",
            },
        },
    ) as server:
        result = await process_instruction(server, profile_content, instruction_content)
    if result["success"]:
        logger.info("Instruction processed successfully.")
    else:
        logger.error(f"Error: {result['error']}")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--profile",
        type=int,
        required=True,
        help="Index of the profile to use.",
    )
    parser.add_argument(
        "--instruction",
        type=Path,
        required=True,
        help="Path to the markdown instruction file.",
    )
    args = parser.parse_args()

    profile = settings.profiles[args.profile]
    print(profile)
    asyncio.run(main(profile=profile, instruction=args.instruction))
