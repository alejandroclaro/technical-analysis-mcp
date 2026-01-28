"""Test MCP Server."""

from typing import Any, cast

import pytest
from fastmcp import Client
from fastmcp.exceptions import ToolError
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
    expected_tools = ["get_ticker_information", "get_asset_price_history", "get_rsi"]

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
    """Test the get_ticker_information tool with valid ticker."""
    async with Client(server) as client:
        result = await client.call_tool("get_ticker_information", {"ticker": "AAPL"})
        assert_that(result.structured_content, is_(not_none()))

        structured_content = cast("dict[str, Any]", result.structured_content)
        assert_that(structured_content, has_key("result"))

        result_data = structured_content["result"]
        assert_that(result_data["symbol"], equal_to("AAPL"))


@pytest.mark.asyncio
async def test_given_invalid_ticker_when_call_get_ticker_information_then_returns_error() -> None:
    """Test the get_ticker_information tool with invalid ticker."""
    async with Client(server) as client:
        result = await client.call_tool("get_ticker_information", {"ticker": "INVALID_TICKER"})
        assert_that(result.structured_content, is_(not_none()))

        structured_content = cast("dict[str, Any]", result.structured_content)
        assert_that(structured_content, has_key("result"))

        result_data = structured_content["result"]
        assert_that(result_data, has_key("what"))


@pytest.mark.asyncio
async def test_given_valid_parameters_when_call_get_asset_price_history_then_returns_price_data() -> None:
    """Test the get_asset_price_history tool with valid parameters."""
    async with Client(server) as client:
        params = {"ticker": "AAPL", "period": "1mo", "interval": "1d"}
        result = await client.call_tool("get_asset_price_history", params)
        assert_that(result.structured_content, is_(not_none()))

        structured_content = cast("dict[str, Any]", result.structured_content)
        assert_that(structured_content, has_key("result"))

        result_data = structured_content["result"]
        assert_that(result_data["ticker"], equal_to("AAPL"))
        assert_that(result_data["period"], equal_to("1mo"))
        assert_that(result_data["interval"], equal_to("1d"))
        assert_that(result_data, has_key("prices"))


@pytest.mark.asyncio
async def test_given_invalid_ticker_when_call_get_asset_price_history_then_returns_error() -> None:
    """Test the get_asset_price_history tool with invalid ticker."""
    async with Client(server) as client:
        params = {"ticker": "INVALID_TICKER", "period": "1mo", "interval": "1d"}
        result = await client.call_tool("get_asset_price_history", params)
        assert_that(result.structured_content, is_(not_none()))

        structured_content = cast("dict[str, Any]", result.structured_content)
        assert_that(structured_content, has_key("result"))

        result_data = structured_content["result"]
        assert_that(result_data, has_key("what"))


@pytest.mark.asyncio
async def test_given_valid_parameters_when_call_get_rsi_then_returns_rsi_data() -> None:
    """Test the get_rsi tool with valid parameters."""
    async with Client(server) as client:
        params = {
            "ticker": "AAPL",
            "source": "close",
            "period": "1mo",
            "interval": "1d",
            "candles": 14,
        }

        result = await client.call_tool("get_rsi", params)
        assert_that(result.structured_content, is_(not_none()))

        structured_content = cast("dict[str, Any]", result.structured_content)
        assert_that(structured_content, has_key("result"))

        result_data = structured_content["result"]
        assert_that(result_data["ticker"], equal_to("AAPL"))
        assert_that(result_data, has_key("data_points"))


@pytest.mark.asyncio
async def test_given_invalid_ticker_when_call_get_rsi_then_returns_error() -> None:
    """Test the get_rsi tool with invalid ticker."""
    async with Client(server) as client:
        params = {
            "ticker": "INVALID_TICKER",
            "source": "close",
            "period": "1mo",
            "interval": "1d",
            "candles": 14,
        }

        result = await client.call_tool("get_rsi", params)
        assert_that(result.structured_content, is_(not_none()))

        structured_content = cast("dict[str, Any]", result.structured_content)
        assert_that(structured_content, has_key("result"))

        result_data = structured_content["result"]
        assert_that(result_data, has_key("what"))


@pytest.mark.asyncio
async def test_given_invalid_period_when_call_get_rsi_then_returns_error() -> None:
    """Test the get_rsi tool with invalid period."""
    async with Client(server) as client:
        params = {
            "ticker": "AAPL",
            "source": "close",
            "period": "invalid_period",
            "interval": "1d",
            "candles": 14,
        }

        with pytest.raises(ToolError):
            await client.call_tool("get_rsi", params)


@pytest.mark.asyncio
async def test_given_invalid_interval_when_call_get_rsi_then_returns_error() -> None:
    """Test the get_rsi tool with invalid interval."""
    async with Client(server) as client:
        params = {
            "ticker": "AAPL",
            "source": "close",
            "period": "1mo",
            "interval": "invalid_interval",
            "candles": 14,
        }

        with pytest.raises(ToolError):
            await client.call_tool("get_rsi", params)


@pytest.mark.asyncio
async def test_given_invalid_candles_when_call_get_rsi_then_returns_error() -> None:
    """Test the get_rsi tool with invalid candles parameter."""
    async with Client(server) as client:
        params = {
            "ticker": "AAPL",
            "source": "close",
            "period": "1mo",
            "interval": "1d",
            "candles": 0,  # Invalid: must be positive
        }

        result = await client.call_tool("get_rsi", params)
        assert_that(result.structured_content, is_(not_none()))

        structured_content = cast("dict[str, Any]", result.structured_content)
        assert_that(structured_content, has_key("result"))

        result_data = structured_content["result"]
        assert_that(result_data, has_key("what"))
