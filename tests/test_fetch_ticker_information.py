"""Test fetch_ticker_information function."""

import pytest

from src.technical_analysis_mcp.tools import fetch_ticker_information


@pytest.mark.asyncio
async def test_fetch_ticker_information_success() -> None:
    """Test fetching ticker information for a valid ticker."""
    result = await fetch_ticker_information("AAPL")
    assert isinstance(result, dict)
    assert "error" not in result
    assert "symbol" in result


@pytest.mark.asyncio
async def test_fetch_ticker_information_failure() -> None:
    """Test fetching ticker information for an invalid ticker."""
    result = await fetch_ticker_information("INVALID_TICKER")
    assert isinstance(result, dict)
    assert result.get("symbol") is None

