"""Test TickerInformation model and parser."""

from typing import Any

import pytest
from hamcrest import assert_that, has_properties

from technical_analysis_mcp.models import parse_yfinance_ticker_information


def test_parse_yfinance_ticker_information_empty() -> None:
    """Test parsing an empty yfinance Ticker.info dictionary."""
    info: dict[str, Any] = {}

    with pytest.raises(ValueError, match="Field 'symbol' is missing"):
        parse_yfinance_ticker_information(info)


def test_parse_yfinance_ticker_information_partial() -> None:
    """Test parsing a partial yfinance Ticker.info dictionary."""
    info: dict[str, Any] = {
        "symbol": "AAPL",
        "shortName": "Apple Inc.",
        "longName": "Apple Inc.",
        "sector": "Technology",
        "marketCap": 3775801327616,
    }

    with pytest.raises(ValueError, match="Field 'industry' is missing"):
        parse_yfinance_ticker_information(info)


def test_parse_yfinance_ticker_information_full() -> None:
    """Test parsing a full yfinance Ticker.info dictionary."""
    info: dict[str, Any] = {
        "symbol": "AAPL",
        "shortName": "Apple Inc.",
        "longName": "Apple Inc.",
        "sector": "Technology",
        "industry": "Consumer Electronics",
        "marketCap": 3775801327616,
        "previousClose": 258.21,
        "regularMarketOpen": 257.88,
        "regularMarketPrice": 255.53,
        "regularMarketVolume": 70054453,
        "trailingPE": 34.25335,
        "forwardPE": 27.922901,
        "dividendYield": 0.41,
        "beta": 1.093,
        "fiftyTwoWeekHigh": 288.62,
        "fiftyTwoWeekLow": 169.21,
        "averageVolume": 46223512,
        "sharesOutstanding": 14697926000,
    }

    result = parse_yfinance_ticker_information(info)

    assert_that(
        result,
        has_properties(
            symbol="AAPL",
            short_name="Apple Inc.",
            long_name="Apple Inc.",
            sector="Technology",
            industry="Consumer Electronics",
            market_cap=3775801327616.0,
            previous_close=258.21,
            current_open=257.88,
            market_price=255.53,
            current_volume=70054453.0,
            trailing_pe=34.25335,
            forward_pe=27.922901,
            dividend_yield=0.41,
            beta=1.093,
            high_52w=288.62,
            low_52w=169.21,
            average_volume=46223512.0,
            shares_outstanding=14697926000.0,
        ),
    )


def test_parse_yfinance_ticker_information_invalid_types() -> None:
    """Test parsing a yfinance Ticker.info dictionary with invalid types."""
    info: dict[str, Any] = {
        "shortName": "Apple Inc.",
    }

    with pytest.raises(ValueError, match="Field 'symbol' is missing"):
        parse_yfinance_ticker_information(info)


def test_parse_yfinance_ticker_information_raises_type_error() -> None:
    """Test parsing a yfinance Ticker.info dictionary with invalid types that raise TypeError."""
    info: dict[str, Any] = {
        "symbol": 123,  # Invalid type
        "shortName": "Apple Inc.",
        "marketCap": "3775801327616",  # Invalid type
    }

    with pytest.raises(TypeError, match="Field 'symbol' is not a string"):
        parse_yfinance_ticker_information(info)
