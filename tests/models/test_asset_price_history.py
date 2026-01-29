"""Test module for the AssetPriceHistory model."""

from datetime import UTC, datetime

import pandas as pd
import pytest
from hamcrest import assert_that, close_to, equal_to, has_length, instance_of

from technical_analysis_mcp.models import AssetPriceHistory, Price, get_price_series


@pytest.fixture
def history() -> AssetPriceHistory:
    """Create sample price data for testing."""
    return AssetPriceHistory(
        ticker="AAPL",
        period="ytd",
        interval="1d",
        prices=[
            Price(
                date=datetime(2024, 1, 1, tzinfo=UTC),
                open=100.0,
                high=105.0,
                low=95.0,
                close=102.0,
                volume=1000,
                dividends=0.0,
                stock_splits=0.0,
            ),
            Price(
                date=datetime(2024, 1, 2, tzinfo=UTC),
                open=102.0,
                high=107.0,
                low=97.0,
                close=105.0,
                volume=1500,
                dividends=0.0,
                stock_splits=0.0,
            ),
            Price(
                date=datetime(2024, 1, 3, tzinfo=UTC),
                open=105.0,
                high=110.0,
                low=100.0,
                close=108.0,
                volume=2000,
                dividends=0.0,
                stock_splits=0.0,
            ),
        ],
    )


def test_should_get_price_series_when_close_source_given(history: AssetPriceHistory) -> None:
    """Test getting price series with close source."""
    result = get_price_series(history, "close")

    assert_that(result, instance_of(pd.Series))
    assert_that(result, has_length(3))
    assert_that(result.iloc[0], close_to(102.0, 0.001))
    assert_that(result.iloc[1], close_to(105.0, 0.001))
    assert_that(result.iloc[2], close_to(108.0, 0.001))

    assert_that(result.index[0], equal_to(datetime(2024, 1, 1, tzinfo=UTC)))
    assert_that(result.index[1], equal_to(datetime(2024, 1, 2, tzinfo=UTC)))
    assert_that(result.index[2], equal_to(datetime(2024, 1, 3, tzinfo=UTC)))


def test_should_get_price_series_when_open_source_given(history: AssetPriceHistory) -> None:
    """Test getting price series with open source."""
    result = get_price_series(history, "open")

    assert_that(result, instance_of(pd.Series))
    assert_that(result, has_length(3))
    assert_that(result.iloc[0], close_to(100.0, 0.001))
    assert_that(result.iloc[1], close_to(102.0, 0.001))
    assert_that(result.iloc[2], close_to(105.0, 0.001))


def test_should_get_price_series_when_high_source_given(history: AssetPriceHistory) -> None:
    """Test getting price series with high source."""
    result = get_price_series(history, "high")

    assert_that(result, instance_of(pd.Series))
    assert_that(result, has_length(3))
    assert_that(result.iloc[0], close_to(105.0, 0.001))
    assert_that(result.iloc[1], close_to(107.0, 0.001))
    assert_that(result.iloc[2], close_to(110.0, 0.001))


def test_should_get_price_series_when_low_source_given(history: AssetPriceHistory) -> None:
    """Test getting price series with low source."""
    result = get_price_series(history, "low")

    assert_that(result, instance_of(pd.Series))
    assert_that(result, has_length(3))
    assert_that(result.iloc[0], close_to(95.0, 0.001))
    assert_that(result.iloc[1], close_to(97.0, 0.001))
    assert_that(result.iloc[2], close_to(100.0, 0.001))
