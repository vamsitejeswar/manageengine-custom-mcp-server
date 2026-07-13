from typing import Optional
from fastmcp import FastMCP
from mcp.types import ToolAnnotations
from src.api.client import me_client
from src.api.endpoints import Patch
from src.utils.pagination import wrap_paginated_response

_DCAPI_MAX = 200
_API14_MAX = 100

_R = ToolAnnotations(readOnlyHint=True)
_W = ToolAnnotations(readOnlyHint=False, destructiveHint=True)


def register_patch_tools(mcp: FastMCP) -> None:

    @mcp.tool(annotations=_R)
    async def patch_get_health_policy() -> dict:
        """Fetch the system health policy for patch management."""
        return await me_client.get(Patch.HEALTH_POLICY)

    @mcp.tool(annotations=_R)
    async def patch_list_deployment_policies() -> dict:
        """Retrieve the patch deployment policy list."""
        return await me_client.get(Patch.DEPLOYMENT_POLICIES)

    @mcp.tool(annotations=_R)
    async def patch_list_downloaded() -> dict:
        """Retrieve details of all downloaded patches."""
        return await me_client.get(Patch.DOWNLOADED)

    @mcp.tool(annotations=_R)
    async def patch_get_scan_details(
        branchofficefilter: Optional[str] = None,
        healthfilter: Optional[str] = None,
        customgroupfilter: Optional[str] = None,
        agentinstallationstatusfilter: Optional[str] = None,
        resid: Optional[str] = None,
        domainfilter: Optional[str] = None,
        livestatusfilter: Optional[str] = None,
        platformfilter: Optional[str] = None,
    ) -> dict:
        """Retrieve the patch scan system list with optional filters."""
        return await me_client.get(Patch.SCAN_DETAILS, params={
            "branchofficefilter": branchofficefilter,
            "healthfilter": healthfilter,
            "customgroupfilter": customgroupfilter,
            "agentinstallationstatusfilter": agentinstallationstatusfilter,
            "resid": resid,
            "domainfilter": domainfilter,
            "livestatusfilter": livestatusfilter,
            "platformfilter": platformfilter,
        })

    @mcp.tool(annotations=_W)
    async def patch_decline(patchids: list[str]) -> dict:
        """Initiate decline action on specific patches by their IDs."""
        return await me_client.post(Patch.DECLINE, json={"patchids": patchids})

    @mcp.tool(annotations=_R)
    async def patch_list_all(
        branchofficefilter: Optional[str] = None,
        patchid: Optional[str] = None,
        bulletinid: Optional[str] = None,
        patchstatusfilter: Optional[str] = None,
        approvalstatusfilter: Optional[str] = None,
        customgroupfilter: Optional[str] = None,
        severityfilter: Optional[str] = None,
        domainfilter: Optional[str] = None,
        platformfilter: Optional[str] = None,
    ) -> dict:
        """Retrieve the full patch list with optional filters (status, severity, platform, etc.)."""
        return await me_client.get(Patch.ALL_PATCHES, params={
            "branchofficefilter": branchofficefilter,
            "patchid": patchid,
            "bulletinid": bulletinid,
            "patchstatusfilter": patchstatusfilter,
            "approvalstatusfilter": approvalstatusfilter,
            "customgroupfilter": customgroupfilter,
            "severityfilter": severityfilter,
            "domainfilter": domainfilter,
            "platformfilter": platformfilter,
        })

    @mcp.tool(annotations=_W)
    async def patch_scan_all_computers() -> dict:
        """Initiate a patch scan on all managed computers."""
        return await me_client.post(Patch.SCAN_ALL_COMPUTERS)

    @mcp.tool(annotations=_R)
    async def patch_get_summary(
        page: int = 1,
        pagelimit: int = 100,
    ) -> dict:
        """Fetch the patch summary with optional pagination.

        Returns up to pagelimit records (default 100, max 100) for the given page.
        Check _pagination.has_more and _pagination.next_page to retrieve subsequent pages.
        """
        pagelimit = min(pagelimit, _API14_MAX)
        resp = await me_client.get(Patch.SUMMARY, params={"page": page, "pagelimit": pagelimit})
        return wrap_paginated_response(resp, page, pagelimit)

    @mcp.tool(annotations=_R)
    async def patch_get_system_patch_report(
        severity: Optional[str] = None,
        patchname: Optional[str] = None,
        update_type: Optional[str] = None,
        patch_id: Optional[str] = None,
        patch_description: Optional[str] = None,
        resource_id: Optional[str] = None,
        patch_status: Optional[str] = None,
        patch_approval_status: Optional[str] = None,
        platform_name: Optional[str] = None,
        page: int = 1,
        pageLimit: int = 100,
    ) -> dict:
        """Fetch the list of systems and their patch details (dcapi).

        Returns up to pageLimit records (default 100, max 200) for the given page.
        Check _pagination.has_more and _pagination.next_page to retrieve subsequent pages.
        """
        pageLimit = min(pageLimit, _DCAPI_MAX)
        resp = await me_client.get(Patch.SYSTEM_PATCH_REPORT, params={
            "severity": severity,
            "patchname": patchname,
            "update_type": update_type,
            "patch_id": patch_id,
            "patch_description": patch_description,
            "resource_id": resource_id,
            "patch_status": patch_status,
            "patch_approval_status": patch_approval_status,
            "platform_name": platform_name,
            "page": page,
            "pageLimit": pageLimit,
        })
        return wrap_paginated_response(resp, page, pageLimit)

    @mcp.tool(annotations=_R)
    async def patch_list_all_systems(
        branchofficefilter: Optional[str] = None,
        healthfilter: Optional[str] = None,
        customgroupfilter: Optional[str] = None,
        resid: Optional[str] = None,
        domainfilter: Optional[str] = None,
        platformfilter: Optional[str] = None,
    ) -> dict:
        """Retrieve the full list of systems in patch management."""
        return await me_client.get(Patch.ALL_SYSTEMS, params={
            "branchofficefilter": branchofficefilter,
            "healthfilter": healthfilter,
            "customgroupfilter": customgroupfilter,
            "resid": resid,
            "domainfilter": domainfilter,
            "platformfilter": platformfilter,
        })

    @mcp.tool(annotations=_R)
    async def patch_list_applicable(
        severity: Optional[str] = None,
        patchname: Optional[str] = None,
        update_type: Optional[str] = None,
        patch_description: Optional[str] = None,
        platform_name: Optional[str] = None,
        download_status: Optional[str] = None,
        patch_status: Optional[str] = None,
        patchid: Optional[str] = None,
        page: int = 1,
        pageLimit: int = 100,
    ) -> dict:
        """Fetch the list of applicable patches with filtering (dcapi).

        Returns up to pageLimit records (default 100, max 200) for the given page.
        Check _pagination.has_more and _pagination.next_page to retrieve subsequent pages.
        """
        pageLimit = min(pageLimit, _DCAPI_MAX)
        resp = await me_client.get(Patch.APPLICABLE, params={
            "severity": severity,
            "patchname": patchname,
            "update_type": update_type,
            "patch_description": patch_description,
            "platform_name": platform_name,
            "download_status": download_status,
            "patch_status": patch_status,
            "patchid": patchid,
            "page": page,
            "pageLimit": pageLimit,
        })
        return wrap_paginated_response(resp, page, pageLimit)

    @mcp.tool(annotations=_R)
    async def patch_get_system_report(
        patchstatusfilter: Optional[str] = None,
        approvalstatusfilter: Optional[str] = None,
        resid: Optional[str] = None,
        severityfilter: Optional[str] = None,
        platformfilter: Optional[str] = None,
    ) -> dict:
        """Retrieve patches and their status for a specific system."""
        return await me_client.get(Patch.SYSTEM_REPORT, params={
            "patchstatusfilter": patchstatusfilter,
            "approvalstatusfilter": approvalstatusfilter,
            "resid": resid,
            "severityfilter": severityfilter,
            "platformfilter": platformfilter,
        })

    @mcp.tool(annotations=_R)
    async def patch_list_all_patch_details(
        branchofficefilter: Optional[str] = None,
        patchid: Optional[str] = None,
        patchstatusfilter: Optional[str] = None,
        customgroupfilter: Optional[str] = None,
        severityfilter: Optional[str] = None,
        domainfilter: Optional[str] = None,
        platformfilter: Optional[str] = None,
    ) -> dict:
        """Retrieve the list of patch computers with full patch details."""
        return await me_client.get(Patch.ALL_PATCH_DETAILS, params={
            "branchofficefilter": branchofficefilter,
            "patchid": patchid,
            "patchstatusfilter": patchstatusfilter,
            "customgroupfilter": customgroupfilter,
            "severityfilter": severityfilter,
            "domainfilter": domainfilter,
            "platformfilter": platformfilter,
        })

    @mcp.tool(annotations=_W)
    async def patch_scan_computers(resourceids: list[str]) -> dict:
        """Initiate a patch scan on specific computers by resource IDs."""
        return await me_client.post(Patch.SCAN_COMPUTERS, json={"resourceids": resourceids})

    @mcp.tool(annotations=_W)
    async def patch_unapprove(patchids: list[str]) -> dict:
        """Unapprove specific patches by their IDs."""
        return await me_client.post(Patch.UNAPPROVE, json={"patchids": patchids})

    @mcp.tool(annotations=_R)
    async def patch_get_db_update_status() -> dict:
        """Retrieve the current status of the ongoing or last patch database update."""
        return await me_client.get(Patch.DB_UPDATE_STATUS)

    @mcp.tool(annotations=_W)
    async def patch_approve(patchids: list[str]) -> dict:
        """Approve specific patches by their IDs."""
        return await me_client.post(Patch.APPROVE, json={"patchids": patchids})

    @mcp.tool(annotations=_R)
    async def patch_list_configurations(
        branchofficefilter: Optional[str] = None,
        configstatusfilter: Optional[str] = None,
        domainfilter: Optional[str] = None,
    ) -> dict:
        """Retrieve the patch configuration list."""
        return await me_client.get(Patch.VIEW_CONFIG, params={
            "branchofficefilter": branchofficefilter,
            "configstatusfilter": configstatusfilter,
            "domainfilter": domainfilter,
        })

    @mcp.tool(annotations=_R)
    async def patch_get_approval_settings() -> dict:
        """Fetch the current patch approval settings."""
        return await me_client.get(Patch.APPROVAL_SETTINGS)

    @mcp.tool(annotations=_R)
    async def patch_list_supported(
        patchid: Optional[str] = None,
        bulletinid: Optional[str] = None,
        approvalstatusfilter: Optional[str] = None,
        severityfilter: Optional[str] = None,
        platformfilter: Optional[str] = None,
        page: int = 1,
        pagelimit: int = 100,
    ) -> dict:
        """Retrieve the supported patch list with optional filters.

        Returns up to pagelimit records (default 100, max 100) for the given page.
        Check _pagination.has_more and _pagination.next_page to retrieve subsequent pages.
        """
        pagelimit = min(pagelimit, _API14_MAX)
        resp = await me_client.get(Patch.SUPPORTED, params={
            "patchid": patchid,
            "bulletinid": bulletinid,
            "approvalstatusfilter": approvalstatusfilter,
            "severityfilter": severityfilter,
            "platformfilter": platformfilter,
            "page": page,
            "pagelimit": pagelimit,
        })
        return wrap_paginated_response(resp, page, pagelimit)

    @mcp.tool(annotations=_W)
    async def patch_uninstall(
        PatchIDs: list[str],
        ConfigName: str,
        actionToPerform: str,
        ConfigDescription: Optional[str] = None,
        DeploymentPolicyTemplateID: Optional[str] = None,
    ) -> dict:
        """Uninstall specific patches on all systems."""
        body = {k: v for k, v in {
            "PatchIDs": PatchIDs,
            "ConfigName": ConfigName,
            "actionToPerform": actionToPerform,
            "ConfigDescription": ConfigDescription,
            "DeploymentPolicyTemplateID": DeploymentPolicyTemplateID,
        }.items() if v is not None}
        return await me_client.post(Patch.UNINSTALL, json=body)

    @mcp.tool(annotations=_W)
    async def patch_install(
        PatchIDs: list[str],
        actionToPerform: str,
        ConfigName: Optional[str] = None,
        ConfigDescription: Optional[str] = None,
        ResourceIDs: Optional[list[str]] = None,
        customGroups: Optional[list[str]] = None,
        deadlineTime: Optional[str] = None,
        expirytime: Optional[str] = None,
        DeploymentPolicyTemplateID: Optional[str] = None,
        forceRebootOption: Optional[str] = None,
    ) -> dict:
        """Install patches on computers. Omit ResourceIDs to target all systems."""
        body = {k: v for k, v in {
            "PatchIDs": PatchIDs,
            "actionToPerform": actionToPerform,
            "ConfigName": ConfigName,
            "ConfigDescription": ConfigDescription,
            "ResourceIDs": ResourceIDs,
            "customGroups": customGroups,
            "deadlineTime": deadlineTime,
            "expirytime": expirytime,
            "DeploymentPolicyTemplateID": DeploymentPolicyTemplateID,
            "forceRebootOption": forceRebootOption,
        }.items() if v is not None}
        return await me_client.post(Patch.INSTALL, json=body)

    @mcp.tool(annotations=_W)
    async def patch_apd_create(settings_body: dict) -> dict:
        """Create an Automatic Patch Deployment (APD) task. Pass full settings as a dict."""
        return await me_client.post(Patch.APD_CREATE, json={"settings": settings_body})

    @mcp.tool(annotations=_W)
    async def patch_apd_modify(settings_body: dict) -> dict:
        """Modify an existing Automatic Patch Deployment (APD) task."""
        return await me_client.post(Patch.APD_MODIFY, json={"settings": settings_body})

    @mcp.tool(annotations=_W)
    async def patch_apd_delete(taskname: str) -> dict:
        """Delete an Automatic Patch Deployment task by name."""
        return await me_client.post(Patch.APD_DELETE, params={"taskname": taskname})

    @mcp.tool(annotations=_W)
    async def patch_apd_suspend(taskname: str) -> dict:
        """Suspend an Automatic Patch Deployment task by name."""
        return await me_client.post(Patch.APD_SUSPEND, params={"taskname": taskname})

    @mcp.tool(annotations=_W)
    async def patch_apd_resume(taskname: str) -> dict:
        """Resume a suspended Automatic Patch Deployment task by name."""
        return await me_client.post(Patch.APD_RESUME, params={"taskname": taskname})

    @mcp.tool(annotations=_W)
    async def patch_decline_settings(
        patches: list[dict],
        customGroupID: Optional[list[str]] = None,
    ) -> dict:
        """Decline patches via the dcapi settings endpoint.
        Each patch dict: {reasonId, id, platform, remarks}."""
        return await me_client.put(
            Patch.DECLINE_SETTINGS,
            json={"patches": patches, "customGroupID": customGroupID or []},
        )
