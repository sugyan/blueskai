"""
Main module for Blueskai agent.

This module provides functionality to process markdown instructions
using an AI agent. It includes CLI support for reading instructions
from a file and processing them.
"""

import asyncio
import logging
from argparse import ArgumentParser
from pathlib import Path

from agents.mcp import MCPServerStdio

from .runner import Runner
from .settings import Profile, settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main(profile: Profile, instruction: Path, model: str) -> None:
    """Process a markdown instruction from file.

    Args:
        profile: Profile to use.
        instruction: Path to markdown instruction file.
        model: OpenAI model to use for the agent.

    Returns:
        None. Prints the processing result.
    """
    # Create runner with specified profile and model
    runner = Runner(profile_path=profile.file, model=model)

    async with (
        MCPServerStdio(
            name="bsky",
            params={
                "command": str(
                    (Path(__file__).parent.parent / "bin" / "bsky-rmcp").resolve()
                ),
                "env": {
                    "BLUESKY_IDENTIFIER": profile.bsky_identifier,
                    "BLUESKY_APP_PASSWORD": profile.bsky_app_password,
                    "TZ": settings.tz,
                    "RUST_LOG": "info",
                },
            },
        ) as bsky_rmcp,
        MCPServerStdio(
            name="expertise",
            params={
                "command": "npx",
                "args": [
                    "-y",
                    "mcp-remote",
                    settings.expertise_mcp_url,
                ],
            },
            client_session_timeout_seconds=15,
        ) as expertise,
    ):
        result = await runner.process_instruction(
            mcp_servers=filter(
                lambda x: x.name in profile.mcp_servers,
                [bsky_rmcp, expertise],
            ),
            instruction_path=instruction,
        )
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
    parser.add_argument(
        "--model",
        type=str,
        choices=[
            "gpt-4.1-nano-2025-04-14",
            "gpt-4.1-mini-2025-04-14",
            "o4-mini-2025-04-16",
        ],
        default="o4-mini-2025-04-16",
        help="OpenAI model to use (default: o4-mini-2025-04-16).",
    )
    args = parser.parse_args()

    profile = settings.profiles[args.profile]
    print(f"Profile: {profile.file.name}")
    print(f"Model: {args.model}")
    asyncio.run(main(profile=profile, instruction=args.instruction, model=args.model))
