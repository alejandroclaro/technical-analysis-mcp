# Test MCP Server

import pytest
from src.server.mcp_server import TechnicalAnalysisMCPServer


@pytest.mark.asyncio
async def test_server_lifecycle():
    """Test the MCP server lifecycle."""
    server = TechnicalAnalysisMCPServer()
    await server.on_start()
    await server.on_stop()
