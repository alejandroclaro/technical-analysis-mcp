"""Module for computing the Relative Strength Index (RSI)."""

from datetime import datetime
from typing import cast

import numpy as np
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


def compute_rsi_from_time_series(
    series: pd.Series,
    window: int,
) -> pd.Series:
    """Compute RSI values using pandas Series.

    Args:
        series: The pandas series with price values and datetime index.
        window: The RSI window period.

    Returns:
        The pandas Series of RSI values.

    """
    if len(series) < window + 1 or window <= 0:
        return pd.Series(dtype=float)

    deltas = series.diff()
    gains = deltas.clip(lower=0)
    losses = -deltas.clip(upper=0)
    avg_gains = np.full(len(series), np.nan)
    avg_losses = np.full(len(series), np.nan)

    avg_gains[window] = gains.iloc[1 : window + 1].mean()
    avg_losses[window] = losses.iloc[1 : window + 1].mean()

    for i in range(window + 1, len(series)):
        avg_gains[i] = (avg_gains[i - 1] * (window - 1) + gains.iloc[i]) / window
        avg_losses[i] = (avg_losses[i - 1] * (window - 1) + losses.iloc[i]) / window

    avg_gain_series = pd.Series(avg_gains, index=series.index)
    avg_loss_series = pd.Series(avg_losses, index=series.index)

    rs = avg_gain_series / avg_loss_series
    rsi = cast("pd.Series", 100 - (100 / (1 + rs)))
    rsi = rsi.fillna(50.0)

    return rsi.iloc[window:]


async def compute_rsi(
    ticker: str,
    period: Period,
    interval: Interval,
    window: int = 14,
    source: PriceSource = "close",
) -> TimeSeries | Error:
    """Compute the Relative Strength Index (RSI) for a given ticker.

    Args:
        ticker: The ticker symbol (e.g., "AAPL").
        period: The time period for which to fetch historical data.
        interval: The interval between data points.
        window: The number of candles/samples to calculate RSI (default 14).
        source: The price source to use.

    Returns:
        The indicator series.
    """
    if window <= 0:
        return Error(what=f"The RSI window must be positive, got: {window}")

    history = await fetch_asset_price_history(ticker, period, interval)

    if isinstance(history, Error):
        return history

    if len(history.prices) <= window:
        return Error(
            what=f"Insufficient data for RSI calculation. "
            f"Need at least {window + 1} candles/samples. but got {len(history.prices)} points. Reason: "
            f"1) The period is too short for the interval, 2) or the interval is too big for the period. "
            f"Try a) increasing the period, b) reducing the interval, c) or reducing the number of RSI candles."
        )

    price_series = get_price_series(history, source)
    rsi_series = compute_rsi_from_time_series(price_series, window)

    data_points = []
    for date, value in rsi_series.items():
        if isinstance(date, datetime):
            data_points.append(DataPoint(date=date, value=float(value)))

    return TimeSeries(ticker=ticker, points=data_points)
