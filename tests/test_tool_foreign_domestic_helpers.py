"""
Module for testing Foreign Domestic Helpers data fetching and processing.

This module contains unit tests for the functions related to Foreign Domestic Helpers
statistics in the HK Law MCP Server.
"""

import unittest
from unittest.mock import patch, MagicMock
from typing import List, Any
from hkopenai.hk_law_mcp_server.foreign_domestic_helpers import (
    fetch_fdh_data,
    _get_foreign_domestic_helpers_statistics,
    register,
)


class TestForeignDomesticHelpers(unittest.TestCase):
    """Test class for verifying Foreign Domestic Helpers data processing."""

    CSV_DATA = """As at end of Year,Philippines,Indonesia,Others,Total
2016,189105,154073,8335,351513
2017,201090,159613,8948,369651
2018,210897,165907,9271,386075
2019,219073,170828,9419,399320
2020,207402,157802,8680,373884
2021,191783,140057,7611,339451
2022,190059,139961,8169,338189
2023,199516,147597,9118,356231
2024,202972,155577,9422,367971"""

    def setUp(self):
        """Set up test environment with mocked HTTP responses for data fetching."""
        self.mock_requests = patch("requests.get").start()
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.text = self.CSV_DATA
        mock_response.encoding = "utf-8"
        self.mock_requests.return_value = mock_response
        self.addCleanup(patch.stopall)

    def test_fetch_fdh_data(self):
        """Test fetching and parsing of Foreign Domestic Helpers data."""
        data: List[Dict[str, str]] = fetch_fdh_data()
        self.assertEqual(len(data), 9)
        self.assertEqual(data[0]["As at end of Year"], "2016")
        self.assertEqual(int(data[0]["Philippines"]), 189105)
        self.assertEqual(int(data[0]["Total"]), 351513)

    def test_get_foreign_domestic_helpers_statistics_default(self):
        """Test retrieval of all Foreign Domestic Helpers statistics without filters."""
        result: Dict[str, Any] = _get_foreign_domestic_helpers_statistics()
        self.assertIn("data", result)
        data = result["data"]

        self.assertEqual(len(data), 9)
        self.assertEqual(data[0]["As at end of Year"], "2016")
        self.assertEqual(int(data[0]["Philippines"]), 189105)
        self.assertEqual(int(data[0]["Total"]), 351513)

    def test_get_foreign_domestic_helpers_statistics_year_filter(self):
        """Test retrieval of Foreign Domestic Helpers statistics for a specific year."""
        result: Dict[str, Any] = _get_foreign_domestic_helpers_statistics(year=2020)
        self.assertIn("data", result)
        data = result["data"]
        self.assertEqual(data["As at end of Year"], "2020")
        self.assertEqual(int(data["Philippines"]), 207402)
        self.assertEqual(int(data["Total"]), 373884)

    def test_get_foreign_domestic_helpers_statistics_year_not_found(self):
        """Test error handling when data for a specific year is not found."""
        result: Dict[str, Any] = _get_foreign_domestic_helpers_statistics(year=2030)
        self.assertIn("error", result)
        self.assertEqual(result["error"], "No data for year 2030")

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
        self.assertEqual(
            decorated_function.__name__, "get_foreign_domestic_helpers_statistics"
        )

        # Call the decorated function and verify it calls _get_foreign_domestic_helpers_statistics
        with patch(
            "hkopenai.hk_law_mcp_server.foreign_domestic_helpers._get_foreign_domestic_helpers_statistics"
        ) as mock_get_foreign_domestic_helpers_statistics:
            decorated_function(2023)
            mock_get_foreign_domestic_helpers_statistics.assert_called_once_with(2023)


if __name__ == "__main__":
    unittest.main()
