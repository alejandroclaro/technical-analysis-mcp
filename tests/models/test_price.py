"""Test module for the Price model."""

from datetime import UTC, datetime

import pandas as pd
import pytest
from hamcrest import assert_that, close_to, equal_to, has_length, instance_of

from technical_analysis_mcp.models import Price
from technical_analysis_mcp.models.price import convert_prices_to_panda_series


@pytest.fixture
def prices() -> list[Price]:
    """Create sample price data for testing."""
    return [
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
    ]


def test_given_close_price_when_convert_to_series_then_only_include_close_prices(prices: list[Price]) -> None:
    """Test getting price series with close source."""
    result = convert_prices_to_panda_series(prices, "close")

    assert_that(result, instance_of(pd.Series))
    assert_that(result, has_length(3))
    assert_that(result.iloc[0], close_to(102.0, 0.001))
    assert_that(result.iloc[1], close_to(105.0, 0.001))
    assert_that(result.iloc[2], close_to(108.0, 0.001))

    assert_that(result.index[0], equal_to(datetime(2024, 1, 1, tzinfo=UTC)))
    assert_that(result.index[1], equal_to(datetime(2024, 1, 2, tzinfo=UTC)))
    assert_that(result.index[2], equal_to(datetime(2024, 1, 3, tzinfo=UTC)))


def test_given_open_price_when_convert_to_series_then_only_include_close_prices(prices: list[Price]) -> None:
    """Test getting price series with open source."""
    result = convert_prices_to_panda_series(prices, "open")

    assert_that(result, instance_of(pd.Series))
    assert_that(result, has_length(3))
    assert_that(result.iloc[0], close_to(100.0, 0.001))
    assert_that(result.iloc[1], close_to(102.0, 0.001))
    assert_that(result.iloc[2], close_to(105.0, 0.001))


def test_given_high_price_when_convert_to_series_then_only_include_close_prices(prices: list[Price]) -> None:
    """Test getting price series with high source."""
    result = convert_prices_to_panda_series(prices, "high")

    assert_that(result, instance_of(pd.Series))
    assert_that(result, has_length(3))
    assert_that(result.iloc[0], close_to(105.0, 0.001))
    assert_that(result.iloc[1], close_to(107.0, 0.001))
    assert_that(result.iloc[2], close_to(110.0, 0.001))


def test_given_low_price_when_convert_to_series_then_only_include_close_prices(prices: list[Price]) -> None:
    """Test getting price series with low source."""
    result = convert_prices_to_panda_series(prices, "low")

    assert_that(result, instance_of(pd.Series))
    assert_that(result, has_length(3))
    assert_that(result.iloc[0], close_to(95.0, 0.001))
    assert_that(result.iloc[1], close_to(97.0, 0.001))
    assert_that(result.iloc[2], close_to(100.0, 0.001))
