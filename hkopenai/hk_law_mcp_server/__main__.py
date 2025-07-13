"""
Main entry point for the HK OpenAI Law and Security MCP Server.

This module serves as the entry point to run the server.
"""

from hkopenai_common.cli_utils import cli_main
from .server import server

if __name__ == "__main__":
    cli_main(server, "HK Law MCP Server")