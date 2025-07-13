"""
Module for setting up and running the HK OpenAI Law and Security MCP Server.

This module configures the server with tools for law and security data in Hong Kong.
"""

from fastmcp import FastMCP
from hkopenai.hk_law_mcp_server import foreign_domestic_helpers
from typing import Dict, List, Annotated, Optional, Union
from pydantic import Field


def create_mcp_server():
    """Create and configure the MCP server"""
    mcp = FastMCP(name="HK OpenAI Law and Security Server")

    @mcp.tool(
        description="Statistics on Foreign Domestic Helpers in Hong Kong. Data source: Immigration Department"
    )
    def get_fdh_statistics(
        year: Annotated[
            Optional[int], Field(description="Filter by specific year")
        ] = None,
    ) -> Dict[str, Union[Dict[str, str], List[Dict[str, str]], str]]:
        return foreign_domestic_helpers.get_fdh_statistics(year)

    return mcp


def main(host: str, port: int, sse: bool):
    """Run the HK OpenAI Law and Security MCP Server with command-line arguments.
    
    Args:
        args: Command line arguments passed to the function.
    """
    server = create_mcp_server()

    if sse:
        server.run(transport="streamable-http", host=host, port=port)
        print(f"Server running in SSE mode on port {args.port}, bound to {args.host}")
    else:
        server.run()
        print("Server running in stdio mode")


if __name__ == "__main__":
    main()
