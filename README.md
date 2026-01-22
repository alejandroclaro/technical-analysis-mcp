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
you need it, without the wait or hiting rate limits.

And that's not all. We're also incorporating non-technical indicators like
sentiment and other signals derived from free sources of information, giving
you a comprehensive view of the market landscape.

## :sparkles: Features

- **Comprehensive Data Fetching**: Retrieve detailed financial, and real-time
  descriptive information for specific financial instruments or companies.
- **Local Database and Cache**: Store previously fetched data locally to avoid
  repeated internet requests.
- **Modular Design**: Organized into modular tools.
- **Structured Data**: Uses structured responses to improve predectivility and
  processing by LLMs.
- **Error Handling**: Errors are returned as structured objects rather than
  raising exceptions.
- **Type Hints**: Extensive use of type hints for better LLMs "undertanding"
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

### Running Tests

To run the unit tests, use the following command:

```bash
uv run pytest
```

To run tests with coverage, use:

```bash
uv run pytest --cov=src/technical_analysis_mcp --cov-report=markdown
```

This will generate a coverage report in Markdown format and display it in the terminal.

### Linting and Formatting

```bash
# To run basic linting, use:
uv run ruff check

# To run type checking, use:
uv run pyright

# To run markdown linting, use:
uv run pymarkdown scan .
```

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

## :question: FAQ

### What makes this project different from other MCPs?

Our project stands out by offering a complete and robust solution that
leverages free sources of information and mathematical calculations to provide
top-notch tools and functions without the hefty price tag. Additionally, we
include a cache and local database to store previously fetched data, ensuring
lightning-fast access to information without repeated internet requests.

### How can I contribute to the project?

We welcome contributions from everyone! Please follow the guidelines outlined
in the Contributing section to get started.

### Where can I get help if I have issues or questions?

For support, please open an issue on the GitHub repository or contact the
maintainers directly. We're here to help!
