from typing import Optional
from fastmcp import FastMCP
from mcp.types import ToolAnnotations

_R = ToolAnnotations(readOnlyHint=True)
from src.api.client import me_client
from src.api.endpoints import Reports
from src.config import settings
from src.utils.pagination import wrap_offset_paginated_response

_QUERY_REPORT_MAX = 200
_CUSTOM_REPORT_MAX = 500


def register_report_tools(mcp: FastMCP) -> None:

    @mcp.tool(annotations=_R)
    async def report_list_query_reports() -> dict:
        """List all available query reports."""
        return await me_client.get(Reports.QUERY_REPORTS)

    @mcp.tool(annotations=_R)
    async def report_get_query_data(
        report_id: int,
        startIndex: int = 0,
        limit: int = 100,
    ) -> dict:
        """Fetch data for a specific query report by its numeric ID.

        startIndex is 0-based. Returns up to limit records (default 100, max 200).
        Check _pagination.has_more and _pagination.next_start_index to retrieve subsequent pages.
        """
        limit = min(limit, _QUERY_REPORT_MAX)
        resp = await me_client.get(
            Reports.query_data(report_id),
            params={"startIndex": startIndex, "limit": limit},
        )
        return wrap_offset_paginated_response(resp, startIndex, limit)

    @mcp.tool(annotations=_R)
    async def report_list_custom_reports() -> dict:
        """Fetch all available custom reports for the authenticated user."""
        return await me_client.get(Reports.CUSTOM_REPORTS)

    @mcp.tool(annotations=_R)
    async def report_get_custom_data(
        first_item_index: int = 0,
        page_length: int = 100,
    ) -> dict:
        """Retrieve custom report data.

        first_item_index is 0-based. Returns up to page_length records (default 100, max 500).
        Check _pagination.has_more and _pagination.next_start_index to retrieve subsequent pages.
        """
        page_length = min(page_length, _CUSTOM_REPORT_MAX)
        resp = await me_client.post(
            Reports.custom_view(settings.crview),
            params={"_FI": first_item_index, "_PL": page_length},
        )
        return wrap_offset_paginated_response(resp, first_item_index, page_length)
