# Agent Interaction Guide

This document outlines how AI agents can interact with the Technical Analysis
MCP server. It provides detailed information about the repository structure,
available tools, and best practices for working with the codebase.

## Repository Structure

```text
technical-analysis-mcp/
├── AGENT.md                    # Agent interaction guide
├── README.md                   # Project overview and setup instructions
├── pyproject.toml              # Project configuration and dependencies
├── poetry.lock                 # Dependency lock file
├── src/                        # Source code
│   ├── __init__.py             # Package initialization
│   ├── models/                 # Data models
│   │   └── __init__.py         # Models module initialization
│   ├── server/                 # MCP server implementation
│   │   ├── __init__.py         # Server module initialization
│   │   └── mcp_server.py       # MCP server implementation
│   └── tools/                  # Technical analysis tools
│       ├── __init__.py         # Tools module initialization
│       └── lookup_tool.py      # Lookup tool implementation
└── tests/                      # Unit and integration tests
    ├── __init__.py             # Tests module initialization
    ├── test_lookup_tool.py     # Lookup tool tests
    └── test_mcp_server.py      # MCP server tests
```

## Overview

The MCP server provides tools for fetching market, sector, industry, and ticker
data using `yfinance`. Agents can query these tools via the MCP protocol. The
server is built using `FastMCP` and supports multiple transport mechanisms
(stdio, HTTP, SSE).

## Supported Tools

### 1. Lookup Tool

**File**: `src/tools/lookup_tool.py`

**Purpose**: Fetch ticker information such as symbol, name, and sector.

**Example Query**:

```json
{
  "tool": "lookup",
  "query": "AAPL"
}
```

**Response**:

```json
{
  "symbol": "AAPL",
  "name": "Apple Inc.",
  "sector": "Technology"
}
```

**Error Handling**:

- If the ticker is invalid or empty, the tool raises a `ValueError`.
- If no data is found for the ticker, the tool raises a `ValueError`.

### 2. Market Tool (Planned)

**Purpose**: Fetch market data (e.g., indices, trends).

### 3. Sector Tool (Planned)

**Purpose**: Fetch sector-specific data.

### 4. Industry Tool (Planned)

**Purpose**: Fetch industry-specific data.

### 5. Calendars Tool (Planned)

**Purpose**: Fetch calendar events (e.g., earnings, dividends).

## Example Queries

### Lookup Ticker

```json
{
  "tool": "lookup",
  "query": "AAPL"
}
```

**Response**:

```json
{
  "symbol": "AAPL",
  "name": "Apple Inc.",
  "sector": "Technology"
}
```

### Invalid Ticker

```json
{
  "tool": "lookup",
  "query": ""
}
```

**Response**:

```json
{
  "error": "Ticker cannot be empty"
}
```

## Error Handling

- If a tool fails, the server will respond with an error message.
- Agents should handle retries or fallbacks gracefully.

### Example Error Response

```json
{
  "error": "Failed to fetch market data: Invalid ticker"
}
```

## Transport Mechanisms

- **stdio**: Direct communication via standard input/output.
- **HTTP**: RESTful API endpoints.
- **SSE**: Server-Sent Events for real-time updates.

## Authentication

The MCP server supports API key authentication. Agents must include the API key
in their requests.

### Example Authenticated Request

```json
{
  "tool": "lookup",
  "query": "AAPL",
  "api_key": "your-api-key"
}
```

## Best Practices

1. **Input Validation**: Always validate inputs before sending them to the
   server.
2. **Error Handling**: Handle errors gracefully and provide meaningful feedback
   to users.
3. **Rate Limiting**: Be mindful of rate limits when making multiple requests.
4. **Caching**: Cache responses to avoid redundant requests.

## Development

### Running Tests

To run the tests, use the following command:

```bash
poetry run pytest
```

### Formatting Code

To format the code, use the following command:

```bash
poetry run ruff src tests
```

### Starting the Server

To start the MCP server, use the following command:

```bash
poetry run technical-analysis-mcp
```

## Examples

### Python Example

```python
import requests

# Fetch ticker data
response = requests.post(
    "http://localhost:8000/query",
    json={
        "tool": "lookup",
        "query": "AAPL"
    }
)

print(response.json())
```

### JavaScript Example

```javascript
// Fetch ticker data
fetch("http://localhost:8000/query", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    tool: "lookup",
    query: "AAPL"
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## Additional Notes

- The repository uses `Poetry` for dependency management. Ensure you have Poetry
  installed and configured.
- The project is licensed under the MIT License. See the `README.md` file for
  more details.
- Contributions are welcome! Please open an issue or submit a pull request.

## Future Enhancements

- Implement additional tools (Market, Sector, Industry, Calendars).
- Add more detailed error handling and logging.
- Support for additional transport mechanisms.
- Enhance documentation and examples.
