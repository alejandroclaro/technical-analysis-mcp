"""Test fetch_ticker_information function."""

import pytest
from hamcrest import (
    assert_that,
    has_key,
    is_,
    not_,
)

from src.technical_analysis_mcp.tools.fetch_ticker_information import fetch_ticker_information


@pytest.mark.asyncio
async def test_fetch_ticker_information_success() -> None:
    """Test fetching ticker information for a valid ticker."""
    result = await fetch_ticker_information("AAPL")
    assert_that(result, is_(dict))
    assert_that(result, not_(has_key("error")))
    assert_that(result, has_key("symbol"))
    assert_that(result["symbol"], is_("AAPL"))


@pytest.mark.asyncio
async def test_fetch_ticker_information_failure() -> None:
    """Test fetching ticker information for an invalid ticker."""
    result = await fetch_ticker_information("INVALID_TICKER")
    assert_that(result, is_(dict))
    assert_that(result, not_(has_key("symbol")))
    assert_that(result, has_key("error"))
    assert_that(result["error"], is_(str))
