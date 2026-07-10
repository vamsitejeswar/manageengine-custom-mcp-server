from typing import Optional
from fastmcp import FastMCP
from src.api.client import me_client
from src.api.endpoints import SOM


def register_som_tools(mcp: FastMCP) -> None:

    @mcp.tool()
    async def som_get_summary() -> dict:
        """Retrieve detailed summary for SOM (Systems/OS Management) computers."""
        return await me_client.get(SOM.SUMMARY)

    @mcp.tool()
    async def som_list_computers(
        branchofficefilter: Optional[str] = None,
        computernamefilter: Optional[str] = None,
        fqdnfilter: Optional[str] = None,
        domainfilter: Optional[str] = None,
        platformfilter: Optional[str] = None,
        residfilter: Optional[str] = None,
        installstatusfilter: Optional[str] = None,
        liveStatusfilter: Optional[str] = None,
        searchcomputerfilter: Optional[str] = None,
        servicetagfilter: Optional[str] = None,
        agentcontactfilter: Optional[str] = None,
        page: Optional[int] = None,
        pagelimit: Optional[int] = None,
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

    @mcp.tool()
    async def som_list_remote_offices(
        page: Optional[int] = None,
        pagelimit: Optional[int] = None,
    ) -> dict:
        """Retrieve details of all configured remote offices."""
        return await me_client.get(SOM.REMOTE_OFFICE, params={
            "page": page,
            "pagelimit": pagelimit,
        })

    @mcp.tool()
    async def som_install_agent(resourceids: list[int]) -> dict:
        """Install the ManageEngine agent on specific computers by resource ID."""
        return await me_client.post(SOM.INSTALL_AGENT, json={"resourceids": resourceids})

    @mcp.tool()
    async def som_uninstall_agent(resourceids: list[int]) -> dict:
        """Uninstall the ManageEngine agent from specific computers by resource ID."""
        return await me_client.post(SOM.UNINSTALL_AGENT, json={"resourceids": resourceids})

    @mcp.tool()
    async def som_remove_computer(resourceids: list[int]) -> dict:
        """Remove specific computers from ManageEngine management by resource ID."""
        return await me_client.post(SOM.REMOVE_COMPUTER, json={"resourceids": resourceids})
