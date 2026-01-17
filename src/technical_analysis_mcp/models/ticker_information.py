"""Ticker Information Model."""

from typing import Any

from pydantic import BaseModel

from technical_analysis_mcp.utils import (
    get_dictionary_optional_float,
    get_dictionary_optional_string,
    get_dictionary_string,
)


class TickerInformation(BaseModel):
    """Structured model for ticker information."""

    symbol: str
    sector: str
    industry: str
    short_name: str
    long_name: str | None = None
    market_cap: float | None = None
    previous_close: float | None = None
    regular_market_open: float | None = None
    regular_market_price: float | None = None
    regular_market_volume: float | None = None
    trailing_pe: float | None = None
    forward_pe: float | None = None
    dividend_yield: float | None = None
    beta: float | None = None
    fifty_two_week_high: float | None = None
    fifty_two_week_low: float | None = None
    average_volume: float | None = None
    shares_outstanding: float | None = None


def parse_yfinance_ticker_information(info: dict[str, Any]) -> "TickerInformation":
    """Parse yfinance Ticker.info dictionary into a TickerInformation model.

    Args:
        info: The yfinance Ticker.info dictionary.

    Returns:
        The parsed TickerInformation model.

    Raises:
        ValueError: If any mandatory field is missing.
        TypeError: If any of the fields is not of the expected type.

    """
    symbol = get_dictionary_string(info, "symbol")
    sector = get_dictionary_string(info, "sector")
    industry = get_dictionary_string(info, "industry")
    short_name = get_dictionary_string(info, "shortName")

    ticker = TickerInformation(
        symbol=symbol,
        sector=sector,
        industry=industry,
        short_name=short_name,
    )

    ticker.long_name = get_dictionary_optional_string(info, "longName")
    ticker.market_cap = get_dictionary_optional_float(info, "marketCap")
    ticker.previous_close = get_dictionary_optional_float(info, "previousClose")
    ticker.regular_market_open = get_dictionary_optional_float(info, "regularMarketOpen")
    ticker.regular_market_price = get_dictionary_optional_float(info, "regularMarketPrice")
    ticker.regular_market_volume = get_dictionary_optional_float(info, "regularMarketVolume")
    ticker.trailing_pe = get_dictionary_optional_float(info, "trailingPE")
    ticker.forward_pe = get_dictionary_optional_float(info, "forwardPE")
    ticker.dividend_yield = get_dictionary_optional_float(info, "dividendYield")
    ticker.beta = get_dictionary_optional_float(info, "beta")
    ticker.fifty_two_week_high = get_dictionary_optional_float(info, "fiftyTwoWeekHigh")
    ticker.fifty_two_week_low = get_dictionary_optional_float(info, "fiftyTwoWeekLow")
    ticker.average_volume = get_dictionary_optional_float(info, "averageVolume")
    ticker.shares_outstanding = get_dictionary_optional_float(info, "sharesOutstanding")

    return ticker
