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

from src.technical_analysis_mcp.server.server import server


@pytest.mark.asyncio
async def test_server_runs() -> None:
    """Test the MCP server lifecycle."""
    async with Client(server) as client:
        assert_that(await client.ping(), is_(True))


@pytest.mark.asyncio
async def test_server_provides_instructions() -> None:
    """Test that the server provides instructions."""
    async with Client(server) as client:
        instructions = None

        if client.initialize_result is not None:
            instructions = client.initialize_result.instructions

        assert_that(instructions, is_(not_none()))
        instructions = cast("str", instructions)
        assert_that(instructions.strip(), is_(not_(equal_to(""))))


@pytest.mark.asyncio
async def test_tools_are_properly_registered() -> None:
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
