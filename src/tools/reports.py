from typing import Optional
from fastmcp import FastMCP
from src.api.client import me_client
from src.api.endpoints import Reports
from src.config import settings


def register_report_tools(mcp: FastMCP) -> None:

    @mcp.tool()
    async def report_list_query_reports() -> dict:
        """List all available query reports."""
        return await me_client.get(Reports.QUERY_REPORTS)

    @mcp.tool()
    async def report_get_query_data(
        report_id: int,
        startIndex: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> dict:
        """Fetch data for a specific query report by its numeric ID."""
        return await me_client.get(
            Reports.query_data(report_id),
            params={"startIndex": startIndex, "limit": limit},
        )

    @mcp.tool()
    async def report_list_custom_reports() -> dict:
        """Fetch all available custom reports for the authenticated user."""
        return await me_client.get(Reports.CUSTOM_REPORTS)

    @mcp.tool()
    async def report_get_custom_data(
        first_item_index: Optional[int] = None,
        page_length: Optional[int] = None,
    ) -> dict:
        """Retrieve custom report data. page_length max is 500."""
        return await me_client.post(
            Reports.custom_view(settings.crview),
            params={"_FI": first_item_index, "_PL": page_length},
        )
