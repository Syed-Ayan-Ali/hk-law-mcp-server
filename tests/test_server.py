"""
Module for testing the MCP server creation and functionality.

This module contains unit tests for the server setup of the HK Law MCP Server.
"""

import unittest
from unittest.mock import patch, Mock
from hkopenai.hk_law_mcp_server.server import create_mcp_server


class TestApp(unittest.TestCase):
    """Test class for verifying MCP server creation and tool functionality."""

    @patch("hkopenai.hk_law_mcp_server.server.FastMCP")
    @patch("hkopenai.hk_law_mcp_server.server.foreign_domestic_helpers")
    def test_create_mcp_server(self, mock_foreign_domestic_helpers, mock_fastmcp):
        """Test the creation and configuration of the MCP server with mocked dependencies."""
        # Setup mocks
        mock_server = Mock()

        # Configure mock_server.tool to return a mock that acts as the decorator
        # This mock will then be called with the function to be decorated
        mock_server.tool.return_value = Mock()
        mock_fastmcp.return_value = mock_server

        # Test server creation
        server = create_mcp_server()

        # Verify server creation
        mock_fastmcp.assert_called_once()
        self.assertEqual(server, mock_server)

        mock_foreign_domestic_helpers.register.assert_called_once_with(mock_server)


if __name__ == "__main__":
    unittest.main()
