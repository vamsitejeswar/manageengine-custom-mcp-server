from typing import Optional
from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from src.api.client import me_client
from src.api.endpoints import SOM
from src.utils.pagination import wrap_paginated_response

_R = ToolAnnotations(readOnlyHint=True)
_W = ToolAnnotations(readOnlyHint=False, destructiveHint=True)

_API14_MAX = 100


def register_som_tools(mcp: FastMCP) -> None:

    @mcp.tool(annotations=_R)
    async def som_get_summary() -> dict:
        """Retrieve detailed summary for SOM (Systems/OS Management) computers."""
        return await me_client.get(SOM.SUMMARY)

    @mcp.tool(annotations=_R)
    async def som_list_computers(
        branchofficefilter: str | None = None,
        computernamefilter: str | None = None,
        fqdnfilter: str | None = None,
        domainfilter: str | None = None,
        platformfilter: str | None = None,
        residfilter: str | None = None,
        installstatusfilter: str | None = None,
        liveStatusfilter: str | None = None,
        searchcomputerfilter: str | None = None,
        servicetagfilter: str | None = None,
        agentcontactfilter: str | None = None,
        page: int = 1,
        pagelimit: int = 100,
    ) -> dict:
        """Retrieve all computer details managed by SOM with optional filters.

        Returns up to pagelimit records (default 100, max 100) for the given page.
        Check _pagination.has_more and _pagination.next_page to retrieve subsequent pages.
        """
        pagelimit = min(pagelimit, _API14_MAX)
        resp = await me_client.get(SOM.COMPUTERS, params={
            "branchofficefilter": branchofficefilter,
            "computernamefilter": computernamefilter,
            "fqdnfilter": fqdnfilter,
            "domainfilter": domainfilter,
            "platformfilter": platformfilter,
            "residfilter": residfilter,
            "installstatusfilter": installstatusfilter,
            "liveStatusfilter": liveStatusfilter,
            "searchcomputerfilter": searchcomputerfilter,
            "servicetagfilter": servicetagfilter,
            "agentcontactfilter": agentcontactfilter,
            "page": page,
            "pagelimit": pagelimit,
        })
        return wrap_paginated_response(resp, page, pagelimit)

    @mcp.tool(annotations=_R)
    async def som_list_remote_offices(
        page: int = 1,
        pagelimit: int = 100,
    ) -> dict:
        """Retrieve details of all configured remote offices.

        Returns up to pagelimit records (default 100, max 100) for the given page.
        Check _pagination.has_more and _pagination.next_page to retrieve subsequent pages.
        """
        pagelimit = min(pagelimit, _API14_MAX)
        resp = await me_client.get(SOM.REMOTE_OFFICE, params={"page": page, "pagelimit": pagelimit})
        return wrap_paginated_response(resp, page, pagelimit)

    @mcp.tool(annotations=_W)
    async def som_install_agent(resourceids: list[int]) -> dict:
        """Install the ManageEngine agent on specific computers by resource ID."""
        return await me_client.post(SOM.INSTALL_AGENT, json={"resourceids": resourceids})

    @mcp.tool(annotations=_W)
    async def som_uninstall_agent(resourceids: list[int]) -> dict:
        """Uninstall the ManageEngine agent from specific computers by resource ID."""
        return await me_client.post(SOM.UNINSTALL_AGENT, json={"resourceids": resourceids})

    @mcp.tool(annotations=_W)
    async def som_remove_computer(resourceids: list[int]) -> dict:
        """Remove specific computers from ManageEngine management by resource ID."""
        return await me_client.post(SOM.REMOVE_COMPUTER, json={"resourceids": resourceids})
