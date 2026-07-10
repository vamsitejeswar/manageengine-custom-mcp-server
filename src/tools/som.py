from typing import Optional
from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from src.api.client import me_client
from src.api.endpoints import SOM

_R = ToolAnnotations(readOnlyHint=True)
_W = ToolAnnotations(readOnlyHint=False, destructiveHint=True)


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
        page: int | None = None,
        pagelimit: int | None = None,
    ) -> dict:
        """Retrieve all computer details managed by SOM with optional filters."""
        return await me_client.get(SOM.COMPUTERS, params={
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

    @mcp.tool(annotations=_R)
    async def som_list_remote_offices(
        page: int | None = None,
        pagelimit: int | None = None,
    ) -> dict:
        """Retrieve details of all configured remote offices."""
        return await me_client.get(SOM.REMOTE_OFFICE, params={"page": page, "pagelimit": pagelimit})

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
