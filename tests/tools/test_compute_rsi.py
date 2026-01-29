"""Test module for the compute_rsi tool."""

from datetime import UTC, datetime
from typing import cast

import pandas as pd
import pytest
from hamcrest import (
    all_of,
    assert_that,
    close_to,
    equal_to,
    greater_than,
    greater_than_or_equal_to,
    has_length,
    instance_of,
    is_,
    less_than_or_equal_to,
)

from technical_analysis_mcp.models import TimeSeries
from technical_analysis_mcp.tools.compute_rsi import compute_rsi, compute_rsi_from_time_series


def test_should_compute_rsi_from_time_series_when_valid_data_given() -> None:
    """Test computing RSI values from time series with valid data using pandas."""
    dates = [
        datetime(2024, 1, 1, tzinfo=UTC),
        datetime(2024, 1, 2, tzinfo=UTC),
        datetime(2024, 1, 3, tzinfo=UTC),
        datetime(2024, 1, 4, tzinfo=UTC),
        datetime(2024, 1, 5, tzinfo=UTC),
        datetime(2024, 1, 6, tzinfo=UTC),
        datetime(2024, 1, 7, tzinfo=UTC),
        datetime(2024, 1, 8, tzinfo=UTC),
        datetime(2024, 1, 9, tzinfo=UTC),
        datetime(2024, 1, 10, tzinfo=UTC),
        datetime(2024, 1, 11, tzinfo=UTC),
        datetime(2024, 1, 12, tzinfo=UTC),
        datetime(2024, 1, 13, tzinfo=UTC),
        datetime(2024, 1, 14, tzinfo=UTC),
        datetime(2024, 1, 15, tzinfo=UTC),
        datetime(2024, 1, 16, tzinfo=UTC),
    ]

    prices = [
        100.0,
        102.0,
        105.0,
        103.0,
        107.0,
        110.0,
        108.0,
        106.0,
        104.0,
        105.0,
        107.0,
        109.0,
        111.0,
        109.0,
        112.0,
        110.0,
    ]

    series = pd.Series(prices, index=dates)
    window = 14

    result = compute_rsi_from_time_series(series, window)
    assert_that(result, has_length(2))

    for value in result.to_numpy():
        assert_that(value, close_to(50, 50))


def test_should_return_empty_series_when_insufficient_data_given() -> None:
    """Test computing RSI values with insufficient data."""
    dates = [
        datetime(2024, 1, 1, tzinfo=UTC),
        datetime(2024, 1, 2, tzinfo=UTC),
        datetime(2024, 1, 3, tzinfo=UTC),
        datetime(2024, 1, 4, tzinfo=UTC),
        datetime(2024, 1, 5, tzinfo=UTC),
    ]

    prices = [100.0, 102.0, 105.0, 103.0, 107.0]
    series = pd.Series(prices, index=dates)
    window = 14

    result = compute_rsi_from_time_series(series, window)

    assert_that(result, has_length(0))


def test_should_return_empty_series_when_zero_or_negative_window_given() -> None:
    """Test computing RSI values with zero or negative window."""
    dates = [
        datetime(2024, 1, 1, tzinfo=UTC),
        datetime(2024, 1, 2, tzinfo=UTC),
        datetime(2024, 1, 3, tzinfo=UTC),
    ]

    prices = [100.0, 102.0, 105.0]
    series = pd.Series(prices, index=dates)

    result_zero = compute_rsi_from_time_series(series, 0)
    assert_that(result_zero, has_length(0))

    result_negative = compute_rsi_from_time_series(series, -5)
    assert_that(result_negative, has_length(0))


@pytest.mark.asyncio
async def test_should_compute_rsi_when_valid_ticker_given() -> None:
    """Test computing RSI with valid ticker."""
    result = await compute_rsi(
        ticker="AAPL",
        period="1mo",
        interval="1d",
        window=14,
        source="close",
    )

    assert_that(result, is_(instance_of(TimeSeries)))
    time_series = cast("TimeSeries", result)

    assert_that(time_series.ticker, equal_to("AAPL"))
    assert_that(time_series.data_points, has_length(greater_than(0)))

    for data_point in time_series.data_points:
        assert_that(data_point.value, all_of(greater_than_or_equal_to(0), less_than_or_equal_to(100)))
