"""Module for fetching asset price history."""

from datetime import datetime

import yfinance as yf

from technical_analysis_mcp.models import (
    AssetPriceHistory,
    Error,
    Interval,
    Period,
    Price,
)


async def fetch_asset_price_history(
    ticker: str,
    period: Period,
    interval: Interval,
) -> AssetPriceHistory | Error:
    """Fetch asset price history for a given ticker symbol.

    Args:
        ticker: The ticker symbol of the stock to get historical prices for, e.g., "AAPL".
        period: The time period for which to fetch historical data.
        interval: The interval between data points.

    Returns:
        The historical asset prices. If no data is found, an error is returned.
    """
    try:
        information = yf.Ticker(ticker)
        data = information.history(period=period, interval=interval)
        prices = []

        if data.empty:
            return Error(what=f"No historical data found for ticker: {ticker}")

        for index, row in data.iterrows():
            price = Price(
                date=datetime.fromisoformat(str(index)),
                open=float(row["Open"]),
                high=float(row["High"]),
                low=float(row["Low"]),
                close=float(row["Close"]),
                volume=int(row["Volume"]),
                dividends=float(row["Dividends"]),
                stock_splits=float(row["Stock Splits"]),
            )

            prices.append(price)

        return AssetPriceHistory(ticker=ticker, period=period, interval=interval, prices=prices)
    except (ValueError, TypeError, KeyError) as e:
        return Error(what=f"Error fetching historical data for ticker {ticker}: {e}")
