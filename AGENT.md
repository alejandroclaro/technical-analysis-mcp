# Agent Interaction Guide

This document outlines how AI agents can interact with the Technical Analysis
MCP server.

## Overview

The MCP server provides tools for fetching market, sector, industry, and ticker
data using `yfinance`. Agents can query these tools via the MCP protocol.

## Supported Tools

1. **Market Tool**: Fetch market data (e.g., indices, trends).
2. **Sector Tool**: Fetch sector-specific data.
3. **Industry Tool**: Fetch industry-specific data.
4. **Calendars Tool**: Fetch calendar events (e.g., earnings, dividends).
5. **Lookup Tool**: Search for tickers.

## Example Queries

### Market Data

```json
{
  "tool": "market",
  "query": "^GSPC"
}
```

**Response**:

```json
{
  "symbol": "^GSPC",
  "price": 4500.0,
  "volume": 1000000
}
```

### Sector Data

```json
{
  "tool": "sector",
  "query": "XLC"
}
```

**Response**:

```json
{
  "symbol": "XLC",
  "sector": "Communication Services",
  "industry": "Telecom Services"
}
```

### Industry Data

```json
{
  "tool": "industry",
  "query": "AAPL"
}
```

**Response**:

```json
{
  "symbol": "AAPL",
  "industry": "Technology",
  "description": "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide."
}
```

### Calendar Events

```json
{
  "tool": "calendars",
  "query": "AAPL"
}
```

**Response**:

```json
[
  {
    "date": "2023-10-01",
    "event": "Earnings Release"
  },
  {
    "date": "2023-11-01",
    "event": "Dividend Payment"
  }
]
```

### Ticker Lookup

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
  "tool": "market",
  "query": "^GSPC",
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

## Examples

### Python Example

```python
import requests

# Fetch market data
response = requests.post(
    "http://localhost:8000/query",
    json={
        "tool": "market",
        "query": "^GSPC"
    }
)

print(response.json())
```

### JavaScript Example

```javascript
// Fetch market data
fetch("http://localhost:8000/query", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    tool: "market",
    query: "^GSPC"
  })
})
.then(response => response.json())
.then(data => console.log(data));
```
