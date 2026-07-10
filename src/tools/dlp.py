from typing import Optional
from fastmcp import FastMCP
from src.api.client import me_client
from src.api.endpoints import DLP


def register_dlp_tools(mcp: FastMCP) -> None:

    @mcp.tool()
    async def dlp_get_usb_printer_report(
        page: Optional[int] = None,
        pagelimit: Optional[int] = None,
    ) -> dict:
        """Retrieve all USB printers with custom group association count."""
        return await me_client.get(DLP.USB_PRINTER, params={"page": page, "pagelimit": pagelimit})

    @mcp.tool()
    async def dlp_get_network_printer_report(
        page: Optional[int] = None,
        pagelimit: Optional[int] = None,
    ) -> dict:
        """Retrieve all network printers with custom group association count."""
        return await me_client.get(DLP.NETWORK_PRINTER, params={"page": page, "pagelimit": pagelimit})

    @mcp.tool()
    async def dlp_get_false_positives(
        boundarytype: Optional[int] = None,
        page: Optional[int] = None,
        pagelimit: Optional[int] = None,
    ) -> dict:
        """Retrieve false positives reported by endpoints in the enterprise perimeter.
        boundarytype: 1=Storage, 5=Network printers, 6=USB printers, 8=Web domains, 16=Email domains."""
        return await me_client.get(DLP.FALSE_POSITIVES, params={
            "boundarytype": boundarytype,
            "page": page,
            "pagelimit": pagelimit,
        })

    @mcp.tool()
    async def dlp_get_endpoint_activity(
        actionFilter: Optional[int] = None,
        page: Optional[int] = None,
        pagelimit: Optional[int] = None,
    ) -> dict:
        """Retrieve all activities performed on endpoints.
        actionFilter: 0=Allowed, 1=Blocked, 2=Self Override, 3=Reported False Positive."""
        return await me_client.get(DLP.ENDPOINT_ACTIVITY, params={
            "actionFilter": actionFilter,
            "page": page,
            "pagelimit": pagelimit,
        })

    @mcp.tool()
    async def dlp_get_justifications(
        justificationmsg: Optional[str] = None,
        page: Optional[int] = None,
        pagelimit: Optional[int] = None,
    ) -> dict:
        """Retrieve business justifications used by endpoints."""
        return await me_client.get(DLP.JUSTIFICATIONS, params={
            "justificationmsg": justificationmsg,
            "page": page,
            "pagelimit": pagelimit,
        })

    @mcp.tool()
    async def dlp_get_rules_report(
        ruleClass: Optional[str] = None,
        page: Optional[int] = None,
        pagelimit: Optional[int] = None,
    ) -> dict:
        """Retrieve all deployed DLP rules with custom group association count.
        ruleClass: Finance, PII, Health, Source code, Custom rules."""
        return await me_client.get(DLP.RULES, params={
            "ruleClass": ruleClass,
            "page": page,
            "pagelimit": pagelimit,
        })

    @mcp.tool()
    async def dlp_get_email_domains_report(
        page: Optional[int] = None,
        pagelimit: Optional[int] = None,
    ) -> dict:
        """Retrieve all deployed email domains with custom group association count."""
        return await me_client.get(DLP.EMAIL_DOMAINS, params={"page": page, "pagelimit": pagelimit})

    @mcp.tool()
    async def dlp_get_web_domains_report(
        page: Optional[int] = None,
        pagelimit: Optional[int] = None,
    ) -> dict:
        """Retrieve all deployed web domains with custom group association count."""
        return await me_client.get(DLP.WEB_DOMAINS, params={"page": page, "pagelimit": pagelimit})

    @mcp.tool()
    async def dlp_get_devices_report(
        page: Optional[int] = None,
        pagelimit: Optional[int] = None,
    ) -> dict:
        """Retrieve all devices with custom group association count."""
        return await me_client.get(DLP.DEVICES, params={"page": page, "pagelimit": pagelimit})

    @mcp.tool()
    async def dlp_get_applications_report(
        page: Optional[int] = None,
        pagelimit: Optional[int] = None,
    ) -> dict:
        """Retrieve all deployed applications with custom group association count."""
        return await me_client.get(DLP.APPLICATIONS, params={"page": page, "pagelimit": pagelimit})

    @mcp.tool()
    async def dlp_get_data_rule_violations(
        ruleClass: Optional[str] = None,
        page: Optional[int] = None,
        pagelimit: Optional[int] = None,
    ) -> dict:
        """Retrieve false positives reported by endpoints in data rule violations."""
        return await me_client.get(DLP.DATA_RULE_VIOLATIONS, params={
            "ruleClass": ruleClass,
            "page": page,
            "pagelimit": pagelimit,
        })
