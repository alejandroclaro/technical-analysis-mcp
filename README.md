# Technical Analysis MCP

A MCP (Modular Communication Protocol) server for providing technical analysis
tools to AI agents using `yfinance`.

## Goals

- Provide a modular and extensible MCP server for technical analysis.
- Integrate with `yfinance` to fetch market, sector, industry, and ticker data.
- Support multiple transport mechanisms (stdio, HTTP, SSE).

## Structure

```text
src/
├── server/  # MCP server implementation
├── tools/   # Technical analysis tools
└── models/  # Data models

tests/       # Unit and integration tests
```

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd technical-analysis-mcp
   ```

2. Install dependencies using Poetry:

   ```bash
   poetry install
   ```

## Usage

1. Start the MCP server:

   ```bash
   poetry run python -m src.server.mcp_server
   ```

2. Interact with the server using an MCP client or AI agent.

### Example Queries

#### Market Data

```json
{
  "tool": "market",
  "query": "^GSPC"
}
```

#### Sector Data

```json
{
  "tool": "sector",
  "query": "XLC"
}
```

#### Industry Data

```json
{
  "tool": "industry",
  "query": "AAPL"
}
```

#### Calendar Events

```json
{
  "tool": "calendars",
  "query": "AAPL"
}
```

#### Ticker Lookup

```json
{
  "tool": "lookup",
  "query": "AAPL"
}
```

## Authentication

The MCP server supports API key authentication. To enable authentication, pass
an API key when initializing the server:

```python
server = TechnicalAnalysisMCPServer(api_key="your-api-key")
```

## Development

- Run tests:

  ```bash
  poetry run pytest
  ```

- Format code:

  ```bash
  poetry run ruff src tests
  ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
