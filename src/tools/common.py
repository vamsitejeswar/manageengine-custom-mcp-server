from fastmcp import FastMCP
from src.api.client import me_client
from src.api.endpoints import Common


def register_common_tools(mcp: FastMCP) -> None:

    @mcp.tool()
    async def common_list_custom_groups() -> dict:
        """Retrieve the list of all custom groups configured on the Endpoint Central server."""
        return await me_client.get(Common.CUSTOM_GROUPS)

    @mcp.tool()
    async def common_get_server_properties() -> dict:
        """Retrieve details of domains, custom groups, and branch offices managed by the server."""
        return await me_client.get(Common.SERVER_PROPERTIES)
