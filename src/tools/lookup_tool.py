# Lookup Tool

import yfinance as yf
from pydantic import BaseModel


class TickerData(BaseModel):
    """Structured output for ticker data."""

    symbol: str
    name: str
    sector: str


class LookupTool:
    """Tool for looking up tickers."""

    def __init__(self):
        """Initialize the tool instance."""
        pass

    def lookup_ticker(self, ticker: str) -> TickerData:
        """Lookup a ticker and return its information.

        Args:
            ticker: The ticker symbol (e.g., "AAPL").

        Returns:
            TickerData: Structured ticker data.

        Raises:
            ValueError: If the ticker is invalid or data fetch fails.
        """
        if not ticker:
            raise ValueError("Ticker cannot be empty")

        ticker_data = yf.Ticker(ticker)
        info = ticker_data.info

        if not info or "error" in info:
            raise ValueError(f"No data found for ticker: {ticker}")

        return TickerData(
            symbol=info.get("symbol", ""),
            name=info.get("longName", ""),
            sector=info.get("sector", ""),
        )
