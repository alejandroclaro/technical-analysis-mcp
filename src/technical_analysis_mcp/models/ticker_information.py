"""Ticker Information Model."""

from typing import Any

from pydantic import BaseModel, Field

from technical_analysis_mcp.utils import (
    get_dictionary_optional_float,
    get_dictionary_optional_string,
    get_dictionary_string,
)

SYMBOL_DESCRIPTION = "The ticker symbol or unique identifier for the financial instrument or company."
SECTOR_DESCRIPTION = "The sector to which the financial instrument or company belongs."
INDUSTRY_DESCRIPTION = "The industry to which the financial instrument or company belongs."
SHORT_NAME_DESCRIPTION = "The short name or abbreviation of the financial instrument or company."
LONG_NAME_DESCRIPTION = "The full name of the financial instrument or company."
MARKET_CAP_DESCRIPTION = "The market capitalization of the financial instrument or company."
PREVIOUS_CLOSE_DESCRIPTION = "The previous closing price of the financial instrument."
REGULAR_MARKET_OPEN_DESCRIPTION = "The opening price of the financial instrument in the regular market."
REGULAR_MARKET_PRICE_DESCRIPTION = "The current price of the financial instrument in the regular market."
REGULAR_MARKET_VOLUME_DESCRIPTION = "The trading volume of the financial instrument in the regular market."
TRAILING_PE_DESCRIPTION = "The trailing price-to-earnings ratio of the financial instrument."
FORWARD_PE_DESCRIPTION = "The forward price-to-earnings ratio of the financial instrument."
DIVIDEND_YIELD_DESCRIPTION = "The dividend yield of the financial instrument."
BETA_DESCRIPTION = "The beta value of the financial instrument, indicating its volatility relative to the market."
FIFTY_TWO_WEEK_HIGH_DESCRIPTION = "The highest price of the financial instrument over the past 52 weeks."
FIFTY_TWO_WEEK_LOW_DESCRIPTION = "The lowest price of the financial instrument over the past 52 weeks."
AVERAGE_VOLUME_DESCRIPTION = "The average trading volume of the financial instrument."
SHARES_OUTSTANDING_DESCRIPTION = "The number of outstanding shares of the financial instrument."


class TickerInformation(BaseModel):
    """Structured model for ticker information."""

    symbol: str = Field(..., description=SYMBOL_DESCRIPTION)
    sector: str = Field(..., description=SECTOR_DESCRIPTION)
    industry: str = Field(..., description=INDUSTRY_DESCRIPTION)
    short_name: str = Field(..., description=SHORT_NAME_DESCRIPTION)
    long_name: str | None = Field(None, description=LONG_NAME_DESCRIPTION)
    market_cap: float | None = Field(None, description=MARKET_CAP_DESCRIPTION)
    previous_close: float | None = Field(None, description=PREVIOUS_CLOSE_DESCRIPTION)
    regular_market_open: float | None = Field(None, description=REGULAR_MARKET_OPEN_DESCRIPTION)
    regular_market_price: float | None = Field(None, description=REGULAR_MARKET_PRICE_DESCRIPTION)
    regular_market_volume: float | None = Field(None, description=REGULAR_MARKET_VOLUME_DESCRIPTION)
    trailing_pe: float | None = Field(None, description=TRAILING_PE_DESCRIPTION)
    forward_pe: float | None = Field(None, description=FORWARD_PE_DESCRIPTION)
    dividend_yield: float | None = Field(None, description=DIVIDEND_YIELD_DESCRIPTION)
    beta: float | None = Field(None, description=BETA_DESCRIPTION)
    fifty_two_week_high: float | None = Field(None, description=FIFTY_TWO_WEEK_HIGH_DESCRIPTION)
    fifty_two_week_low: float | None = Field(None, description=FIFTY_TWO_WEEK_LOW_DESCRIPTION)
    average_volume: float | None = Field(None, description=AVERAGE_VOLUME_DESCRIPTION)
    shares_outstanding: float | None = Field(None, description=SHARES_OUTSTANDING_DESCRIPTION)


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
        regular_market_open=get_dictionary_optional_float(info, "regularMarketOpen"),
        regular_market_price=get_dictionary_optional_float(info, "regularMarketPrice"),
        regular_market_volume=get_dictionary_optional_float(info, "regularMarketVolume"),
        trailing_pe=get_dictionary_optional_float(info, "trailingPE"),
        forward_pe=get_dictionary_optional_float(info, "forwardPE"),
        dividend_yield=get_dictionary_optional_float(info, "dividendYield"),
        beta=get_dictionary_optional_float(info, "beta"),
        fifty_two_week_high=get_dictionary_optional_float(info, "fiftyTwoWeekHigh"),
        fifty_two_week_low=get_dictionary_optional_float(info, "fiftyTwoWeekLow"),
        average_volume=get_dictionary_optional_float(info, "averageVolume"),
        shares_outstanding=get_dictionary_optional_float(info, "sharesOutstanding"),
    )
