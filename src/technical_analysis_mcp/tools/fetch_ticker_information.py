"""Ticker information tools."""

from typing import Any

import yfinance as yf


async def fetch_ticker_information(ticker: str) -> dict[str, Any]:
    """Fetch comprehensive ticker information.

    Args:
        ticker: The ticker symbol (e.g., 'AAPL', 'MSFT', 'GOOGL')

    Returns:
        - Stock Price & Trading Information,
        - Company Information,
        - Financial Metrics,
        - Earnings & Revenue,
        - Margins & Returns,
        - Dividends,
        - Balance Sheet,
        - Ownership,
        - Analyst Coverage,
        - Risk Metrics,
        - Other.

    """
    try:
        result = yf.Ticker(ticker)

        if result.isin is None:
            return {
                "error": f"Company ticker {ticker} not found.",
            }
    except Exception:  # noqa: BLE001
        return {
            "error": f"Error: getting stock information for {ticker}",
        }

    return result.info
