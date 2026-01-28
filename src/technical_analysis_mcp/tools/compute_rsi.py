"""Module for computing the Relative Strength Index (RSI)."""

from datetime import datetime

from technical_analysis_mcp.models import (
    DataPoint,
    Error,
    Interval,
    Period,
    Price,
    PriceSource,
    TimeSeries,
)

from .fetch_asset_price_history import fetch_asset_price_history


def extract_price_data(prices: list[Price], source: PriceSource) -> list[tuple[datetime, float]]:
    """Extract price data from Price objects based on the specified source.

    Args:
        prices: List of Price objects.
        source: Which price field to extract (open, high, low, close).

    Returns:
        List of tuples containing (datetime, price_value).
    """
    extracted_data: list[tuple[datetime, float]] = []

    for price in prices:
        if source == "open":
            extracted_data.append((price.date, price.open))
        elif source == "high":
            extracted_data.append((price.date, price.high))
        elif source == "low":
            extracted_data.append((price.date, price.low))
        else:  # "close"
            extracted_data.append((price.date, price.close))

    return extracted_data


def compute_price_deltas(prices: list[float]) -> list[float]:
    """Calculate price differences between consecutive periods.

    Args:
        prices: List of price values.

    Returns:
        List of price differences where the first element is 0.
    """
    if not prices:
        return []

    deltas = [0.0] * len(prices)

    for i in range(1, len(prices)):
        deltas[i] = prices[i] - prices[i - 1]

    return deltas


def separate_gains_losses(deltas: list[float]) -> tuple[list[float], list[float]]:
    """Separate price deltas into gains and losses.

    Args:
        deltas: List of price differences.

    Returns:
        Tuple of (gains, losses) where:
        - gains[i] = delta[i] if delta[i] > 0 else 0
        - losses[i] = abs(delta[i]) if delta[i] < 0 else 0
    """
    gains = [0.0] * len(deltas)
    losses = [0.0] * len(deltas)

    for i, delta in enumerate(deltas):
        if delta > 0:
            gains[i] = delta
        elif delta < 0:
            losses[i] = -delta

    return gains, losses


def compute_average_gain_loss(
    gains: list[float],
    losses: list[float],
    period: int,
) -> tuple[list[float], list[float]]:
    """Compute exponential moving averages of gains and losses.

    Args:
        gains: List of gain values.
        losses: List of loss values.
        period: RSI period for smoothing.

    Returns:
        Tuple of (average_gains, average_losses) lists.
    """
    n = len(gains)
    average_gains = [0.0] * n
    average_losses = [0.0] * n

    if n <= period:
        return average_gains, average_losses

    avg_gain = sum(gains[1 : period + 1]) / period
    avg_loss = sum(losses[1 : period + 1]) / period
    average_gains[period] = avg_gain
    average_losses[period] = avg_loss

    for i in range(period + 1, n):
        average_gains[i] = (average_gains[i - 1] * (period - 1) + gains[i]) / period
        average_losses[i] = (average_losses[i - 1] * (period - 1) + losses[i]) / period

    return average_gains, average_losses


def compute_rsi_values(
    average_gains: list[float],
    average_losses: list[float],
    period: int,
) -> list[float]:
    """Compute RSI values from average gains and losses.

    Args:
        average_gains: List of average gain values.
        average_losses: List of average loss values.
        period: RSI period.

    Returns:
        List of RSI values.
    """
    n = len(average_gains)
    rsi_values = [0.0] * n

    for i in range(period, n):
        avg_gain = average_gains[i]
        avg_loss = average_losses[i]

        if avg_loss == 0:
            rsi_values[i] = 100.0
        else:
            rs = avg_gain / avg_loss
            rsi_values[i] = 100 - (100 / (1 + rs))

    return rsi_values


async def compute_rsi(
    ticker: str,
    source: PriceSource,
    period: Period,
    interval: Interval,
    candles: int = 14,
) -> TimeSeries | Error:
    """Compute the Relative Strength Index (RSI) for a given ticker.

    Args:
        ticker: The ticker symbol (e.g., "AAPL").
        source: The price source to use.
        period: The time period for which to fetch historical data.
        interval: The interval between data points.
        candles: The number of candles/samples to calculate RSI (default 14).

    Returns:
        The indicator series.
    """
    if candles <= 0:
        return Error(what=f"RSI period must be positive, got: {candles}")

    history = await fetch_asset_price_history(ticker, period, interval)

    if isinstance(history, Error):
        return history

    if len(history.prices) <= candles:
        return Error(
            what=f"Insufficient data for RSI calculation. "
            f"Need at least {candles + 1} candles/samples. but got {len(history.prices)} points. Reason: "
            f"1) The period is too short for the interval, 2) or the interval is too big for the period. "
            f"Try a) increasing the period, b) reducing the interval, c) or reducing the number of RSI candles."
        )

    price_data = extract_price_data(history.prices, source)
    x = [date for date, _ in price_data]
    y = [value for _, value in price_data]
    deltas = compute_price_deltas(y)
    gains, losses = separate_gains_losses(deltas)
    average_gains, average_losses = compute_average_gain_loss(gains, losses, candles)
    rsi = compute_rsi_values(average_gains, average_losses, candles)

    result = [DataPoint(date=x[i], value=float(rsi[i])) for i in range(candles, len(rsi))]

    return TimeSeries(ticker=ticker, data_points=result)
