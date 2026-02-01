"""Module for computing Simple Moving Average (SMA)."""

from datetime import datetime
from typing import cast

import pandas as pd

from technical_analysis_mcp.models import (
    DataPoint,
    Error,
    Interval,
    Period,
    PriceSource,
    TimeSeries,
    get_price_series,
)

from .fetch_asset_price_history import fetch_asset_price_history


def compute_sma_from_time_series(
    series: pd.Series,
    window: int,
) -> pd.Series:
    """Compute Simple Moving Average values using pandas.

    Args:
        series: The pandas series with price values and datetime index.
        window: The moving window period.

    Returns:
        The pandas Series of SMA values.

    """
    if len(series) < window or window <= 0:
        return pd.Series(dtype=float)

    mean = cast("pd.Series", series.rolling(window=window).mean())

    return mean.dropna()


async def compute_sma(
    ticker: str,
    period: Period,
    interval: Interval,
    window: int = 20,
    source: PriceSource = "close",
) -> TimeSeries | Error:
    """Compute the Simple Moving Average (SMA) for a given ticker.

    Args:
        ticker: The ticker symbol (e.g., "AAPL").
        period: The time period for which to fetch historical data.
        interval: The interval between data points.
        window: The moving window period for SMA calculation (default 20).
        source: The price source to use.

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

    price_series = get_price_series(history, source)
    sma = compute_sma_from_time_series(price_series, window)
    data_points = []

    for date, value in sma.items():
        if isinstance(date, datetime):
            data_points.append(DataPoint(date=date, value=float(value)))

    return TimeSeries(ticker=ticker, points=data_points)
