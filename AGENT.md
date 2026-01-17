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
│   └── technical_analysis_mcp/ # Main package
│       ├── __init__.py         # Package initialization
│       ├── server.py           # Server entry point
│       ├── models/             # Data models
│       │   └── __init__.py     # Models module initialization
│       └── tools/              # Technical analysis tools
│           └── __init__.py     # Tools module initialization
└── tests/                      # Unit and integration tests
    ├── __init__.py             # Tests module initialization
    └── test_mcp_server.py      # MCP server tests
```

## Overview

The MCP server is being developed to provide tools for fetching market, sector,
industry, and ticker data using `yfinance`. The server is built using `FastMCP`
and will support multiple transport mechanisms (stdio, HTTP, SSE) once the tools
are implemented.

Currently, the server provides the basic infrastructure and lifecycle management.
Tools for technical analysis will be added in future updates.

## Supported Tools

The MCP server is currently being developed and will support various tools for
technical analysis. The tools are planned for future implementation.

## Transport Mechanisms

- **stdio**: Direct communication via standard input/output.
- **HTTP**: RESTful API endpoints (PLANNED).
- **SSE**: Server-Sent Events for real-time updates (PLANNED).

## Best Practices

1. **Input Validation**: Always validate inputs before sending them to the
   server.
2. **Error Handling**: Handle errors gracefully and provide meaningful feedback
   to users.
3. **Rate Limiting**: Be mindful of rate limits when making multiple requests.
4. **Caching**: Cache responses to avoid redundant requests.

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

AI agents MUST run the unit tests after making changes to any source code
file. No task is considered complete without ensuring that the code
passes all tests.

```bash
uv run pytest
```

### Linting and Formatting

AI agents MUST run the linters and formatters after making changes to any
file. No task is considered complete without ensuring that the code
passes all linting and formatting checks.

#### Commands to Run

```bash
# Format code
uv run ruff format src tests

# Run basic linting
uv run ruff check src tests

# Run type checking
uv run pyright

# Run markdown linting
uv run pymarkdownlnt scan *.md
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

- `feat(server): add HTTP transport support`
- `fix(models): resolve data validation issue`
- `docs: update setup instructions`

## Error Handling

- If a tool fails, the server will respond with an error message.
- Agents should handle retries or fallbacks gracefully.

### Example Error Response

```json
{
  "error": "Failed to fetch market data: Invalid ticker"
}
```
