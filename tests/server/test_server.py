"""Test MCP Server."""

from typing import Any, cast

import pytest
from fastmcp import Client
from hamcrest import (
    assert_that,
    contains_inanyorder,
    equal_to,
    has_key,
    is_,
    not_,
    not_none,
)

from technical_analysis_mcp.server.server import server


@pytest.mark.asyncio
async def test_given_server_initialized_when_ping_then_returns_true() -> None:
    """Test the MCP server lifecycle."""
    async with Client(server) as client:
        assert_that(await client.ping(), is_(True))


@pytest.mark.asyncio
async def test_given_server_initialized_when_get_instructions_then_returns_non_empty_instructions() -> None:
    """Test that the server provides instructions."""
    async with Client(server) as client:
        instructions = None

        if client.initialize_result is not None:
            instructions = client.initialize_result.instructions

        assert_that(instructions, is_(not_none()))
        instructions = cast("str", instructions)
        assert_that(instructions.strip(), is_(not_(equal_to(""))))


@pytest.mark.asyncio
async def test_given_server_initialized_when_list_tools_then_returns_registered_tools() -> None:
    """Test that tools are properly registered with expected properties."""
    expected_tools = ["get_ticker_information"]

    async with Client(server) as client:
        tools = await client.list_tools()
        actual_names = [tool.name for tool in tools]

        assert_that(actual_names, contains_inanyorder(*expected_tools))

        for tool in tools:
            assert_that(tool.description, is_(not_none()))
            assert_that(tool.inputSchema, is_(not_none()))
            assert_that(tool.outputSchema, is_(not_none()))

            description = cast("str", tool.description)
            output_schema = cast("dict[str, Any]", tool.outputSchema)

            assert_that(description.strip(), is_(not_(equal_to(""))))
            assert_that(output_schema, has_key("properties"))
            assert_that(output_schema["properties"], is_(not_none()))


@pytest.mark.asyncio
async def test_given_valid_ticker_when_call_get_ticker_information_then_returns_ticker_data() -> None:
    """Test the get_ticker_information tool directly."""
    async with Client(server) as client:
        result = await client.call_tool("get_ticker_information", {"ticker": "AAPL"})
        assert_that(result.structured_content, is_(not_none()))

        structured_content = cast("dict[str, Any]", result.structured_content)
        assert_that(structured_content, has_key("result"))

        result_data = structured_content["result"]
        assert_that(result_data["symbol"], equal_to("AAPL"))

        result = await client.call_tool("get_ticker_information", {"ticker": "INVALID_TICKER"})
        assert_that(result.structured_content, is_(not_none()))

        structured_content = cast("dict[str, Any]", result.structured_content)
        assert_that(structured_content, has_key("result"))

        result_data = structured_content["result"]
        assert_that(result_data, has_key("what"))
