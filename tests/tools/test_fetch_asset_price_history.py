"""Test module for the fetch_asset_price_history tool."""

import pytest
from hamcrest import (
    assert_that,
    empty,
    has_properties,
    instance_of,
    is_,
    not_,
)

from technical_analysis_mcp.models import AssetPriceHistory, Error
from technical_analysis_mcp.tools import fetch_asset_price_history


@pytest.mark.asyncio
async def test_given_invalid_ticker_when_fetch_asset_price_history_then_returns_error() -> None:
    """Test fetching asset price history for an invalid ticker."""
    ticker = "INVALID_TICKER"
    period = "1mo"
    interval = "1d"

    result = await fetch_asset_price_history(ticker, period, interval)

    assert_that(result, is_(instance_of(Error)))

    if isinstance(result, Error):
        assert_that(result.what, is_(str))
        assert_that(result.what, is_(not_(empty())))


@pytest.mark.asyncio
async def test_given_valid_ticker_when_fetch_asset_price_history_then_returns_asset_price_history() -> None:
    """Test fetching asset price history for a valid ticker."""
    ticker = "AAPL"
    period = "1mo"
    interval = "1d"

    result = await fetch_asset_price_history(ticker, period, interval)

    assert_that(result, is_(instance_of(AssetPriceHistory)))

    if isinstance(result, AssetPriceHistory):
        assert_that(result, has_properties(ticker=ticker, period=period, interval=interval))
        assert_that(result.prices, is_(not_(empty())))


@pytest.mark.asyncio
async def test_given_edge_case_period_when_fetch_asset_price_history_then_returns_asset_price_history() -> None:
    """Test fetching asset price history for an edge case period."""
    ticker = "AAPL"
    period = "max"
    interval = "1d"

    result = await fetch_asset_price_history(ticker, period, interval)

    assert_that(result, is_(instance_of(AssetPriceHistory)))

    if isinstance(result, AssetPriceHistory):
        assert_that(result, has_properties(ticker=ticker, period=period, interval=interval))
        assert_that(result.prices, is_(not_(empty())))


@pytest.mark.asyncio
async def test_given_edge_case_interval_when_fetch_asset_price_history_then_returns_asset_price_history() -> None:
    """Test fetching asset price history for an edge case interval."""
    ticker = "AAPL"
    period = "1mo"
    interval = "1mo"

    result = await fetch_asset_price_history(ticker, period, interval)

    assert_that(result, is_(instance_of(AssetPriceHistory)))

    if isinstance(result, AssetPriceHistory):
        assert_that(result, has_properties(ticker=ticker, period=period, interval=interval))
        assert_that(result.prices, is_(not_(empty())))
