"""Test MCP REPL."""

from unittest.mock import AsyncMock, MagicMock, patch

from hamcrest import assert_that, is_

from technical_analysis_mcp.repl.repl import Repl


def test_get_instructions() -> None:
    """Test getting server instructions."""
    with patch("technical_analysis_mcp.repl.repl.Client") as mock_client_class:
        mock_init_result = MagicMock()
        mock_init_result.instructions = "Test instructions"

        mock_client = AsyncMock()
        mock_client.initialize_result = mock_init_result
        mock_client_class.return_value = mock_client

        repl = Repl()
        repl.do_get_instructions("")


def test_list_tools() -> None:
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


def test_get_tool_description() -> None:
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


def test_call_tool() -> None:
    """Test calling a tool."""
    with patch("technical_analysis_mcp.repl.repl.Client") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.call_tool = AsyncMock(return_value={"result": "success"})
        mock_client_class.return_value = mock_client

        repl = Repl()
        repl.do_call_tool('test_tool {"param": "value"}')

        mock_client.call_tool.assert_called_once_with("test_tool", {"param": "value"})


def test_exit_commands() -> None:
    """Test exit commands."""
    repl = Repl()

    assert_that(repl.do_exit(""), is_(True))
    assert_that(repl.do_quit(""), is_(True))
    assert_that(repl.do_EOF(""), is_(True))
