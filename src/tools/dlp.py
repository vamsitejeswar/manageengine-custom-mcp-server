from typing import Optional
from fastmcp import FastMCP
from mcp.types import ToolAnnotations

_R = ToolAnnotations(readOnlyHint=True)
from src.api.client import me_client
from src.api.endpoints import DLP
from src.utils.pagination import wrap_paginated_response

_API14_MAX = 100


def register_dlp_tools(mcp: FastMCP) -> None:

    @mcp.tool(annotations=_R)
    async def dlp_get_usb_printer_report(
        page: int = 1,
        pagelimit: int = 100,
    ) -> dict:
        """Retrieve all USB printers with custom group association count.

        Returns up to pagelimit records (default 100, max 100) for the given page.
        Check _pagination.has_more and _pagination.next_page to retrieve subsequent pages.
        """
        pagelimit = min(pagelimit, _API14_MAX)
        resp = await me_client.get(DLP.USB_PRINTER, params={"page": page, "pagelimit": pagelimit})
        return wrap_paginated_response(resp, page, pagelimit)

    @mcp.tool(annotations=_R)
    async def dlp_get_network_printer_report(
        page: int = 1,
        pagelimit: int = 100,
    ) -> dict:
        """Retrieve all network printers with custom group association count.

        Returns up to pagelimit records (default 100, max 100) for the given page.
        Check _pagination.has_more and _pagination.next_page to retrieve subsequent pages.
        """
        pagelimit = min(pagelimit, _API14_MAX)
        resp = await me_client.get(DLP.NETWORK_PRINTER, params={"page": page, "pagelimit": pagelimit})
        return wrap_paginated_response(resp, page, pagelimit)

    @mcp.tool(annotations=_R)
    async def dlp_get_false_positives(
        boundarytype: Optional[int] = None,
        page: int = 1,
        pagelimit: int = 100,
    ) -> dict:
        """Retrieve false positives reported by endpoints in the enterprise perimeter.
        boundarytype: 1=Storage, 5=Network printers, 6=USB printers, 8=Web domains, 16=Email domains.

        Returns up to pagelimit records (default 100, max 100) for the given page.
        Check _pagination.has_more and _pagination.next_page to retrieve subsequent pages.
        """
        pagelimit = min(pagelimit, _API14_MAX)
        resp = await me_client.get(DLP.FALSE_POSITIVES, params={
            "boundarytype": boundarytype,
            "page": page,
            "pagelimit": pagelimit,
        })
        return wrap_paginated_response(resp, page, pagelimit)

    @mcp.tool(annotations=_R)
    async def dlp_get_endpoint_activity(
        actionFilter: Optional[int] = None,
        page: int = 1,
        pagelimit: int = 100,
    ) -> dict:
        """Retrieve all activities performed on endpoints.
        actionFilter: 0=Allowed, 1=Blocked, 2=Self Override, 3=Reported False Positive.

        Returns up to pagelimit records (default 100, max 100) for the given page.
        Check _pagination.has_more and _pagination.next_page to retrieve subsequent pages.
        """
        pagelimit = min(pagelimit, _API14_MAX)
        resp = await me_client.get(DLP.ENDPOINT_ACTIVITY, params={
            "actionFilter": actionFilter,
            "page": page,
            "pagelimit": pagelimit,
        })
        return wrap_paginated_response(resp, page, pagelimit)

    @mcp.tool(annotations=_R)
    async def dlp_get_justifications(
        justificationmsg: Optional[str] = None,
        page: int = 1,
        pagelimit: int = 100,
    ) -> dict:
        """Retrieve business justifications used by endpoints.

        Returns up to pagelimit records (default 100, max 100) for the given page.
        Check _pagination.has_more and _pagination.next_page to retrieve subsequent pages.
        """
        pagelimit = min(pagelimit, _API14_MAX)
        resp = await me_client.get(DLP.JUSTIFICATIONS, params={
            "justificationmsg": justificationmsg,
            "page": page,
            "pagelimit": pagelimit,
        })
        return wrap_paginated_response(resp, page, pagelimit)

    @mcp.tool(annotations=_R)
    async def dlp_get_rules_report(
        ruleClass: Optional[str] = None,
        page: int = 1,
        pagelimit: int = 100,
    ) -> dict:
        """Retrieve all deployed DLP rules with custom group association count.
        ruleClass: Finance, PII, Health, Source code, Custom rules.

        Returns up to pagelimit records (default 100, max 100) for the given page.
        Check _pagination.has_more and _pagination.next_page to retrieve subsequent pages.
        """
        pagelimit = min(pagelimit, _API14_MAX)
        resp = await me_client.get(DLP.RULES, params={
            "ruleClass": ruleClass,
            "page": page,
            "pagelimit": pagelimit,
        })
        return wrap_paginated_response(resp, page, pagelimit)

    @mcp.tool(annotations=_R)
    async def dlp_get_email_domains_report(
        page: int = 1,
        pagelimit: int = 100,
    ) -> dict:
        """Retrieve all deployed email domains with custom group association count.

        Returns up to pagelimit records (default 100, max 100) for the given page.
        Check _pagination.has_more and _pagination.next_page to retrieve subsequent pages.
        """
        pagelimit = min(pagelimit, _API14_MAX)
        resp = await me_client.get(DLP.EMAIL_DOMAINS, params={"page": page, "pagelimit": pagelimit})
        return wrap_paginated_response(resp, page, pagelimit)

    @mcp.tool(annotations=_R)
    async def dlp_get_web_domains_report(
        page: int = 1,
        pagelimit: int = 100,
    ) -> dict:
        """Retrieve all deployed web domains with custom group association count.

        Returns up to pagelimit records (default 100, max 100) for the given page.
        Check _pagination.has_more and _pagination.next_page to retrieve subsequent pages.
        """
        pagelimit = min(pagelimit, _API14_MAX)
        resp = await me_client.get(DLP.WEB_DOMAINS, params={"page": page, "pagelimit": pagelimit})
        return wrap_paginated_response(resp, page, pagelimit)

    @mcp.tool(annotations=_R)
    async def dlp_get_devices_report(
        page: int = 1,
        pagelimit: int = 100,
    ) -> dict:
        """Retrieve all devices with custom group association count.

        Returns up to pagelimit records (default 100, max 100) for the given page.
        Check _pagination.has_more and _pagination.next_page to retrieve subsequent pages.
        """
        pagelimit = min(pagelimit, _API14_MAX)
        resp = await me_client.get(DLP.DEVICES, params={"page": page, "pagelimit": pagelimit})
        return wrap_paginated_response(resp, page, pagelimit)

    @mcp.tool(annotations=_R)
    async def dlp_get_applications_report(
        page: int = 1,
        pagelimit: int = 100,
    ) -> dict:
        """Retrieve all deployed applications with custom group association count.

        Returns up to pagelimit records (default 100, max 100) for the given page.
        Check _pagination.has_more and _pagination.next_page to retrieve subsequent pages.
        """
        pagelimit = min(pagelimit, _API14_MAX)
        resp = await me_client.get(DLP.APPLICATIONS, params={"page": page, "pagelimit": pagelimit})
        return wrap_paginated_response(resp, page, pagelimit)

    @mcp.tool(annotations=_R)
    async def dlp_get_data_rule_violations(
        ruleClass: Optional[str] = None,
        page: int = 1,
        pagelimit: int = 100,
    ) -> dict:
        """Retrieve false positives reported by endpoints in data rule violations.

        Returns up to pagelimit records (default 100, max 100) for the given page.
        Check _pagination.has_more and _pagination.next_page to retrieve subsequent pages.
        """
        pagelimit = min(pagelimit, _API14_MAX)
        resp = await me_client.get(DLP.DATA_RULE_VIOLATIONS, params={
            "ruleClass": ruleClass,
            "page": page,
            "pagelimit": pagelimit,
        })
        return wrap_paginated_response(resp, page, pagelimit)
