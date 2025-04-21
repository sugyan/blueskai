"""Tests for Blueskai main module."""

from unittest.mock import patch

from blueskai.main import process_instruction


@patch("blueskai.main.Agent")
@patch("blueskai.main.Runner.run_sync")
def test_process_instruction(mock_runner, mock_agent):
    """Test processing an instruction."""
    # Mock the agent's response
    mock_runner.return_value.final_output = "Test response"

    result = process_instruction("# Test instruction")

    assert result["success"] is True
    assert result["response"] == "Test response"
