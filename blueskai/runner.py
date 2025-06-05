"""
Runner module for processing instructions with AI agents.

This module provides the Runner class that handles instruction processing
with configurable AI models and MCP servers.
"""

import logging
import zoneinfo
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

import agents
from agents import Agent, ItemHelpers
from agents.mcp import MCPServer

from .settings import settings

logger = logging.getLogger(__name__)


class Runner:
    """Process instructions using AI agents with configurable models."""

    def __init__(self, profile_path: Path, model: str):
        """Initialize Runner with specified profile and model.

        Args:
            profile_path: Path to the profile file.
            model: The OpenAI model to use for the agent.
        """
        self.profile_path = profile_path
        self.model = model

    async def process_instruction(
        self, mcp_servers: Iterable[MCPServer], instruction: str
    ) -> dict[str, Any]:
        """Process a single markdown instruction using an Agent.

        Args:
            mcp_servers: MCP servers to use with the agent.
            instruction: The markdown instruction to process.

        Returns:
            Dict containing the agent's response.
        """
        try:
            # Read profile from file
            with self.profile_path.open("r") as file:
                profile_content = file.read()

            # Create an agent
            agent = Agent(
                name="Blueskai Processor",
                instructions=f"""
                    You act entirely as the person indicated in the following profile:
                    {profile_content}
                """,
                model=self.model,
                mcp_servers=list(mcp_servers),
            )

            # Use agents.Runner to process the instruction
            logger.info(f"Processing instruction with agent using model: {self.model}")

            current_time = datetime.now(tz=zoneinfo.ZoneInfo(settings.tz))
            result = agents.Runner.run_streamed(
                agent,
                f"""
                    <!-- Current date and time: {current_time.strftime("%Y-%m-%d %H:%M:%S (%a)")} -->
                    {instruction}
                """,
                max_turns=20,
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
