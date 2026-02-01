"""Test module for the compute_rsi tool."""

from datetime import UTC, datetime
from typing import cast

import pandas as pd
import pytest
from hamcrest import (
    all_of,
    assert_that,
    close_to,
    empty,
    equal_to,
    greater_than,
    greater_than_or_equal_to,
    has_length,
    instance_of,
    is_,
    less_than_or_equal_to,
    not_,
)

from technical_analysis_mcp.models import Error, TimeSeries
from technical_analysis_mcp.tools.compute_rsi import compute_rsi, compute_rsi_from_time_series


def test_given_series_when_compute_rsi_then_returns_right_rsi_computation() -> None:
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


def test_given_insufficient_data_when_compute_rsi_then_returns_empty_series() -> None:
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


def test_given_invalid_window_when_compute_rsi_then_returns_empty_series() -> None:
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
async def test_given_right_input_when_compute_rsi_then_returns_right_rsi_calculation() -> None:
    """Test computing RSI with valid ticker."""
    result = await compute_rsi(
        ticker="AAPL",
        lookback_period="1mo",
        interval="1d",
        window=14,
        source="close",
    )

    assert_that(result, is_(instance_of(TimeSeries)))
    time_series = cast("TimeSeries", result)

    assert_that(time_series.ticker, equal_to("AAPL"))
    assert_that(time_series.points, has_length(greater_than(0)))

    for data_point in time_series.points:
        assert_that(data_point.value, all_of(greater_than_or_equal_to(0), less_than_or_equal_to(100)))


@pytest.mark.asyncio
async def test_given_large_window_when_compute_rsi_then_return_error() -> None:
    """Test error when window is too large."""
    result = await compute_rsi(
        ticker="AAPL",
        lookback_period="1mo",
        interval="1d",
        window=100,
        source="close",
    )

    assert_that(result, is_(instance_of(Error)))

    if isinstance(result, Error):
        assert_that(result.what, not_(empty()))


@pytest.mark.asyncio
async def test_given_negative_window_when_compute_rsi_then_returns_error() -> None:
    """Test computing RSI with negative window."""
    result = await compute_rsi(
        ticker="AAPL",
        lookback_period="1mo",
        interval="1d",
        window=-5,
        source="close",
    )

    assert_that(result, instance_of(Error))


@pytest.mark.asyncio
async def test_given_zero_window_when_compute_rsi_then_returns_error() -> None:
    """Test computing RSI with zero window."""
    result = await compute_rsi(
        ticker="AAPL",
        lookback_period="1mo",
        interval="1d",
        window=0,
        source="close",
    )

    assert_that(result, instance_of(Error))
