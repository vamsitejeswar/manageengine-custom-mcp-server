from typing import Optional
from fastmcp import FastMCP
from src.api.client import me_client
from src.api.endpoints import BitLocker


def register_bitlocker_tools(mcp: FastMCP) -> None:

    @mcp.tool()
    async def bitlocker_get_tpm_report(
        residfilter: Optional[str] = None,
        domainfilter: Optional[str] = None,
    ) -> dict:
        """Retrieve TPM (Trusted Platform Module) details across computers."""
        return await me_client.get(BitLocker.TPM_REPORT, params={
            "residfilter": residfilter,
            "domainfilter": domainfilter,
        })

    @mcp.tool()
    async def bitlocker_get_report(
        residfilter: Optional[str] = None,
        domainfilter: Optional[str] = None,
    ) -> dict:
        """Retrieve drive-level BitLocker encryption details across computers."""
        return await me_client.get(BitLocker.REPORT, params={
            "residfilter": residfilter,
            "domainfilter": domainfilter,
        })

    @mcp.tool()
    async def bitlocker_get_recovery_keys(
        keyProtectorId: Optional[str] = None,
        compName: Optional[str] = None,
        domainfilter: Optional[str] = None,
    ) -> dict:
        """Retrieve BitLocker recovery keys, optionally filtered by computer or key protector ID."""
        return await me_client.get(BitLocker.RECOVERY_KEYS, params={
            "keyProtectorId": keyProtectorId,
            "compName": compName,
            "domainfilter": domainfilter,
        })
