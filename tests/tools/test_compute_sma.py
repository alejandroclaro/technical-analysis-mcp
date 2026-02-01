"""Test module for the compute_sma tool."""

from datetime import UTC, datetime
from typing import cast

import pandas as pd
import pytest
from hamcrest import (
    assert_that,
    close_to,
    empty,
    equal_to,
    greater_than,
    has_length,
    instance_of,
    is_,
    not_,
)

from technical_analysis_mcp.models import Error, TimeSeries
from technical_analysis_mcp.tools.compute_sma import (
    compute_sma,
    compute_sma_from_time_series,
)


def test_given_series_when_compute_sma_then_returns_right_sma_computation() -> None:
    """Test computing SMA values from time series with valid data using pandas."""
    dates = [
        datetime(2024, 1, 1, tzinfo=UTC),
        datetime(2024, 1, 2, tzinfo=UTC),
        datetime(2024, 1, 3, tzinfo=UTC),
        datetime(2024, 1, 4, tzinfo=UTC),
        datetime(2024, 1, 5, tzinfo=UTC),
        datetime(2024, 1, 6, tzinfo=UTC),
        datetime(2024, 1, 7, tzinfo=UTC),
    ]

    prices = [100.0, 102.0, 105.0, 103.0, 107.0, 110.0, 108.0]
    series = pd.Series(prices, index=dates)
    window = 3

    result = compute_sma_from_time_series(series, window)

    assert_that(result, has_length(5))  # 7-3+1 = 5
    assert_that(result.iloc[0], close_to(102.3333, 0.001))  # (100+102+105)/3
    assert_that(result.iloc[1], close_to(103.3333, 0.001))  # (102+105+103)/3
    assert_that(result.iloc[2], close_to(105.0, 0.001))  # (105+103+107)/3
    assert_that(result.iloc[3], close_to(106.6667, 0.001))  # (103+107+110)/3
    assert_that(result.iloc[4], close_to(108.3333, 0.001))  # (107+110+108)/3


def test_given_insufficient_data_when_compute_sma_then_returns_empty_series() -> None:
    """Test computing SMA values with insufficient data."""
    dates = [datetime(2024, 1, 1, tzinfo=UTC), datetime(2024, 1, 2, tzinfo=UTC)]
    prices = [100.0, 102.0]
    series = pd.Series(prices, index=dates)
    window = 3

    result = compute_sma_from_time_series(series, window)

    assert_that(result, has_length(0))


def test_given_invalid_window_when_compute_sma_then_returns_empty_series() -> None:
    """Test computing SMA values with zero or negative window."""
    dates = [datetime(2024, 1, 1, tzinfo=UTC), datetime(2024, 1, 2, tzinfo=UTC), datetime(2024, 1, 3, tzinfo=UTC)]

    prices = [100.0, 102.0, 105.0]
    series = pd.Series(prices, index=dates)

    result_zero = compute_sma_from_time_series(series, 0)
    assert_that(result_zero, has_length(0))

    result_negative = compute_sma_from_time_series(series, -5)
    assert_that(result_negative, has_length(0))


@pytest.mark.asyncio
async def test_given_right_input_when_compute_sma_then_returns_right_sma_calculation() -> None:
    """Test computing SMA with valid ticker."""
    result = await compute_sma(
        ticker="AAPL",
        lookback_period="1mo",
        interval="1d",
        window=20,
        source="close",
    )

    assert_that(result, is_(instance_of(TimeSeries)))
    time_series = cast("TimeSeries", result)

    assert_that(time_series.ticker, equal_to("AAPL"))
    assert_that(time_series.points, has_length(greater_than(0)))

    for data_point in time_series.points:
        assert_that(data_point.value, greater_than(0.0))


@pytest.mark.asyncio
async def test_given_large_window_when_compute_sma_then_return_error() -> None:
    """Test error when window is too large."""
    result = await compute_sma(
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
async def test_given_negative_window_when_compute_sma_then_returns_error() -> None:
    """Test computing SMA with negative window."""
    result = await compute_sma(
        ticker="AAPL",
        lookback_period="1mo",
        interval="1d",
        window=-5,
        source="close",
    )

    assert_that(result, instance_of(Error))


@pytest.mark.asyncio
async def test_given_zero_window_when_compute_sma_then_returns_error() -> None:
    """Test computing SMA with zero window."""
    result = await compute_sma(
        ticker="AAPL",
        lookback_period="1mo",
        interval="1d",
        window=0,
        source="close",
    )

    assert_that(result, instance_of(Error))
