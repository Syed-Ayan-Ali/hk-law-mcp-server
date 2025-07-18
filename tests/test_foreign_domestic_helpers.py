"""
Module for testing the foreign domestic helpers tool functionality.

This module contains unit tests for fetching and processing foreign domestic helpers data.
"""

import unittest
from unittest.mock import patch, MagicMock

from hkopenai.hk_law_mcp_server.tools.foreign_domestic_helpers import (
    _get_foreign_domestic_helpers_statistics,
    register,
)


class TestForeignDomesticHelpers(unittest.TestCase):
    """
    Test class for verifying foreign domestic helpers functionality.

    This class contains test cases to ensure the data fetching and processing
    for foreign domestic helpers data work as expected.
    """

    def test_get_foreign_domestic_helpers_statistics(self):
        """
        Test the retrieval and filtering of foreign domestic helpers statistics.

        This test verifies that the function correctly fetches and filters data by year,
        and handles error cases.
        """
        # Mock the CSV data
        mock_csv_data = [
            {"As at end of Year": "2020", "Number of FDH": "300000"},
            {"As at end of Year": "2021", "Number of FDH": "310000"},
            {"As at end of Year": "2022", "Number of FDH": "320000"},
        ]

        with patch(
            "hkopenai.hk_law_mcp_server.tools.foreign_domestic_helpers.fetch_csv_from_url"
        ) as mock_fetch_csv_from_url:
            # Setup mock response for successful data fetching
            mock_fetch_csv_from_url.return_value = mock_csv_data

            # Test filtering by year
            result = _get_foreign_domestic_helpers_statistics(year=2021)
            self.assertIn("data", result)
            self.assertEqual(result["data"]["Number of FDH"], "310000")

            # Test no year filter
            result = _get_foreign_domestic_helpers_statistics()
            self.assertIn("data", result)
            self.assertEqual(len(result["data"]), 3)

            # Test empty result for non-matching year
            result = _get_foreign_domestic_helpers_statistics(year=2023)
            self.assertIn("error", result)
            self.assertEqual(result["error"], "No data for year 2023")

            # Test error handling when fetch_csv_from_url returns an error
            mock_fetch_csv_from_url.return_value = {"error": "CSV fetch failed"}
            result = _get_foreign_domestic_helpers_statistics(year=2021)
            self.assertEqual(result, {"type": "Error", "error": "CSV fetch failed"})

    def test_register_tool(self):
        """
        Test the registration of the get_foreign_domestic_helpers_statistics tool.

        This test verifies that the register function correctly registers the tool
        with the FastMCP server and that the registered tool calls the underlying
        _get_foreign_domestic_helpers_statistics function.
        """
        mock_mcp = MagicMock()

        # Call the register function
        register(mock_mcp)

        # Verify that mcp.tool was called with the correct description
        mock_mcp.tool.assert_called_once_with(
            description="Statistics on Foreign Domestic Helpers in Hong Kong. Data source: Immigration Department"
        )

        # Get the mock that represents the decorator returned by mcp.tool
        mock_decorator = mock_mcp.tool.return_value

        # Verify that the mock decorator was called once (i.e., the function was decorated)
        mock_decorator.assert_called_once()

        # The decorated function is the first argument of the first call to the mock_decorator
        decorated_function = mock_decorator.call_args[0][0]

        # Verify the name of the decorated function
        self.assertEqual(decorated_function.__name__, "get_foreign_domestic_helpers_statistics")

        # Call the decorated function and verify it calls _get_foreign_domestic_helpers_statistics
        with patch(
            "hkopenai.hk_law_mcp_server.tools.foreign_domestic_helpers._get_foreign_domestic_helpers_statistics"
        ) as mock_get_foreign_domestic_helpers_statistics:
            decorated_function(year=2021)
            mock_get_foreign_domestic_helpers_statistics.assert_called_once_with(2021)
