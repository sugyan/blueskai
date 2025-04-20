"""Tests for Blueskai main module."""

import pytest
from unittest.mock import patch, mock_open
import os
from pathlib import Path

from blueskai.main import (
    process_markdown_instruction,
    get_instruction_from_file,
    get_default_instruction,
    process_instruction,
    main,
)


def test_process_markdown_instruction():
    """Test that the instruction processor returns expected format."""
    # Test with basic instruction
    instruction = "# Test Instruction\n\nThis is a test."
    result = process_markdown_instruction(instruction)
    
    assert isinstance(result, dict)
    assert result["status"] == "success"
    assert "response" in result
    assert "Processed instruction" in result["response"]
    
    # Test with empty instruction
    result = process_markdown_instruction("")
    assert result["status"] == "success"
    assert "response" in result


def test_get_instruction_from_file_success():
    """Test reading instruction from file successfully."""
    test_content = "# Test Instruction"
    
    with patch("pathlib.Path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=test_content)):
            result = get_instruction_from_file("test.md")
            
    assert result["status"] == "success"
    assert result["instruction"] == test_content


def test_get_instruction_from_file_not_found():
    """Test reading instruction from nonexistent file."""
    with patch("pathlib.Path.exists", return_value=False):
        result = get_instruction_from_file("nonexistent.md")
        
    assert result["status"] == "error"
    assert "File not found" in result["error"]


def test_get_instruction_from_file_read_error():
    """Test handling file read errors."""
    with patch("pathlib.Path.exists", return_value=True):
        with patch("builtins.open", side_effect=IOError("Permission denied")):
            result = get_instruction_from_file("test.md")
            
    assert result["status"] == "error"
    assert "Error reading file" in result["error"]


def test_get_default_instruction():
    """Test the default instruction content."""
    instruction = get_default_instruction()
    assert "Sample Task" in instruction
    assert isinstance(instruction, str)


@patch("blueskai.main.process_markdown_instruction")
def test_process_instruction(mock_process, capsys):
    """Test processing an instruction and printing the result."""
    # Test successful processing
    mock_process.return_value = {"status": "success", "response": "Test response"}
    
    result = process_instruction("# Test instruction")
    
    assert result["status"] == "success"
    captured = capsys.readouterr()
    assert "Agent Response:" in captured.out
    assert "Test response" in captured.out
    
    # Test error processing
    mock_process.return_value = {"status": "error", "error": "Test error"}
    
    result = process_instruction("# Test instruction")
    
    assert result["status"] == "error"
    captured = capsys.readouterr()
    assert "Error: Test error" in captured.out


@patch("blueskai.main.get_default_instruction")
@patch("blueskai.main.process_instruction")
def test_main_default(mock_process, mock_default):
    """Test main function with default instruction."""
    mock_default.return_value = "# Default instruction"
    mock_process.return_value = {"status": "success", "response": "Default processed"}
    
    result = main()
    
    mock_default.assert_called_once()
    mock_process.assert_called_once_with("# Default instruction")
    assert result == {"status": "success", "response": "Default processed"}


@patch("blueskai.main.get_instruction_from_file")
@patch("blueskai.main.process_instruction")
def test_main_with_filepath(mock_process, mock_get_file):
    """Test main function with filepath provided."""
    mock_get_file.return_value = {"status": "success", "instruction": "# Test from file"}
    mock_process.return_value = {"status": "success", "response": "File processed"}
    
    result = main("test.md")
    
    mock_get_file.assert_called_once_with("test.md")
    mock_process.assert_called_once_with("# Test from file")
    assert result == {"status": "success", "response": "File processed"}


@patch("blueskai.main.get_instruction_from_file")
def test_main_with_file_error(mock_get_file, capsys):
    """Test main function with file error."""
    mock_get_file.return_value = {"status": "error", "error": "File not found: nonexistent.md"}
    
    result = main("nonexistent.md")
    
    assert result["status"] == "error"
    assert result["error"] == "File not found: nonexistent.md"
    captured = capsys.readouterr()
    assert "Error: File not found" in captured.out
    assert "Usage:" in captured.out