"""MCP server entry point."""

from typing import Any

from mcp.server.fastmcp import FastMCP

from .tools import fetch_stock_info

server = FastMCP("technical-analysis", dependencies=["yfinance>=1.0"])


@server.tool()
async def get_ticker_info(ticker: str) -> dict[str, Any]:
    """Get comprehensive ticker information.

    Args:
        ticker (str): The ticker name of company name.

    Returns:
        dict[strin, Any]: The ticker information.

    """
    return await fetch_stock_info(ticker)


def main() -> None:
    """Entry point for the server."""
    server.run(transport="stdio")


if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
