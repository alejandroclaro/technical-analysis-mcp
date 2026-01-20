"""Test fetch_ticker_information function."""

import pytest
from hamcrest import (
    assert_that,
    empty,
    has_properties,
    instance_of,
    is_,
    not_,
)

from technical_analysis_mcp.models import Error, TickerInformation
from technical_analysis_mcp.tools import fetch_ticker_information


@pytest.mark.asyncio
async def test_given_valid_ticker_when_fetch_ticker_information_then_returns_ticker_information() -> None:
    """Test fetching ticker information for a valid ticker."""
    result = await fetch_ticker_information("AAPL")

    assert_that(result, is_(instance_of(TickerInformation)))
    assert_that(result, has_properties(symbol="AAPL"))


@pytest.mark.asyncio
async def test_given_invalid_ticker_when_fetch_ticker_information_then_returns_error() -> None:
    """Test fetching ticker information for an invalid ticker."""
    result = await fetch_ticker_information("INVALID_TICKER")

    assert_that(result, is_(instance_of(Error)))

    if isinstance(result, Error):
        assert_that(result.what, is_(str))
        assert_that(result.what, is_(not_(empty())))
