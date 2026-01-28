"""Module for computing Simple Moving Average (SMA)."""

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
        else:
            extracted_data.append((price.date, price.close))

    return extracted_data


def compute_sma_values(
    prices: list[float],
    period: int,
) -> list[float]:
    """Compute Simple Moving Average values.

    Args:
        prices: List of price values.
        period: The moving window period.

    Returns:
        List of SMA values.
    """
    if len(prices) < period or period <= 0:
        return []

    sma_values: list[float] = []

    for i in range(period - 1, len(prices)):
        window = prices[i - period + 1 : i + 1]
        sma = sum(window) / period
        sma_values.append(sma)

    return sma_values


async def compute_sma(
    ticker: str,
    source: PriceSource,
    period: Period,
    interval: Interval,
    window: int = 20,
) -> TimeSeries | Error:
    """Compute the Simple Moving Average (SMA) for a given ticker.

    Args:
        ticker: The ticker symbol (e.g., "AAPL").
        source: The price source to use.
        period: The time period for which to fetch historical data.
        interval: The interval between data points.
        window: The moving window period for SMA calculation (default 20).

    Returns:
        The indicator series.
    """
    if window <= 0:
        return Error(what=f"SMA window must be positive, got: {window}")

    history = await fetch_asset_price_history(ticker, period, interval)

    if isinstance(history, Error):
        return history

    if len(history.prices) < window:
        return Error(
            what=f"Insufficient data for SMA calculation. "
            f"Need at least {window} candles/samples, but got {len(history.prices)} points. Reason: "
            f"1) The period is too short for the interval, 2) or the interval is too big for the period. "
            f"Try a) increasing the period, b) reducing the interval, c) or reducing the SMA window."
        )

    price_data = extract_price_data(history.prices, source)
    dates = [date for date, _ in price_data]
    values = [value for _, value in price_data]
    sma_values = compute_sma_values(values, window)

    result = [DataPoint(date=dates[i + window - 1], value=float(sma_values[i])) for i in range(len(sma_values))]

    return TimeSeries(ticker=ticker, data_points=result)
