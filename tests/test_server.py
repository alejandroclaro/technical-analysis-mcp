"""Test MCP Server."""

import pytest

from src.technical_analysis_mcp.server import server


@pytest.mark.asyncio
async def test_server_lifecycle() -> None:
    """Test the MCP server lifecycle."""
    async with server._mcp_server.lifespan(server._mcp_server):  # noqa: SLF001  # type: ignore[attr-defined]
        ...
