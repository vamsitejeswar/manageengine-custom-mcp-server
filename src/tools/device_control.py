from typing import Optional
from fastmcp import FastMCP
from mcp.types import ToolAnnotations

_R = ToolAnnotations(readOnlyHint=True)
from src.api.client import me_client
from src.api.endpoints import DeviceControl


def register_device_control_tools(mcp: FastMCP) -> None:

    @mcp.tool(annotations=_R)
    async def dc_get_file_activity(
        fileExtnGrp: Optional[str] = None,
        period: Optional[str] = None,
        gid: Optional[str] = None,
        fileExtn: Optional[str] = None,
        numberOfDays: Optional[int] = None,
        computer: Optional[str] = None,
        isblocked: Optional[str] = None,
        dipId: Optional[str] = None,
        domain: Optional[str] = None,
        event: Optional[str] = None,
        page: Optional[int] = None,
        pagelimit: Optional[int] = None,
    ) -> dict:
        """Retrieve all file activities detected within the network."""
        return await me_client.get(DeviceControl.FILE_TRACE, params={
            "fileExtnGrp": fileExtnGrp,
            "period": period,
            "gid": gid,
            "fileExtn": fileExtn,
            "numberOfDays": numberOfDays,
            "computer": computer,
            "isblocked": isblocked,
            "dipId": dipId,
            "domain": domain,
            "event": event,
            "page": page,
            "pagelimit": pagelimit,
        })

    @mcp.tool(annotations=_R)
    async def dc_get_device_audit(
        period: Optional[str] = None,
        computer: Optional[str] = None,
        isblocked: Optional[str] = None,
        gid: Optional[str] = None,
        dipId: Optional[str] = None,
        os_platform: Optional[str] = None,
        domain: Optional[str] = None,
        devicetype: Optional[str] = None,
        page: Optional[int] = None,
        pagelimit: Optional[int] = None,
    ) -> dict:
        """Retrieve all device activities detected across the network."""
        return await me_client.get(DeviceControl.DEVICE_AUDIT, params={
            "period": period,
            "computer": computer,
            "isblocked": isblocked,
            "gid": gid,
            "dipId": dipId,
            "os_platform": os_platform,
            "domain": domain,
            "devicetype": devicetype,
            "page": page,
            "pagelimit": pagelimit,
        })

    @mcp.tool(annotations=_R)
    async def dc_get_file_shadow(
        period: Optional[str] = None,
        computer: Optional[str] = None,
        gid: Optional[str] = None,
        domain: Optional[str] = None,
        numberOfDays: Optional[int] = None,
        status: Optional[str] = None,
        page: Optional[int] = None,
        pagelimit: Optional[int] = None,
    ) -> dict:
        """Retrieve file shadow operation details across the network."""
        return await me_client.get(DeviceControl.FILE_SHADOW, params={
            "period": period,
            "computer": computer,
            "gid": gid,
            "domain": domain,
            "numberOfDays": numberOfDays,
            "status": status,
            "page": page,
            "pagelimit": pagelimit,
        })

    @mcp.tool(annotations=_R)
    async def dc_list_unique_devices(
        isblocked: Optional[str] = None,
        os_platform: Optional[str] = None,
        devicetype: Optional[str] = None,
        page: Optional[int] = None,
        pagelimit: Optional[int] = None,
    ) -> dict:
        """Retrieve the list of unique devices detected across the network."""
        return await me_client.get(DeviceControl.DEVICE_SUMMARY, params={
            "isblocked": isblocked,
            "os_platform": os_platform,
            "devicetype": devicetype,
            "page": page,
            "pagelimit": pagelimit,
        })

    @mcp.tool(annotations=_R)
    async def dc_list_blocked_devices(
        period: Optional[str] = None,
        computer: Optional[str] = None,
        gid: Optional[str] = None,
        dipId: Optional[str] = None,
        os_platform: Optional[str] = None,
        domain: Optional[str] = None,
        devicetype: Optional[str] = None,
        page: Optional[int] = None,
        pagelimit: Optional[int] = None,
    ) -> dict:
        """Retrieve all blocked devices within the network."""
        return await me_client.get(DeviceControl.BLOCK_AUDIT, params={
            "period": period,
            "computer": computer,
            "gid": gid,
            "dipId": dipId,
            "os_platform": os_platform,
            "domain": domain,
            "devicetype": devicetype,
            "page": page,
            "pagelimit": pagelimit,
        })

    @mcp.tool(annotations=_R)
    async def dc_get_mac_device_status(
        page: Optional[int] = None,
        pagelimit: Optional[int] = None,
    ) -> dict:
        """Retrieve device status details for all Mac computers in the network."""
        return await me_client.get(DeviceControl.MAC_DEV_STATUS, params={
            "page": page,
            "pagelimit": pagelimit,
        })

    @mcp.tool(annotations=_R)
    async def dc_get_windows_device_status(
        page: Optional[int] = None,
        pagelimit: Optional[int] = None,
    ) -> dict:
        """Retrieve device status details for all Windows computers in the network."""
        return await me_client.get(DeviceControl.WIN_DEV_STATUS, params={
            "page": page,
            "pagelimit": pagelimit,
        })

    @mcp.tool(annotations=_R)
    async def dc_list_exempted_devices(
        period: Optional[str] = None,
        os_platform: Optional[str] = None,
        domain: Optional[str] = None,
        devicetype: Optional[str] = None,
        status: Optional[str] = None,
        page: Optional[int] = None,
        pagelimit: Optional[int] = None,
    ) -> dict:
        """Retrieve all temporarily exempted devices across the network."""
        return await me_client.get(DeviceControl.DEVICE_EXEMPTION, params={
            "period": period,
            "os_platform": os_platform,
            "domain": domain,
            "devicetype": devicetype,
            "status": status,
            "page": page,
            "pagelimit": pagelimit,
        })

    @mcp.tool(annotations=_R)
    async def dc_list_exempted_device_types(
        period: Optional[str] = None,
        os_platform: Optional[str] = None,
        domain: Optional[str] = None,
        devicetype: Optional[str] = None,
        status: Optional[str] = None,
        page: Optional[int] = None,
        pagelimit: Optional[int] = None,
    ) -> dict:
        """Retrieve temporarily exempted device types across the network."""
        return await me_client.get(DeviceControl.TYPE_EXEMPTION, params={
            "period": period,
            "os_platform": os_platform,
            "domain": domain,
            "devicetype": devicetype,
            "status": status,
            "page": page,
            "pagelimit": pagelimit,
        })
