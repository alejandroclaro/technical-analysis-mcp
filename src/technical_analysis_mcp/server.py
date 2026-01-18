"""MCP server entry point."""

from fastmcp.utilities.logging import get_logger
from mcp.server.fastmcp import FastMCP

from . import __version__
from .models import Error, TickerInformation
from .tools import fetch_ticker_information

server = FastMCP("technical-analysis", dependencies=["yfinance>=1.0"])


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


def main() -> None:
    """Entry point for the server."""
    logger = get_logger("fastmcp")
    logger.info("Starting technical analysis MCP Server v%s", __version__)
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
