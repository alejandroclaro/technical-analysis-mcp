"""Ticker information tools."""

import yfinance as yf

from technical_analysis_mcp.models import (
    Error,
    TickerInformation,
    parse_yfinance_ticker_information,
)


async def fetch_ticker_information(ticker: str) -> TickerInformation | Error:
    """Fetch comprehensive ticker information.

    Args:
        ticker: The ticker symbol (e.g., 'AAPL', 'MSFT', 'GOOGL')

    Returns:
        The ticker basic information in a structured format.

    """
    try:
        information = yf.Ticker(ticker)
        isin = information.get_isin()

        if (isin is None) or (isin == "-"):
            return Error(what=f"Company ticker {ticker} not found.")

        result = parse_yfinance_ticker_information(information.info)
    except (ValueError, TypeError) as e:
        return Error(what=f"Error: getting stock information for {ticker}: {e}")

    return result
