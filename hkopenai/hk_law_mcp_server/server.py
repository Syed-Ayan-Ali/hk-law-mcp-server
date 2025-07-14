"""
Module for setting up and running the HK OpenAI Law and Security MCP Server.

This module configures the server with tools for law and security data in Hong Kong.
"""

from fastmcp import FastMCP
from hkopenai.hk_law_mcp_server import foreign_domestic_helpers



def create_mcp_server():
    """Create and configure the MCP server"""
    mcp = FastMCP(name="HK OpenAI Law and Security Server")

    foreign_domestic_helpers.register(mcp)

    return mcp


def main(host: str, port: int, sse: bool):
    """Run the HK OpenAI Law and Security MCP Server with command-line arguments.

    Args:
        args: Command line arguments passed to the function.
    """
    server = create_mcp_server()

    if sse:
        server.run(transport="streamable-http", host=host, port=port)
        print(f"Server running in SSE mode on port {port}, bound to {host}")
    else:
        server.run()
        print("Server running in stdio mode")



