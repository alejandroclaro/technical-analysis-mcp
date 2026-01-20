"""Ticker Information Model."""

from typing import Any

from pydantic import BaseModel, Field

from technical_analysis_mcp.helpers import (
    get_dictionary_optional_float,
    get_dictionary_optional_string,
    get_dictionary_string,
)

_DESCRIPTIONS = {
    "symbol": "Ticker symbol",
    "sector": "Business sector",
    "industry": "Business industry",
    "short_name": "Short name",
    "long_name": "Full legal name",
    "market_cap": "Market capitalization",
    "previous_close": "Previous closing price",
    "current_open": "Regular market opening price",
    "market_price": "Current market price",
    "current_volume": "Current trading volume",
    "trailing_pe": "Trailing price-to-earnings ratio",
    "forward_pe": "Forward price-to-earnings ratio",
    "dividend_yield": "Dividend yield percentage",
    "beta": "Beta (market volatility indicator)",
    "high_52w": "52-week high price",
    "low_52w": "52-week low price",
    "average_volume": "Average trading volume",
    "shares_outstanding": "Number of outstanding shares",
}


class TickerInformation(BaseModel):
    """Structured model for ticker information."""

    symbol: str = Field(..., description=_DESCRIPTIONS["symbol"])
    sector: str = Field(..., description=_DESCRIPTIONS["sector"])
    industry: str = Field(..., description=_DESCRIPTIONS["industry"])
    short_name: str = Field(..., description=_DESCRIPTIONS["short_name"])
    long_name: str | None = Field(None, description=_DESCRIPTIONS["long_name"])
    market_cap: float | None = Field(None, description=_DESCRIPTIONS["market_cap"])
    previous_close: float | None = Field(None, description=_DESCRIPTIONS["previous_close"])
    current_open: float | None = Field(None, description=_DESCRIPTIONS["current_open"])
    market_price: float | None = Field(None, description=_DESCRIPTIONS["market_price"])
    current_volume: float | None = Field(None, description=_DESCRIPTIONS["current_volume"])
    trailing_pe: float | None = Field(None, description=_DESCRIPTIONS["trailing_pe"])
    forward_pe: float | None = Field(None, description=_DESCRIPTIONS["forward_pe"])
    dividend_yield: float | None = Field(None, description=_DESCRIPTIONS["dividend_yield"])
    beta: float | None = Field(None, description=_DESCRIPTIONS["beta"])
    high_52w: float | None = Field(None, description=_DESCRIPTIONS["high_52w"])
    low_52w: float | None = Field(None, description=_DESCRIPTIONS["low_52w"])
    average_volume: float | None = Field(None, description=_DESCRIPTIONS["average_volume"])
    shares_outstanding: float | None = Field(None, description=_DESCRIPTIONS["shares_outstanding"])


def parse_yfinance_ticker_information(info: dict[str, Any]) -> TickerInformation:
    """Parse yfinance Ticker.info dictionary into a TickerInformation model.

    Args:
        info: The yfinance Ticker.info dictionary.

    Returns:
        The parsed TickerInformation model.

    Raises:
        ValueError: If any mandatory field is missing.
        TypeError: If any of the fields is not of the expected type.

    """
    return TickerInformation(
        symbol=get_dictionary_string(info, "symbol"),
        sector=get_dictionary_string(info, "sector"),
        industry=get_dictionary_string(info, "industry"),
        short_name=get_dictionary_string(info, "shortName"),
        long_name=get_dictionary_optional_string(info, "longName"),
        market_cap=get_dictionary_optional_float(info, "marketCap"),
        previous_close=get_dictionary_optional_float(info, "previousClose"),
        current_open=get_dictionary_optional_float(info, "regularMarketOpen"),
        market_price=get_dictionary_optional_float(info, "regularMarketPrice"),
        current_volume=get_dictionary_optional_float(info, "regularMarketVolume"),
        trailing_pe=get_dictionary_optional_float(info, "trailingPE"),
        forward_pe=get_dictionary_optional_float(info, "forwardPE"),
        dividend_yield=get_dictionary_optional_float(info, "dividendYield"),
        beta=get_dictionary_optional_float(info, "beta"),
        high_52w=get_dictionary_optional_float(info, "fiftyTwoWeekHigh"),
        low_52w=get_dictionary_optional_float(info, "fiftyTwoWeekLow"),
        average_volume=get_dictionary_optional_float(info, "averageVolume"),
        shares_outstanding=get_dictionary_optional_float(info, "sharesOutstanding"),
    )
