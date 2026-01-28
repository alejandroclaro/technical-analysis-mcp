"""Test module for the compute_sma tool."""

from datetime import UTC, datetime
from typing import cast

import pytest
from hamcrest import (
    assert_that,
    close_to,
    equal_to,
    greater_than,
    has_length,
    instance_of,
    is_,
)

from technical_analysis_mcp.models import Error, Price, TimeSeries
from technical_analysis_mcp.tools.compute_sma import (
    compute_sma,
    compute_sma_values,
    extract_price_data,
)


def test_should_extract_price_data_when_close_source_given() -> None:
    """Test extracting price data with close source."""
    prices = [
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
    ]

    result = extract_price_data(prices, "close")

    assert_that(result, has_length(2))
    assert_that(result[0][1], equal_to(102.0))
    assert_that(result[1][1], equal_to(105.0))


def test_should_extract_price_data_when_open_source_given() -> None:
    """Test extracting price data with open source."""
    prices = [
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
    ]

    result = extract_price_data(prices, "open")

    assert_that(result, has_length(1))
    assert_that(result[0][1], equal_to(100.0))


def test_should_extract_price_data_when_high_source_given() -> None:
    """Test extracting price data with high source."""
    prices = [
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
    ]

    result = extract_price_data(prices, "high")

    assert_that(result, has_length(1))
    assert_that(result[0][1], equal_to(105.0))


def test_should_extract_price_data_when_low_source_given() -> None:
    """Test extracting price data with low source."""
    prices = [
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
    ]

    result = extract_price_data(prices, "low")

    assert_that(result, has_length(1))
    assert_that(result[0][1], equal_to(95.0))


def test_should_compute_sma_values_when_valid_data_given() -> None:
    """Test computing SMA values with valid data."""
    prices = [100.0, 102.0, 105.0, 103.0, 107.0, 110.0, 108.0]
    period = 3

    result = compute_sma_values(prices, period)

    assert_that(result, has_length(5))  # 7-3+1 = 5
    assert_that(result[0], close_to(102.3333, 0.001))  # (100+102+105)/3
    assert_that(result[1], close_to(103.3333, 0.001))  # (102+105+103)/3
    assert_that(result[2], close_to(105.0, 0.001))  # (105+103+107)/3
    assert_that(result[3], close_to(106.6667, 0.001))  # (103+107+110)/3
    assert_that(result[4], close_to(108.3333, 0.001))  # (107+110+108)/3


def test_should_compute_sma_values_when_period_equals_length_given() -> None:
    """Test computing SMA values when period equals data length."""
    prices = [100.0, 102.0, 105.0]
    period = 3

    result = compute_sma_values(prices, period)

    assert_that(result, has_length(1))
    assert_that(result[0], close_to(102.3333, 0.001))


def test_should_return_empty_list_when_insufficient_data_given() -> None:
    """Test computing SMA values with insufficient data."""
    prices = [100.0, 102.0]
    period = 3

    result = compute_sma_values(prices, period)

    assert_that(result, has_length(0))


def test_should_return_empty_list_when_zero_or_negative_period_given() -> None:
    """Test computing SMA values with zero or negative period."""
    prices = [100.0, 102.0, 105.0]

    result_zero = compute_sma_values(prices, 0)
    assert_that(result_zero, has_length(0))

    result_negative = compute_sma_values(prices, -5)
    assert_that(result_negative, has_length(0))


@pytest.mark.asyncio
async def test_should_return_error_when_negative_window_given() -> None:
    """Test computing SMA with negative window."""
    result = await compute_sma(
        ticker="AAPL",
        source="close",
        period="1mo",
        interval="1d",
        window=-5,
    )

    assert_that(result, instance_of(Error))


@pytest.mark.asyncio
async def test_should_return_error_when_zero_window_given() -> None:
    """Test computing SMA with zero window."""
    result = await compute_sma(
        ticker="AAPL",
        source="close",
        period="1mo",
        interval="1d",
        window=0,
    )

    assert_that(result, instance_of(Error))


@pytest.mark.asyncio
async def test_should_compute_sma_when_valid_ticker_given() -> None:
    """Test computing SMA with valid ticker."""
    result = await compute_sma(
        ticker="AAPL",
        source="close",
        period="1mo",
        interval="1d",
        window=20,
    )

    assert_that(result, is_(instance_of(TimeSeries)))
    time_series = cast("TimeSeries", result)

    assert_that(time_series.ticker, equal_to("AAPL"))
    assert_that(time_series.data_points, has_length(greater_than(0)))

    # SMA values should be reasonable price values
    for data_point in time_series.data_points:
        # AAPL prices are typically > 0
        assert_that(data_point.value, greater_than(0.0))


@pytest.mark.asyncio
async def test_should_compute_sma_with_different_sources_given() -> None:
    """Test computing SMA with different price sources."""
    # Test with close prices
    result_close = await compute_sma(
        ticker="AAPL",
        source="close",
        period="1mo",
        interval="1d",
        window=10,
    )

    assert_that(result_close, is_(instance_of(TimeSeries)))

    # Test with open prices
    result_open = await compute_sma(
        ticker="AAPL",
        source="open",
        period="1mo",
        interval="1d",
        window=10,
    )

    assert_that(result_open, is_(instance_of(TimeSeries)))


@pytest.mark.asyncio
async def test_should_compute_sma_with_different_windows_given() -> None:
    """Test computing SMA with different window sizes."""
    # Test with window 10
    result_10 = await compute_sma(
        ticker="AAPL",
        source="close",
        period="1mo",
        interval="1d",
        window=10,
    )

    assert_that(result_10, is_(instance_of(TimeSeries)))
    time_series_10 = cast("TimeSeries", result_10)

    # Test with window 20
    result_20 = await compute_sma(
        ticker="AAPL",
        source="close",
        period="1mo",
        interval="1d",
        window=20,
    )

    assert_that(result_20, is_(instance_of(TimeSeries)))
    time_series_20 = cast("TimeSeries", result_20)

    # Window 20 should have fewer data points than window 10
    # (assuming we have at least 20 days of data)
    assert_that(len(time_series_20.data_points), equal_to(len(time_series_10.data_points) - 10))
