"""Test module for the compute_rsi tool."""

from datetime import UTC, datetime
from typing import cast

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

from technical_analysis_mcp.models import Price, TimeSeries
from technical_analysis_mcp.tools.compute_rsi import (
    compute_average_gain_loss,
    compute_price_deltas,
    compute_rsi,
    compute_rsi_values,
    extract_price_data,
    separate_gains_losses,
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
    assert_that(result[0][0], equal_to(prices[0].date))
    assert_that(result[0][1], equal_to(102.0))
    assert_that(result[1][0], equal_to(prices[1].date))
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


def test_should_compute_price_deltas_when_prices_given() -> None:
    """Test calculating price deltas."""
    prices = [100.0, 102.0, 105.0, 103.0, 107.0]

    result = compute_price_deltas(prices)

    assert_that(result, has_length(5))
    assert_that(result[0], equal_to(0.0))  # First delta is 0
    assert_that(result[1], equal_to(2.0))  # 102 - 100
    assert_that(result[2], equal_to(3.0))  # 105 - 102
    assert_that(result[3], equal_to(-2.0))  # 103 - 105
    assert_that(result[4], equal_to(4.0))  # 107 - 103


def test_should_compute_price_deltas_when_single_price_given() -> None:
    """Test calculating price deltas with single price."""
    prices = [100.0]

    result = compute_price_deltas(prices)

    assert_that(result, has_length(1))
    assert_that(result[0], equal_to(0.0))


def test_should_compute_price_deltas_when_empty_list_given() -> None:
    """Test calculating price deltas with empty list."""
    prices: list[float] = []

    result = compute_price_deltas(prices)

    assert_that(result, has_length(0))


def test_should_separate_gains_losses_when_deltas_given() -> None:
    """Test separating gains and losses."""
    deltas = [0.0, 2.0, 3.0, -2.0, 4.0, -1.0]

    gains, losses = separate_gains_losses(deltas)

    assert_that(gains, has_length(6))
    assert_that(losses, has_length(6))
    assert_that(gains, equal_to([0.0, 2.0, 3.0, 0.0, 4.0, 0.0]))
    assert_that(losses, equal_to([0.0, 0.0, 0.0, 2.0, 0.0, 1.0]))


def test_should_separate_gains_losses_when_all_positive_given() -> None:
    """Test separating gains and losses with all positive deltas."""
    deltas = [0.0, 1.0, 2.0, 3.0]

    gains, losses = separate_gains_losses(deltas)

    assert_that(gains, equal_to([0.0, 1.0, 2.0, 3.0]))
    assert_that(losses, equal_to([0.0, 0.0, 0.0, 0.0]))


def test_should_separate_gains_losses_when_all_negative_given() -> None:
    """Test separating gains and losses with all negative deltas."""
    deltas = [0.0, -1.0, -2.0, -3.0]

    gains, losses = separate_gains_losses(deltas)

    assert_that(gains, equal_to([0.0, 0.0, 0.0, 0.0]))
    assert_that(losses, equal_to([0.0, 1.0, 2.0, 3.0]))


def test_should_compute_average_gain_loss_when_period_2_given() -> None:
    """Test calculating average gain and loss with period 2."""
    gains = [0.0, 2.0, 3.0, 0.0, 4.0, 0.0]
    losses = [0.0, 0.0, 0.0, 2.0, 0.0, 1.0]
    period = 2

    avg_gains, avg_losses = compute_average_gain_loss(gains, losses, period)

    assert_that(avg_gains, has_length(6))
    assert_that(avg_losses, has_length(6))

    assert_that(avg_gains[0], equal_to(0.0))
    assert_that(avg_gains[1], equal_to(0.0))
    assert_that(avg_losses[0], equal_to(0.0))
    assert_that(avg_losses[1], equal_to(0.0))
    assert_that(avg_gains[2], close_to(2.5, 0.001))
    assert_that(avg_gains[3], close_to(1.25, 0.001))
    assert_that(avg_gains[4], close_to(2.625, 0.001))
    assert_that(avg_gains[5], close_to(1.3125, 0.001))
    assert_that(avg_losses[2], equal_to(0.0))
    assert_that(avg_losses[3], close_to(1.0, 0.001))
    assert_that(avg_losses[4], close_to(0.5, 0.001))
    assert_that(avg_losses[5], close_to(0.75, 0.001))


def test_should_compute_average_gain_loss_when_period_3_given() -> None:
    """Test calculating average gain and loss with period 3."""
    gains = [0.0, 2.0, 3.0, 1.0, 4.0]
    losses = [0.0, 0.0, 0.0, 2.0, 1.0]
    period = 3

    avg_gains, avg_losses = compute_average_gain_loss(gains, losses, period)

    assert_that(avg_gains[3], close_to(2.0, 0.001))
    assert_that(avg_gains[4], close_to(2.6667, 0.001))
    assert_that(avg_losses[3], close_to(0.6667, 0.001))


def test_should_compute_rsi_values_when_averages_given() -> None:
    """Test calculating RSI values from average gains and losses."""
    avg_gains = [0.0, 0.0, 0.0, 1.25, 2.625, 1.3125]
    avg_losses = [0.0, 0.0, 0.0, 1.0, 0.5, 0.75]
    period = 2

    rsi_values = compute_rsi_values(avg_gains, avg_losses, period)

    assert_that(rsi_values, has_length(6))
    assert_that(rsi_values[0], equal_to(0.0))
    assert_that(rsi_values[1], equal_to(0.0))
    assert_that(rsi_values[2], close_to(100.0, 0.001))
    assert_that(rsi_values[3], close_to(55.5556, 0.001))
    assert_that(rsi_values[4], close_to(84.0, 0.001))
    assert_that(rsi_values[5], close_to(63.6364, 0.001))


def test_should_compute_rsi_values_when_zero_average_loss_given() -> None:
    """Test calculating RSI when average loss is zero."""
    avg_gains = [0.0, 0.0, 0.0, 2.5, 1.25]
    avg_losses = [0.0, 0.0, 0.0, 0.0, 0.0]
    period = 2

    rsi_values = compute_rsi_values(avg_gains, avg_losses, period)

    assert_that(rsi_values[3], close_to(100.0, 0.001))
    assert_that(rsi_values[4], close_to(100.0, 0.001))


def test_should_compute_rsi_values_when_zero_average_gain_given() -> None:
    """Test calculating RSI when average gain is zero."""
    avg_gains = [0.0, 0.0, 0.0, 0.0, 0.0]
    avg_losses = [0.0, 0.0, 0.0, 2.0, 1.0]
    period = 2

    rsi_values = compute_rsi_values(avg_gains, avg_losses, period)

    assert_that(rsi_values[3], close_to(0.0, 0.001))
    assert_that(rsi_values[4], close_to(0.0, 0.001))


def test_should_compute_rsi_values_when_both_averages_zero_given() -> None:
    """Test calculating RSI when both averages are zero."""
    avg_gains = [0.0, 0.0, 0.0, 0.0, 0.0]
    avg_losses = [0.0, 0.0, 0.0, 0.0, 0.0]
    period = 2

    rsi_values = compute_rsi_values(avg_gains, avg_losses, period)

    assert_that(rsi_values[3], close_to(100.0, 0.001))
    assert_that(rsi_values[4], close_to(100.0, 0.001))


@pytest.mark.asyncio
async def test_should_compute_rsi_when_valid_ticker_given() -> None:
    """Test computing RSI with valid ticker."""
    result = await compute_rsi(
        ticker="AAPL",
        source="close",
        period="1mo",
        interval="1d",
        candles=14,
    )

    assert_that(result, is_(instance_of(TimeSeries)))
    time_series = cast("TimeSeries", result)

    assert_that(time_series.ticker, equal_to("AAPL"))
    assert_that(time_series.data_points, has_length(greater_than(0)))

    for data_point in time_series.data_points:
        assert_that(data_point.value, all_of(greater_than_or_equal_to(0), less_than_or_equal_to(100)))
