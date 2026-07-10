from typing import Optional
from fastmcp import FastMCP
from src.api.client import me_client
from src.api.endpoints import Inventory


def register_inventory_tools(mcp: FastMCP) -> None:

    @mcp.tool()
    async def inv_get_summary() -> dict:
        """Retrieve overall summary data for the Inventory module."""
        return await me_client.get(Inventory.ALL_SUMMARY)

    @mcp.tool()
    async def inv_get_filter_params() -> dict:
        """Retrieve available inventory filter parameter values."""
        return await me_client.get(Inventory.FILTER_PARAMS)

    @mcp.tool()
    async def inv_list_scan_computers(
        branchofficefilter: Optional[str] = None,
        residfilter: Optional[str] = None,
        installstatusfilter: Optional[str] = None,
        scanstatusfilter: Optional[str] = None,
        domainfilter: Optional[str] = None,
        livestatusfilter: Optional[str] = None,
    ) -> dict:
        """Retrieve all computers with their scan and installation status details."""
        return await me_client.get(Inventory.SCAN_COMPUTERS, params={
            "branchofficefilter": branchofficefilter,
            "residfilter": residfilter,
            "installstatusfilter": installstatusfilter,
            "scanstatusfilter": scanstatusfilter,
            "domainfilter": domainfilter,
            "livestatusfilter": livestatusfilter,
        })

    @mcp.tool()
    async def inv_get_computer_summary(resid: str) -> dict:
        """Retrieve inventory summary details for a specific computer by resource ID."""
        return await me_client.get(Inventory.COMP_SUMMARY, params={"resid": resid})

    @mcp.tool()
    async def inv_list_software(
        accesstypefilter: Optional[str] = None,
        licensetypefilter: Optional[str] = None,
        domainfilter: Optional[str] = None,
        compliancestatusfilter: Optional[str] = None,
    ) -> dict:
        """Retrieve the list of all software and their inventory details."""
        return await me_client.get(Inventory.SOFTWARE, params={
            "accesstypefilter": accesstypefilter,
            "licensetypefilter": licensetypefilter,
            "domainfilter": domainfilter,
            "compliancestatusfilter": compliancestatusfilter,
        })

    @mcp.tool()
    async def inv_list_prohibited_software(
        uninstallsupportfilter: Optional[str] = None,
        installerformatfilter: Optional[str] = None,
    ) -> dict:
        """Retrieve prohibited software with installation count and uninstall support status."""
        return await me_client.get(Inventory.PROHIBITED_SW, params={
            "uninstallsupportfilter": uninstallsupportfilter,
            "installerformatfilter": installerformatfilter,
        })

    @mcp.tool()
    async def inv_list_hardware(
        branchofficefilter: Optional[str] = None,
        manufacturerFilter: Optional[str] = None,
        hardwareTypeFilter: Optional[str] = None,
        domainfilter: Optional[str] = None,
    ) -> dict:
        """Retrieve the list of all computer hardware and related details."""
        return await me_client.get(Inventory.HARDWARE, params={
            "branchofficefilter": branchofficefilter,
            "manufacturerFilter": manufacturerFilter,
            "hardwareTypeFilter": hardwareTypeFilter,
            "domainfilter": domainfilter,
        })

    @mcp.tool()
    async def inv_get_installed_software(
        resid: str,
        accesstypefilter: Optional[str] = None,
        oscompatibilityfilter: Optional[str] = None,
        licensetypefilter: Optional[str] = None,
        compliancestatusfilter: Optional[str] = None,
    ) -> dict:
        """Retrieve installed software details on a specific computer by resource ID."""
        return await me_client.get(Inventory.INSTALLED_SW, params={
            "resid": resid,
            "accesstypefilter": accesstypefilter,
            "oscompatibilityfilter": oscompatibilityfilter,
            "licensetypefilter": licensetypefilter,
            "compliancestatusfilter": compliancestatusfilter,
        })

    @mcp.tool()
    async def inv_get_software_licenses(swid: str) -> dict:
        """Retrieve license details and associated computers for a given software ID."""
        return await me_client.get(Inventory.LICENSES, params={"swid": swid})

    @mcp.tool()
    async def inv_list_licensed_software(
        compliancestatusfilter: Optional[str] = None,
    ) -> dict:
        """Retrieve all licensed software entries."""
        return await me_client.get(Inventory.LICENSED_SW, params={
            "compliancestatusfilter": compliancestatusfilter,
        })

    @mcp.tool()
    async def inv_list_software_metering() -> dict:
        """Retrieve the list of software with metering enabled."""
        return await me_client.get(Inventory.SW_METERING)

    @mcp.tool()
    async def inv_get_computers_by_hardware(
        hwid: str,
        branchofficefilter: Optional[str] = None,
        customgroupfilter: Optional[str] = None,
        domainfilter: Optional[str] = None,
    ) -> dict:
        """Get computers that have a specific hardware item (by hardware ID)."""
        return await me_client.get(Inventory.COMPUTERS, params={
            "hwid": hwid,
            "branchofficefilter": branchofficefilter,
            "customgroupfilter": customgroupfilter,
            "domainfilter": domainfilter,
        })

    @mcp.tool()
    async def inv_get_computers_by_software(
        swid: str,
        branchofficefilter: Optional[str] = None,
        customgroupfilter: Optional[str] = None,
        oscompatibilityfilter: Optional[str] = None,
        livestatusfilter: Optional[str] = None,
        domainfilter: Optional[str] = None,
    ) -> dict:
        """Get computers that have a specific software installed (by software ID)."""
        return await me_client.get(Inventory.COMPUTERS, params={
            "swid": swid,
            "branchofficefilter": branchofficefilter,
            "customgroupfilter": customgroupfilter,
            "oscompatibilityfilter": oscompatibilityfilter,
            "livestatusfilter": livestatusfilter,
            "domainfilter": domainfilter,
        })

    @mcp.tool()
    async def inv_get_computers_by_licensed_software(
        licswid: str,
        licensefilter: Optional[str] = None,
        domainfilter: Optional[str] = None,
    ) -> dict:
        """Get computers associated with a specific licensed software (by licswid)."""
        return await me_client.get(Inventory.COMPUTERS, params={
            "licswid": licswid,
            "licensefilter": licensefilter,
            "domainfilter": domainfilter,
        })

    @mcp.tool()
    async def inv_get_computers_by_metering_rule(
        swmeruleid: str,
        branchofficefilter: Optional[str] = None,
        customgroupfilter: Optional[str] = None,
        domainfilter: Optional[str] = None,
    ) -> dict:
        """Get computers with software metering enabled for a specific rule (by swmeruleid)."""
        return await me_client.get(Inventory.COMPUTERS, params={
            "swmeruleid": swmeruleid,
            "branchofficefilter": branchofficefilter,
            "customgroupfilter": customgroupfilter,
            "domainfilter": domainfilter,
        })

    @mcp.tool()
    async def inv_get_computers_by_prohibited_software(
        prohibitedswid: str,
        branchofficefilter: Optional[str] = None,
        customgroupfilter: Optional[str] = None,
        oscompatibilityfilter: Optional[str] = None,
        livestatusfilter: Optional[str] = None,
        domainfilter: Optional[str] = None,
    ) -> dict:
        """Get computers where a specific prohibited software is detected (by prohibitedswid)."""
        return await me_client.get(Inventory.COMPUTERS, params={
            "prohibitedswid": prohibitedswid,
            "branchofficefilter": branchofficefilter,
            "customgroupfilter": customgroupfilter,
            "oscompatibilityfilter": oscompatibilityfilter,
            "livestatusfilter": livestatusfilter,
            "domainfilter": domainfilter,
        })

    @mcp.tool()
    async def inv_get_computers_by_license(
        licid: str,
        licensefilter: Optional[str] = None,
        domainfilter: Optional[str] = None,
    ) -> dict:
        """Get computers associated with a specific software license (by licid)."""
        return await me_client.get(Inventory.COMPUTERS, params={
            "licid": licid,
            "licensefilter": licensefilter,
            "domainfilter": domainfilter,
        })
