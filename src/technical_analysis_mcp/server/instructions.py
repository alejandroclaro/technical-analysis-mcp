"""Server Instructions."""

INSTRUCTIONS = (
    "The Technical Analysis MCP Server provides tools for fetching and computing "
    "technical analysis data for stocks and cryptocurrencies. It leverages free "
    "sources of information and mathematical calculations to provide robust tools "
    "and functions. The server includes a cache and local database to store "
    "previously fetched data, ensuring fast access to information without repeated "
    "internet requests. It also incorporates non-technical indicators like sentiment "
    "and other signals derived from free sources of information, giving you a "
    "comprehensive view of the market landscape. "
    "\n\n"
    "## General Information"
    "\n\n"
    "- The server provides structured responses to improve predictability and processing "
    "by LLMs.\n"
    "- Errors are returned as structured objects rather than raising exceptions.\n"
    "- Inputs are validated before processing and edge cases are handled gracefully."
)
