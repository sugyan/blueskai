"""Tests for the Runner module."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from blueskai.runner import Runner


class TestRunner:
    """Test cases for Runner class."""

    def test_init(self):
        """Test Runner initialization."""
        profile_path = Path("profile.md")
        model = "gpt-4.1-mini-2025-04-14"
        runner = Runner(profile_path=profile_path, model=model)

        assert runner.profile_path == profile_path
        assert runner.model == model

    def test_prepare_agent(self):
        """Test agent preparation with profile loading."""
        # Create temporary profile file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Test Profile\nThis is a test profile.")
            profile_path = Path(f.name)

        try:
            runner = Runner(profile_path=profile_path, model="gpt-4.1-mini-2025-04-14")

            # Mock MCP servers
            mcp_servers = []

            with patch("blueskai.runner.Agent") as mock_agent:
                agent = runner.prepare_agent(mcp_servers)

                # Verify Agent was called with correct parameters
                mock_agent.assert_called_once_with(
                    name="Blueskai Processor",
                    instructions="""
                You act entirely as the person indicated in the following profile:
                # Test Profile
This is a test profile.
            """,
                    model="gpt-4.1-mini-2025-04-14",
                    mcp_servers=[],
                )

                assert agent == mock_agent.return_value
        finally:
            # Clean up temporary file
            profile_path.unlink()

    def test_prepare_instruction(self):
        """Test instruction preparation with timestamp."""
        # Create temporary instruction file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Test Instruction\nThis is a test instruction.")
            instruction_path = Path(f.name)

        try:
            runner = Runner(
                profile_path=Path("profile.md"), model="gpt-4.1-mini-2025-04-14"
            )

            with patch("blueskai.runner.datetime") as mock_datetime:
                mock_datetime.now.return_value.strftime.return_value = (
                    "2024-01-01 12:00:00 (Mon)"
                )

                instruction = runner.prepare_instruction(instruction_path)

                expected = """
            <!-- Current date and time: 2024-01-01 12:00:00 (Mon) -->
            # Test Instruction
This is a test instruction.
        """
                assert instruction == expected
        finally:
            # Clean up temporary file
            instruction_path.unlink()

    def test_prepare_instruction_file_not_found(self):
        """Test instruction preparation with non-existent file."""
        runner = Runner(
            profile_path=Path("profile.md"), model="gpt-4.1-mini-2025-04-14"
        )

        with pytest.raises(FileNotFoundError):
            runner.prepare_instruction(Path("non_existent.md"))

    def test_prepare_agent_file_not_found(self):
        """Test agent preparation with non-existent profile file."""
        runner = Runner(
            profile_path=Path("non_existent.md"), model="gpt-4.1-mini-2025-04-14"
        )

        with pytest.raises(FileNotFoundError):
            runner.prepare_agent([])
