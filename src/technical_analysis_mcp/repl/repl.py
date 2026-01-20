"""MCP Client REPL."""

import asyncio
import cmd
import json
import sys

from fastmcp.client import Client

from technical_analysis_mcp.server import server


class Repl(cmd.Cmd):
    """Client REPL for interacting with MCP Server."""

    intro = "Welcome to Technical Analysis MCP. Type 'help' or '?' to list commands.\n"
    prompt = "mcp> "

    def __init__(self) -> None:
        """Initialize the MCP REPL."""
        super().__init__()
        self.client = Client(server)

    def do_exit(self, arg: str) -> bool:
        """Exit the REPL."""
        del arg
        sys.stdout.write("Goodbye!\n")
        return True

    def do_quit(self, arg: str) -> bool:
        """Exit the REPL."""
        return self.do_exit(arg)

    def do_EOF(self, arg: str) -> bool:  # noqa: N802
        """Exit on EOF (Ctrl+D)."""
        sys.stdout.write("\n")
        return self.do_exit(arg)

    def do_get_instructions(self, arg: str) -> None:
        """Get the MCP server instructions."""
        del arg
        asyncio.run(self._get_instructions())

    def do_list_tools(self, arg: str) -> None:
        """List available tools."""
        del arg
        asyncio.run(self._list_tools())

    def do_get_tool_description(self, arg: str) -> None:
        """Get tool description and schema by name."""
        if not arg:
            sys.stdout.write("Usage: tool <tool_name>\n")
            return

        asyncio.run(self._get_tool_info(arg))

    def do_call_tool(self, arg: str) -> None:
        """Call a tool with arguments."""
        if not arg:
            sys.stdout.write("Usage: call <tool_name> <args>\n")
            return

        parts = arg.split()

        if len(parts) < 1:
            sys.stdout.write("Usage: call <tool_name> <args>\n")
            return

        tool_name = parts[0]
        tool_args = " ".join(parts[1:])
        asyncio.run(self._call_tool(tool_name, tool_args))

    async def _get_instructions(self) -> None:
        """Get the MCP server instructions."""
        async with self.client:
            result = self.client.initialize_result
            instructions = "No instructions available."

            if result is not None and result.instructions is not None:
                instructions = result.instructions

            sys.stdout.write(instructions)
            sys.stdout.write("\n")

    async def _list_tools(self) -> None:
        """List available tools."""
        async with self.client:
            tools = await self.client.list_tools()

            for tool in tools:
                sys.stdout.write(f"- {tool.name}\n")

    async def _get_tool_info(self, tool_name: str) -> None:
        """Get tool description and schema."""
        async with self.client:
            tools = await self.client.list_tools()
            tool = next((t for t in tools if t.name == tool_name), None)

            if not tool:
                sys.stdout.write(f"Tool '{tool_name}' not found.\n")
                return

            if tool.description is not None:
                sys.stdout.write(tool.description)
            else:
                sys.stdout.write("No description available")

            if tool.inputSchema:
                sys.stdout.write("\nInput Schema:\n")
                sys.stdout.write(json.dumps(tool.inputSchema))

            if tool.outputSchema:
                sys.stdout.write("\nOutput Schema:\n")
                sys.stdout.write(json.dumps(tool.outputSchema))

            sys.stdout.write("\n")

    async def _call_tool(self, tool_name: str, tool_args: str) -> None:
        """Call a tool with arguments."""
        async with self.client:
            args_dict = json.loads(tool_args)

            result = await self.client.call_tool(tool_name, args_dict)
            sys.stdout.write(json.dumps(result))
            sys.stdout.write("\n")


def main() -> None:
    """Entry point for the MCP REPL."""
    repl = Repl()
    repl.cmdloop()


if __name__ == "__main__":
    main()
