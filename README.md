# Technical analysis MCP server

[![CI](https://img.shields.io/github/actions/workflow/status/alejandroclaro/technical-analysis-mcp/ci.yml?logo=github&style=flat-square)](https://github.com/alejandroclaro/technical-analysis-mcp/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/codecov/c/github/alejandroclaro/technical-analysis-mcp?style=flat-square)](https://app.codecov.io/gh/alejandroclaro/technical-analysis-mcp)
![Python](https://img.shields.io/badge/python-3.12%2B-007ec6?style=flat-square)
[![Stars](https://img.shields.io/github/stars/alejandroclaro/technical-analysis-mcp?color=007ec6&style=flat-square)](https://github.com/alejandroclaro/technical-analysis-mcp/stargazers)
![License](https://img.shields.io/badge/license-MIT-007ec6?style=flat-square)

## :telescope: Overview

The Technical Analysis MCP Server is a cutting-edge project designed to provide
powerful tools for fetching and computing technical-analysis data for stocks
and cryptocurrencies.

## :pushpin: Purpose

Unlike other MCPs and costly services like Alpha Vantage, this project offers a
complete and robust solution that leverages free sources of information and
mathematical calculations to provide top-notch tools and functions without the
hefty price tag.

It doesn't stop there. This project includes a cache and local database to
store previously fetched data, ensuring lightning-fast access to information
without repeated internet requests. This means you get the data you need, when
you need it, without the wait or hitting rate limits.

And that's not all. We're also incorporating non-technical indicators like
sentiment and other signals derived from free sources of information, giving
you a comprehensive view of the market landscape.

## :sparkles: Features

- **Comprehensive Data Fetching**: Retrieve detailed financial, and real-time
  descriptive information for specific financial instruments or companies.
- **Local Database and Cache**: Store previously fetched data locally to avoid
  repeated internet requests.
- **Modular Design**: Organized into modular tools.
- **Structured Data**: Uses structured responses to improve predictability and
  processing by LLMs.
- **Error Handling**: Errors are returned as structured objects rather than
  raising exceptions.
- **Type Hints**: Extensive use of type hints for better LLMs understanding
  and processing.
- **Input Validation**: Validates inputs before processing and handles edge
  cases gracefully.
- **Sentiment and Signal Analysis**: Incorporate non-technical indicators like
  sentiment and other signals derived from free sources of information.

## :rocket: Getting started

You can use this MCP server in your client via uv, or local
development.

### Via uv

```json
{
  "mcpServers": {
    "ta": {
      "command": "uvx",
      "args": ["technical-analysis-mcp"]
    }
  }
}
```

### Local development

```json
{
  "mcpServers": {
    "ta": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/Technical-analysis-mcp",
        "server"
      ]
    }
  }
}
```

## :chart_with_upwards_trend: MCP Tools Available

The following tools are available in this MCP server:

<!-- markdownlint-disable MD013 -->
| Tool Name | Description |
| :-------- | :---------- |
| `get_ticker_information` | Retrieves detailed financial, metadata, and real-time descriptive information for a specific financial instrument or company. |
| `get_asset_price_history` | Fetches comprehensive historical pricing information including OHLC prices, volume, dividends, and stock splits. |
| `get_sma` | Computes the Simple Moving Average (SMA) technical indicator for trend analysis and support/resistance levels. |
| `get_rsi` | Computes the Relative Strength Index (RSI) momentum oscillator for identifying overbought/oversold conditions. |
<!-- markdownlint-enable MD013 -->

## :computer: Interactive REPL

This project includes a REPL (Read-Eval-Print Loop) client that allows you to
interact directly with the MCP server for testing and exploration.

### Starting the REPL

```bash
uv run repl
```

Once started, you'll see a prompt: `mcp>`

### Basic REPL commands

- `help` or `?` - List all available commands
- `get_instructions` - View server instructions and capabilities
- `list_tools` - Display all available MCP tools
- `get_tool_description <tool_name>` - Get detailed information about a
  specific tool
- `call_tool <tool_name> <json_args>` - Execute a tool with arguments
- `history` - Show command history
- `exit`, `quit`, or `Ctrl+D` - Exit the REPL

### Example usage

```bash
mcp> list_tools
- get_ticker_information
- get_asset_price_history
- get_sma
- get_rsi

mcp> call_tool get_ticker_information '{"ticker": "AAPL"}'
{"symbol": "AAPL", "name": "Apple Inc.", ...}
```

## :white_check_mark: Implementation Status

### ✅ Implemention state

- Core data fetching tools:
  - [X] Ticker information retrieval (company details, sector, market cap, etc.)
  - [X] Historical price data (OHLC, volume, dividends, splits)
- Trend indicators**
  - [X] SMA (Simple Moving Average)
  - [ ] EMA (Exponential Moving Average)
  - [ ] WMA (Weighted Moving Average)
  - [ ] DEMA (Double Exponential Moving Average)
  - [ ] TEMA (Triple Exponential Moving Average)
  - [ ] TRIMA (Triangular Moving Average)
  - [ ] KAMA (Kaufman Adaptive Moving Average)
  - [ ] T3 (Triple Exponential Moving Average – T3)
  - [ ] ADX (Average Directional Movement Index)
  - [ ] ADXR (Average Directional Movement Index Rating)
  - [ ] AROON
  - [ ] AROONOSC
  - [ ] SAR (Parabolic SAR)
- Momentum indicators
  - [X] Wilder's RSI (Relative Strength Index)
  - [ ] EMA-based RSI (Relative Strength Index)
  - [ ] MOM (Momentum)
  - [ ] CMO (Chande Momentum Oscillator)
  - [ ] ROC (Rate of Change)
  - [ ] ROCR (Rate of Change Ratio)
  - [ ] MFI (Money Flow Index)
  - [ ] TRIX
  - [ ] ULTOSC (Ultimate Oscillator)
  - [ ] WILLR (Williams %R)
- Oscillators
  - [ ] MACD (Moving Average Convergence/Divergence)
  - [ ] MACDEXT
  - [ ] STOCH (Stochastic Oscillator)
  - [ ] STOCHF (Fast Stochastic)
  - [ ] STOCHRSI
- Volatility indicators
  - [ ] ATR (Average True Range)
  - [ ] NATR (Normalized Average True Range)
  - [ ] BBANDS (Bollinger Bands)
  - [ ] BBANDSWIDTH
- Volume indicators
- [ ] OBV (On-Balance Volume)
  - [ ] AD (Accumulation/Distribution Line)
  - [ ] ADOSC (Accumulation/Distribution Oscillator)
  - [ ] VWAP (Volume Weighted Average Price)
- Sentiment and signal analysis:
  - [ ] Non-technical indicators from free sources
- Performance optimizations:
  - [ ] Caching strategies and rate limiting
- Infrastructure:
  - [X] Structured data responses using Pydantic models
  - [X] Comprehensive error handling
  - [X] Type hints throughout the codebase
  - [X] Input validation with enums and constraints
  - [X] Modular design with separated concerns

## :hammer: Development

### Installation

Getting started with the Technical Analysis MCP Server is a breeze. Just follow
these simple steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/technical-analysis-mcp.git
   cd technical-analysis-mcp
   ```

2. Install dependencies using uv:

   ```bash
   uv sync
   uv pip install -e .
   ```

### Running tests

To run the unit tests, use the following command:

```bash
uv run pytest
```

To run tests with coverage, use:

```bash
uv run pytest --cov=src/technical_analysis_mcp --cov-report=markdown
```

This will generate a coverage report in Markdown format and display it in the terminal.

### Linting and formatting

```bash
# To run basic linting, use:
uv run ruff check

# To run type checking, use:
uv run pyright

# To run markdown linting, use:
uv run pymarkdown scan .
```

### Tips for development

When adding new tools, follow the existing patterns:

1. Create Pydantic data structures in `src/technical_analysis_mcp/models/`
2. Implement tool logic in `src/technical_analysis_mcp/tools/`
3. Register tools in `src/technical_analysis_mcp/server/server.py`
4. Write comprehensive tests in `tests/tools/`, `tests/models/`,
   `tests/servers/`, etc
5. Update this README with new tool information

## :gift: Contributing

We welcome contributions to the Technical Analysis MCP Server! Whether you're a
seasoned developer or just starting out, your help is appreciated. Please
follow these guidelines:

1. **Fork the repository** and create a new branch for your feature or bug fix.
2. **Commit your changes** with clear and concise commit messages following the
   [Conventional Commits](https://www.conventionalcommits.org/) specification.
3. **Push your changes** to your fork and submit a pull request.

## :speech_balloon: Support

For support, please open an issue on the GitHub repository or contact the
maintainers directly. We're here to help!

## :clap: Acknowledgments

A big thank you to all the contributors and supporters of this project. Your
help and feedback are invaluable!
