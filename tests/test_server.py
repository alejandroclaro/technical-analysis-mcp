"""Test MCP Server."""

import pytest
from fastmcp import Client

from src.technical_analysis_mcp.server import server


@pytest.mark.asyncio
async def test_server_runs() -> None:
    """Test the MCP server lifecycle."""
    async with Client(server) as client:
       assert await client.ping()
