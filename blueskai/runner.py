"""
Runner module for processing instructions with AI agents.

This module provides the Runner class that handles instruction processing
with configurable AI models and MCP servers.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

import agents
from agents import Agent, ItemHelpers
from agents.mcp import MCPServer


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

    def prepare_agent(self, mcp_servers: Iterable[MCPServer]) -> Agent:
        """Prepare the agent with profile and configuration.

        Args:
            mcp_servers: MCP servers to use with the agent.

        Returns:
            Configured Agent instance.
        """
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
        return agent

    def prepare_instruction(self, instruction_path: Path) -> str:
        """Prepare instruction with current time context.

        Args:
            instruction_path: Path to the instruction file.

        Returns:
            Formatted instruction string with timestamp.
        """
        # Read instruction from file
        with instruction_path.open("r") as file:
            instruction_content = file.read()

        # Add current time context
        current_time = datetime.now()
        return f"""
            <!-- Current date and time: {current_time.strftime("%Y-%m-%d %H:%M:%S (%a)")} -->
            {instruction_content}
        """

    async def run_agent(self, agent: Agent, instruction: str) -> dict[str, Any]:
        """Execute the agent with the prepared instruction.

        Args:
            agent: Configured Agent instance.
            instruction: Formatted instruction string.

        Returns:
            Dict containing the agent's response.
        """
        try:
            logger.info(f"Processing instruction with agent using model: {self.model}")

            result = agents.Runner.run_streamed(
                agent,
                instruction,
                max_turns=20,
            )
            async for event in result.stream_events():
                # We'll ignore the raw responses event deltas
                if event.type == "raw_response_event":
                    continue
                # When the agent updates, log that
                elif event.type == "agent_updated_stream_event":
                    logger.info(f"Agent updated: {event.new_agent.name}")
                    continue
                # When items are generated, log them
                elif event.type == "run_item_stream_event":
                    if event.item.type == "tool_call_item":
                        logger.info("-- Tool was called")
                    elif event.item.type == "tool_call_output_item":
                        logger.info(f"-- Tool output: {event.item.output}")
                    elif event.item.type == "message_output_item":
                        logger.info(
                            f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}"
                        )
                    else:
                        pass  # Ignore other event types

            return {"success": True}
        except Exception as e:
            logger.exception("Error processing instruction")
            return {"success": False, "error": str(e)}

    async def process_instruction(
        self, mcp_servers: Iterable[MCPServer], instruction_path: Path
    ) -> dict[str, Any]:
        """Process a markdown instruction file using an Agent.

        Args:
            mcp_servers: MCP servers to use with the agent.
            instruction_path: Path to the instruction file.

        Returns:
            Dict containing the agent's response.
        """
        try:
            agent = self.prepare_agent(mcp_servers)
            instruction = self.prepare_instruction(instruction_path)
            return await self.run_agent(agent, instruction)
        except Exception as e:
            logger.exception("Error processing instruction")
            return {"success": False, "error": str(e)}
