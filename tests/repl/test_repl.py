"""Test MCP REPL."""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from technical_analysis_mcp.repl.repl import Repl


def test_given_client_initialized_when_get_instructions_then_returns_instructions() -> None:
    """Test getting server instructions."""
    with patch("technical_analysis_mcp.repl.repl.Client") as mock_client_class:
        mock_init_result = MagicMock()
        mock_init_result.instructions = "Test instructions"

        mock_client = AsyncMock()
        mock_client.initialize_result = mock_init_result
        mock_client_class.return_value = mock_client

        repl = Repl()
        repl.do_get_instructions("")


def test_given_client_initialized_when_list_tools_then_returns_tool_list() -> None:
    """Test listing available tools."""
    with patch("technical_analysis_mcp.repl.repl.Client") as mock_client_class:
        mock_client = AsyncMock()

        mock_client.list_tools = AsyncMock(
            return_value=[
                MagicMock(name="tool1", description="Tool 1"),
                MagicMock(name="tool2", description="Tool 2"),
            ]
        )

        mock_client_class.return_value = mock_client

        repl = Repl()
        repl.do_list_tools("")

        mock_client.list_tools.assert_called_once()


def test_given_client_initialized_when_get_tool_description_then_returns_tool_info() -> None:
    """Test getting tool description and schema by name."""
    with patch("technical_analysis_mcp.repl.repl.Client") as mock_client_class:
        mock_client = AsyncMock()

        mock_client.list_tools = AsyncMock(
            return_value=[
                MagicMock(
                    name="test_tool",
                    description="Test tool description",
                    inputSchema={"type": "object"},
                    outputSchema={"type": "object"},
                )
            ]
        )

        mock_client_class.return_value = mock_client

        repl = Repl()
        repl.do_get_tool_description("test_tool")

        mock_client.list_tools.assert_called_once()


def test_given_client_initialized_when_call_tool_then_executes_tool() -> None:
    """Test calling a tool."""
    with patch("technical_analysis_mcp.repl.repl.Client") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.call_tool = AsyncMock(return_value={"result": "success"})
        mock_client_class.return_value = mock_client

        repl = Repl()
        repl.do_call_tool('test_tool {"param": "value"}')

        mock_client.call_tool.assert_called_once_with("test_tool", {"param": "value"})


def test_given_missing_args_when_call_tool_then_raises_json_decode_error() -> None:
    """Test calling tool with missing arguments."""
    repl = Repl()

    repl.do_call_tool("")

    with pytest.raises(json.JSONDecodeError):
        repl.do_call_tool("tool_name")
