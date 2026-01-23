"""MCP server entry point."""

from fastmcp.utilities.logging import get_logger
from mcp.server.fastmcp import FastMCP

from technical_analysis_mcp.models import AssetPriceHistory, Error, Interval, Period, TickerInformation
from technical_analysis_mcp.tools import fetch_asset_price_history, fetch_ticker_information
from technical_analysis_mcp.version import __version__

from .instructions import INSTRUCTIONS

server = FastMCP(
    "technical-analysis",
    dependencies=["yfinance>=1.0"],
    instructions=INSTRUCTIONS,
)


@server.tool(structured_output=True)
async def get_ticker_information(ticker: str) -> TickerInformation | Error:
    """Get the ticker information.

    Retrieves detailed financial, metadata, and real-time descriptive
    information for a specific financial instrument or company.

    Use this tool when you need to identify a company's sector, industry,
    business summary, market cap, or to verify if a specific ticker symbol
    is valid. This tool serves as the primary "lookup" for background data
    before performing technical analysis or price checks.

    Args:
        ticker (str): The unique identifier for the asset.
                      Supports stock symbols (e.g., "AAPL", "TSLA"),
                      indices (e.g., "^GSPC"), and cryptocurrency
                      pairs (e.g., "BTC/USD" or "ETH-USD").

    Returns:
        TickerInformation | Error: The structured object containing
        comprehensive asset details or an error if the ticker is not found.

    """
    return await fetch_ticker_information(ticker)


@server.tool(structured_output=True)
async def get_asset_price_history(
    ticker: str,
    period: Period,
    interval: Interval,
) -> AssetPriceHistory | Error:
    """Get the historical price data for a financial asset.

    Retrieves comprehensive historical pricing information including open,
    high, low, close prices, trading volume, dividends, and stock splits
    for a specified financial instrument over a defined time period and
    interval.

    Use this tool when you need to perform technical analysis, charting,
    backtesting trading strategies, or analyzing historical price patterns.
    This tool provides the raw price data required for analyzing or
    calculating technical indicators, oscillators etc.

    However, prefer other tools that provide precomputed indicators,
    oscillators, etc, unless you need to the raw historical data.

    Args:
        ticker (str): The unique identifier for the asset.
                      Supports stock symbols (e.g., "AAPL", "TSLA"),
                      indices (e.g., "^GSPC"), and cryptocurrency
                      pairs (e.g., "BTC/USD" or "ETH-USD").
        period (str): The time range for historical data retrieval.
        interval (str): The frequency of data points.

    Returns:
        AssetPriceHistory | Error: The structured historical price data
        or an error if the ticker is invalid, no data is available,
        or parameters are invalid.

    """
    return await fetch_asset_price_history(ticker, period, interval)


def main() -> None:
    """Entry point for the server."""
    logger = get_logger("fastmcp")
    logger.info("Starting technical analysis MCP Server v%s", __version__)
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
