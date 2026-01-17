"""Test MCP Server."""

import pytest
from fastmcp import Client
from hamcrest import assert_that, is_

from src.technical_analysis_mcp.server import server


@pytest.mark.asyncio
async def test_server_runs() -> None:
    """Test the MCP server lifecycle."""
    async with Client(server) as client:
        assert_that(await client.ping(), is_(True))
