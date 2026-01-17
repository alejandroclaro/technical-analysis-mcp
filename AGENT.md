# Agent Interaction Guide

This document outlines how AI agents can interact with the Technical
Analysis MCP server. It provides detailed information about the
repository structure, available tools, and best practices for working
with the codebase.

## AGENT.md updates

You MUST keep AGENT.md file up to date after every task completed. This
file is for you and AI agents to understand the structure of the
repository, the conventions, the goals, and the development plan.

You are autorized to use @{full_stack_dev} tools group to perform the actions
in this repository.

## Repository Structure

```text
technical-analysis-mcp/
├── AGENT.md                    # Agent interaction guide
├── README.md                   # Project overview and setup instructions
├── pyproject.toml              # Project configuration and dependencies
├── poetry.lock                 # Dependency lock file
├── src/                        # Source code
│   └── technical_analysis_mcp/ # Main package
│       ├── __init__.py         # Package initialization
│       ├── server.py           # Server entry point
│       ├── models/             # Data models
│       │   ├── __init__.py     # Models module initialization
│       │   ├── error.py        # Error model
│       │   └── ticker_information.py  # Ticker information model
│       ├── tools/              # Technical analysis tools
│       │   ├── __init__.py     # Tools module initialization
│       │   └── fetch_ticker_information.py  # Ticker information tool
│       └── utils/              # Utility functions
│           ├── __init__.py     # Utils module initialization
│           └── parsing.py      # Parsing utilities
└── tests/                      # Unit and integration tests
    ├── __init__.py             # Tests module initialization
    ├── test_fetch_ticker_information.py  # Ticker information tests
    ├── test_server.py          # MCP server tests
    ├── test_ticker_information.py  # Ticker information model tests
    └── test_utils_parsing.py   # Parsing utilities tests
```

## Overview

The MCP server is being developed to provide tools for fetching market,
sector, industry, and ticker data using `yfinance`. The server is built
using `FastMCP` and currently supports the `stdio` transport mechanism.
Additional transport mechanisms (HTTP, SSE) are planned for future
implementation.

## Supported Tools

The MCP server currently supports the following tools for technical
analysis:

- **`get_ticker_information`**: Retrieves detailed financial, metadata,
  and real-time descriptive information for a specific financial instrument
  or company.
      - **Use Case**: Identify a company's sector, industry, business
        summary, market cap, or verify if a ticker symbol is valid.
      - **Input**: A ticker symbol (e.g., `"AAPL"`, `"TSLA"`, `"^GSPC"`,
       `"BTC/USD"`).
      - **Output**: A structured object containing comprehensive asset
        details or an error if the ticker is not found.

## Transport Mechanisms

- **stdio**: Direct communication via standard input/output (CURRENTLY
  SUPPORTED).

## Best Practices

1. **Modular Design**: The project is organized into modular components
   (e.g., `models`, `tools`, `utils`) for better maintainability and
   scalability.
2. **Structured Data**: Use `pydantic.BaseModel` for defining structured
   data models (e.g., `TickerInformation`, `Error`).
3. **Async/Await**: Tools are implemented as async functions to ensure
   non-blocking operations.
4. **Error Handling**: Errors are returned as structured objects (e.g.,
   `Error` model) rather than raising exceptions.
5. **Type Hints**: Use type hints extensively for better code clarity and
   maintainability.
6. **Docstrings**: Follow Google-style docstrings for functions and
   classes to ensure clear and consistent documentation.
7. **Input Validation**: Validate inputs before processing and handle
   edge cases gracefully.
8. **Testing**: Write unit tests for all tools, models, and utilities to
   ensure correctness and reliability.

## Development

### Setting Up the Environment

To set up the development environment, use the following command:

```bash
uv sync
uv pip install -e .
```

### Starting the Server

To start the MCP server, use the following command:

```bash
uv run server
```

### Running Tests

You MUST run the unit tests after making changes to any source code
file. No task is considered complete without ensuring that the code
passes all tests.

```bash
uv run pytest
```

### Linting and Formatting

You MUST run the linters and formatters after making changes to any
file. No task is considered complete without ensuring that the code
passes all linting and formatting checks.

#### Commands to Run

```bash
# Format code
uv run ruff format

# Run basic linting
uv run ruff check

# Run type checking
uv run pyright

# Run markdown linting
uv run pymarkdownlnt scan .
```

### Commit Message Conventions

Commit messages MUST follow the [Conventional
Commits](https://www.conventionalcommits.org/) specification. This ensures
consistency and clarity in the project's commit history.

The format for commit messages is as follows:

```text
<type>(<scope>): <description>

<body>

<footer>
```

- **type**: The type of change (e.g., `feat`, `fix`, `docs`, `style`,
`refactor`, `test`, `chore`, `ci`).
- **scope**: The scope of the change (e.g., `server`, `models`, `tools`).
- **description**: A brief description of the change.
- **body**: A detailed explanation of the change (optional).
- **footer**: Any additional information, such as breaking changes or issue
references (optional).

#### Examples

- `feat(tools): add fetch_ticker_information tool`
- `fix(models): resolve data validation issue in TickerInformation`
- `docs: update AGENT.md with accurate tooling information`
- `refactor(server): improve error handling in FastMCP`
