from typing import Optional
from fastmcp import FastMCP
from mcp.types import ToolAnnotations

_R = ToolAnnotations(readOnlyHint=True)
from src.api.client import me_client
from src.api.endpoints import DEX


def register_dex_tools(mcp: FastMCP) -> None:

    @mcp.tool(annotations=_R)
    async def dex_get_config() -> dict:
        """Retrieve DEX (Digital Experience) module configuration and metadata."""
        return await me_client.get(DEX.META)

    @mcp.tool(annotations=_R)
    async def dex_get_addon_info() -> dict:
        """Retrieve addon module information for DEX."""
        return await me_client.get(DEX.ADDON)

    @mcp.tool(annotations=_R)
    async def dex_get_last_update_time() -> dict:
        """Retrieve the last time the DEX score summary was generated."""
        return await me_client.get(DEX.LAST_UPDATED_TIME)

    @mcp.tool(annotations=_R)
    async def dex_get_next_process_time() -> dict:
        """Retrieve the next scheduled DEX score summary generation time."""
        return await me_client.get(DEX.NEXT_PROCESS_TIME)

    @mcp.tool(annotations=_R)
    async def dex_get_latest_experience(
        score_profile_id: str,
        resourceId: Optional[str] = None,
        branchOffice: Optional[str] = None,
        cgFilter: Optional[str] = None,
    ) -> dict:
        """Retrieve the latest experience score for a DEX score profile."""
        return await me_client.get(
            DEX.latest_experience(score_profile_id),
            params={"resourceId": resourceId, "branchOffice": branchOffice, "cgFilter": cgFilter},
        )

    @mcp.tool(annotations=_R)
    async def dex_get_device_profile(score_profile_id: str, agent_resource_id: str) -> dict:
        """Retrieve experience and device details for a specific agent/device."""
        return await me_client.get(DEX.device_profile(score_profile_id, agent_resource_id))

    @mcp.tool(annotations=_R)
    async def dex_get_device_nodes(
        score_profile_id: str,
        agent_resource_id: str,
        filterType: Optional[str] = None,
    ) -> dict:
        """Retrieve detailed experience metric nodes for a specific device."""
        return await me_client.get(
            DEX.device_nodes(score_profile_id, agent_resource_id),
            params={"filterType": filterType},
        )
