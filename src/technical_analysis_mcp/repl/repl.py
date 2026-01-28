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
        """Initialize the MCP REPL.

        Initializes the command-line interface and sets up the FastMCP client
        connection to the technical analysis server.

        """
        super().__init__()
        self._hist = []
        self.client = Client(server)

    def precmd(self, line: str) -> str:
        """This method is called after the line has been input but before it has been interpreted.

        Args:
            line: Command line argument (unused).

        Returns:
            str: The same input argument.

        """
        self._hist += [line.strip()]
        return line

    def onecmd(self, line: str) -> bool:
        """Interpret the argument as though it had been typed in response to the prompt.

        Args:
            line: Command line argument (unused).

        Returns:
            bool: False to continue in the REPL.

        """
        try:
            return cmd.Cmd.onecmd(self, line)
        except Exception as e:  # noqa: BLE001
            sys.stderr.write(f"Exception: {e}\n")
            sys.stderr.write("\nCheck yout internet connection.\n")
            return False

    def do_exit(self, line: str) -> bool:
        """Exit the REPL.

        Args:
            line: Command line argument (unused).

        Returns:
            bool: True to exit the REPL.

        """
        del line
        sys.stdout.write("Goodbye!\n")
        return True

    def do_quit(self, line: str) -> bool:
        """Exit the REPL.

        Alias for the exit command.

        Args:
            line: Command line argument (unused).

        Returns:
            bool: True to exit the REPL.

        """
        return self.do_exit(line)

    def do_EOF(self, line: str) -> bool:  # noqa: N802
        """Exit on EOF (Ctrl+D).

        Handles the end-of-file signal to gracefully exit the REPL.

        Args:
            line: Command line argument (unused).

        Returns:
            bool: True to exit the REPL.

        """
        sys.stdout.write("\n")
        return self.do_exit(line)

    def do_history(self, line: str) -> None:
        """Occurs on "history" command.

        Print a list of commands that have been previously entered.

        Args:
            line: Command line argument (unused).

        """
        del line

        for entry in self._hist:
            sys.stdout.write(f"{entry}\n")

    def do_get_instructions(self, line: str) -> None:
        """Get the MCP server instructions.

        Retrieves and displays the server's initialization instructions
        that describe the server's capabilities and usage guidelines.

        Args:
            line: Command line argument (unused).

        """
        del line
        asyncio.run(self._get_instructions())

    def do_list_tools(self, line: str) -> None:
        """List available tools.

        Displays a list of all registered tools available on the server.

        Args:
            line: Command line argument (unused).

        """
        del line
        asyncio.run(self._list_tools())

    def do_get_tool_description(self, line: str) -> None:
        """Get tool description and schema by name.

        Displays detailed information about a specific tool including its
        description, input schema, and output schema.

        Args:
            line: The name of the tool to get information about.

        """
        if not line:
            sys.stdout.write("Usage: tool <tool_name>\n")
            return

        asyncio.run(self._get_tool_info(line))

    def do_call_tool(self, line: str) -> None:
        """Call a tool with arguments.

        Executes a specific tool with the provided arguments and displays
        the result.

        Args:
            line: Command line argument containing tool name and JSON arguments.
                Format: "<tool_name> <json_args>"

        Raises:
            json.JSONDecodeError: If the provided arguments are not valid JSON.

        """
        if not line:
            sys.stdout.write("Usage: call <tool_name> <args>\n")
            return

        parts = line.split()

        if len(parts) < 1:
            sys.stdout.write("Usage: call <tool_name> <args>\n")
            return

        tool_name = parts[0]
        tool_args = " ".join(parts[1:])
        asyncio.run(self._call_tool(tool_name, tool_args))

    async def _get_instructions(self) -> None:
        """Get the MCP server instructions.

        Retrieves the server's initialization instructions asynchronously
        and displays them to the user.

        """
        async with self.client:
            result = self.client.initialize_result
            instructions = "No instructions available."

            if result is not None and result.instructions is not None:
                instructions = result.instructions

            sys.stdout.write(instructions)
            sys.stdout.write("\n")

    async def _list_tools(self) -> None:
        """List available tools.

        Retrieves the list of registered tools from the server and
        displays them to the user.

        """
        async with self.client:
            tools = await self.client.list_tools()

            for tool in tools:
                sys.stdout.write(f"- {tool.name}\n")

    async def _get_tool_info(self, tool_name: str) -> None:
        """Get tool description and schema.

        Retrieves detailed information about a specific tool including its
        description, input schema, and output schema.

        Args:
            tool_name: The name of the tool to get information about.

        """
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
        """Call a tool with arguments.

        Executes a specific tool with the provided JSON arguments and
        displays the result.

        Args:
            tool_name: The name of the tool to call.
            tool_args: JSON string containing the tool arguments.

        Raises:
            json.JSONDecodeError: If the provided arguments are not valid JSON.

        """
        async with self.client:
            args_dict = json.loads(tool_args)

            result = await self.client.call_tool(tool_name, args_dict)

            if result.structured_content is not None:
                sys.stdout.write(json.dumps(result.structured_content))
            else:
                for c in result.content:
                    if c.type == "text":
                        sys.stdout.write(c.text)

            sys.stdout.write("\n")


def main() -> None:
    """Entry point for the MCP REPL.

    Initializes and starts the REPL command loop for interacting with
    the technical analysis MCP server.

    """
    repl = Repl()
    repl.cmdloop()


if __name__ == "__main__":
    main()
