"""Test MCP REPL."""

import cmd
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastmcp.client.client import CallToolResult
from hamcrest import assert_that, equal_to, is_, not_none

from technical_analysis_mcp.repl.repl import Repl


def test_given_repl_initialized_when_ping_then_works() -> None:
    """Test basic REPL initialization."""
    repl = Repl()
    assert_that(repl, is_(not_none()))
    assert_that(repl.prompt, equal_to("mcp> "))


def test_given_exit_command_when_executed_then_returns_true() -> None:
    """Test the exit command returns True to exit REPL."""
    repl = Repl()

    with patch("sys.stdout.write") as write_mock:
        result = repl.do_exit("")

        assert_that(result, is_(True))
        write_mock.assert_called_once_with("Goodbye!\n")


def test_given_quit_command_when_executed_then_returns_true() -> None:
    """Test the quit command returns True to exit REPL."""
    repl = Repl()

    with patch("sys.stdout.write") as write_mock:
        result = repl.do_quit("")

        assert_that(result, is_(True))
        write_mock.assert_called_once_with("Goodbye!\n")


def test_given_eof_command_when_executed_then_returns_true() -> None:
    """Test the EOF command returns True to exit REPL."""
    repl = Repl()

    with patch("sys.stdout.write") as write_mock:
        result = repl.do_EOF("")

        assert_that(result, is_(True))
        assert_that(write_mock.call_count, equal_to(2))
        write_mock.assert_any_call("\n")


def test_given_history_command_when_executed_then_displays_command_history() -> None:
    """Test the history command displays previously entered commands."""
    repl = Repl()

    repl.precmd("get_instructions")
    repl.precmd("list_tools")

    with patch("sys.stdout.write") as write_mock:
        repl.do_history("")

        calls = [call[0][0] for call in write_mock.call_args_list]
        assert_that(any("get_instructions" in call for call in calls), is_(True))
        assert_that(any("list_tools" in call for call in calls), is_(True))


def test_given_exception_in_onecmd_when_executed_then_handles_gracefully() -> None:
    """Test that exceptions in command execution are handled gracefully."""
    repl = Repl()

    with (
        patch.object(cmd.Cmd, "onecmd", side_effect=Exception("Test error")),
        patch("sys.stderr.write") as mock_stderr,
    ):
        result = repl.onecmd("some_command")
        assert_that(result, is_(False))

        error_calls = [call[0][0] for call in mock_stderr.call_args_list]
        assert_that(any("Exception: Test error" in call for call in error_calls), is_(True))
        assert_that(any("Check yout internet connection." in call for call in error_calls), is_(True))


def test_given_client_initialized_when_get_instructions_then_returns_instructions() -> None:
    """Test getting server instructions writes non-empty output."""
    with patch("technical_analysis_mcp.repl.repl.Client") as client_class_mock:
        mock_init_result = MagicMock()
        mock_init_result.instructions = "Test instructions"

        client_mock = AsyncMock()
        client_mock.initialize_result = mock_init_result
        client_class_mock.return_value = client_mock

        repl = Repl()

        with patch("sys.stdout.write") as write_mock:
            repl.do_get_instructions("")

            assert_that(write_mock.called, is_(True))
            write_calls = [call[0][0] for call in write_mock.call_args_list]
            combined_output = "".join(write_calls)
            assert_that("Test instructions" in combined_output, is_(True))
            assert_that(combined_output.strip(), not_none())


def test_given_client_initialized_when_list_tools_then_returns_tool_list() -> None:
    """Test listing available tools writes tool names to output."""
    with patch("technical_analysis_mcp.repl.repl.Client") as client_class_mock:
        client_mock = AsyncMock()

        client_mock.list_tools = AsyncMock(
            return_value=[
                MagicMock(name="tool1", description="Tool 1"),
                MagicMock(name="tool2", description="Tool 2"),
            ]
        )

        client_class_mock.return_value = client_mock

        repl = Repl()

        with patch("sys.stdout.write") as write_mock:
            repl.do_list_tools("")

            client_mock.list_tools.assert_called_once()
            write_calls = [call[0][0] for call in write_mock.call_args_list]
            combined_output = "".join(write_calls)

            # If tool names are present, output is clearly not empty
            assert_that("tool1" in combined_output, is_(True))
            assert_that("tool2" in combined_output, is_(True))


def test_given_client_initialized_when_get_tool_description_then_returns_tool_info() -> None:
    """Test getting tool description calls the appropriate methods."""
    with patch("technical_analysis_mcp.repl.repl.Client") as client_class_mock:
        client_mock = AsyncMock()

        client_mock.list_tools = AsyncMock(
            return_value=[
                MagicMock(
                    name="test_tool",
                    description="Test tool description",
                    inputSchema={"type": "object"},
                    outputSchema={"type": "object"},
                )
            ]
        )

        client_class_mock.return_value = client_mock

        repl = Repl()

        with patch("sys.stdout.write") as write_mock:
            repl.do_get_tool_description("test_tool")

            client_mock.list_tools.assert_called_once()
            write_mock.reset_mock()
            repl.do_get_tool_description("")
            write_mock.assert_called_with("Usage: tool <tool_name>\n")


def test_given_client_initialized_when_call_tool_then_executes_tool() -> None:
    """Test calling a tool with valid arguments."""
    with patch("technical_analysis_mcp.repl.repl.Client") as client_class_mock:
        client_mock = AsyncMock()
        client_mock.call_tool = AsyncMock(return_value=CallToolResult(content=[], structured_content=None, meta=None))
        client_class_mock.return_value = client_mock

        repl = Repl()
        repl.do_call_tool('test_tool {"param": "value"}')

        client_mock.call_tool.assert_called_once_with("test_tool", {"param": "value"})


def test_given_missing_args_when_call_tool_then_raises_json_decode_error() -> None:
    """Test calling tool with missing arguments."""
    repl = Repl()

    repl.do_call_tool("")

    with pytest.raises(json.JSONDecodeError):
        repl.do_call_tool("tool_name")


def test_given_missing_tool_name_when_get_tool_description_then_shows_usage() -> None:
    """Test get_tool_description validation with missing tool name."""
    repl = Repl()

    with patch("sys.stdout.write") as write_mock:
        repl.do_get_tool_description("")
        write_mock.assert_called_once_with("Usage: tool <tool_name>\n")


def test_given_missing_arguments_when_call_tool_then_shows_usage() -> None:
    """Test call_tool validation with missing arguments."""
    repl = Repl()

    with patch("sys.stdout.write") as write_mock:
        repl.do_call_tool("")
        write_mock.assert_called_once_with("Usage: call <tool_name> <args>\n")
