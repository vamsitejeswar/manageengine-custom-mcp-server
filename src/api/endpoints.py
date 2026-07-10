"""All ManageEngine Endpoint Central API paths in one place.

Static strings for fixed paths; staticmethods for paths with URL parameters.
Tools must never hardcode a path — import from here instead.
"""


class Patch:
    HEALTH_POLICY = "/api/1.4/patch/healthpolicy"
    DEPLOYMENT_POLICIES = "/api/1.4/patch/deploymentpolicies"
    DOWNLOADED = "/api/1.4/patch/downloadedpatches"
    SCAN_DETAILS = "/api/1.4/patch/scandetails"
    DECLINE = "/api/1.4/patch/declinepatch"
    ALL_PATCHES = "/api/1.4/patch/allpatches"
    SCAN_ALL_COMPUTERS = "/api/1.4/patch/computers/scanall"
    SCAN_COMPUTERS = "/api/1.4/patch/computers/scan"
    SUMMARY = "/api/1.4/patch/summary"
    ALL_SYSTEMS = "/api/1.4/patch/allsystems"
    SYSTEM_REPORT = "/api/1.4/patch/systemreport"
    ALL_PATCH_DETAILS = "/api/1.4/patch/allpatchdetails"
    UNAPPROVE = "/api/1.4/patch/unapprovepatch"
    APPROVE = "/api/1.4/patch/approvepatch"
    DB_UPDATE_STATUS = "/api/1.4/patch/dbupdatestatus"
    VIEW_CONFIG = "/api/1.4/patch/viewconfig"
    APPROVAL_SETTINGS = "/api/1.4/patch/approvalsettings"
    SUPPORTED = "/api/1.4/patch/supportedpatches"
    INSTALL = "/api/1.4/patch/installpatch"
    UNINSTALL = "/api/1.4/patch/uninstallpatch"
    APD_CREATE = "/api/1.4/patch/createAPDTask"
    APD_MODIFY = "/api/1.4/patch/modifyAPDTask"
    APD_DELETE = "/api/1.4/patch/deleteAPDTask"
    APD_SUSPEND = "/api/1.4/patch/suspendAPDTask"
    APD_RESUME = "/api/1.4/patch/resumeAPDTask"
    # dcapi variants
    SYSTEM_PATCH_REPORT = "/dcapi/threats/systemreport/patches"
    APPLICABLE = "/dcapi/threats/patches"
    DECLINE_SETTINGS = "/dcapi/patch/settings/declinePatch/declinePatches"


class Vulnerability:
    VULNERABILITIES = "/dcapi/threats/vulnerabilities"
    SERVER_MISCONFIGS = "/dcapi/threats/servermisconfigurations"
    SYSTEM_VULN_REPORT = "/dcapi/threats/systemreport/vulnerabilities"
    SYSTEM_REPORT = "/dcapi/threats/systemreport"
    DETAILED_VULN = "/dcapi/threats/detailedinfo/vulnerabilities"
    SYSTEM_SERVER_MISCONFIG_REPORT = "/dcapi/threats/systemreport/servermisconfigurations"
    SYSTEM_MISCONFIG_REPORT = "/dcapi/threats/systemreport/systemmisconfigurations"
    SYSTEM_MISCONFIGS = "/dcapi/threats/systemmisconfigurations"


class DeviceControl:
    FILE_TRACE = "/api/1.4/reports/dcm/filetrace"
    DEVICE_AUDIT = "/api/1.4/reports/dcm/deviceaudit"
    FILE_SHADOW = "/api/1.4/reports/dcm/fileshadow"
    DEVICE_SUMMARY = "/api/1.4/reports/dcm/devicesummary"
    BLOCK_AUDIT = "/api/1.4/reports/dcm/blockdeviceaudit"
    MAC_DEV_STATUS = "/api/1.4/reports/dcm/maccomputerdevstatus"
    WIN_DEV_STATUS = "/api/1.4/reports/dcm/computerdevstatus"
    DEVICE_EXEMPTION = "/api/1.4/reports/dcm/deviceexemption"
    TYPE_EXEMPTION = "/api/1.4/reports/dcm/devicetypeexemption"


class CustomField:
    UDT_LENGTH = "/dcapi/customColumn/udtLength"
    LIST = "/dcapi/customColumn/customColumnPage"
    ADD = "/dcapi/customColumn/addCustomColumn"
    MODIFY = "/dcapi/customColumn/modifyCustomColumn"
    MODIFY_VALUE = "/dcapi/customColumn/modifyCustomColumnValue"
    REMOVE = "/dcapi/customColumn/removeCustomColumn"
    DATA_TYPE = "/dcapi/customColumn/customDataType"
    UDT_NAME_EXISTS = "/dcapi/customColumn/udtNameExists"

    @staticmethod
    def computer_update(resource_id: str) -> str:
        return f"/dcapi/customFields/computers/{resource_id}/update"

    @staticmethod
    def computer_fields(resource_id: str) -> str:
        return f"/dcapi/customColumn/{resource_id}/customFields"

    @staticmethod
    def computer_metadata(resource_id: str) -> str:
        return f"/dcapi/customFields/computers/{resource_id}"


class Inventory:
    ALL_SUMMARY = "/api/1.4/inventory/allsummary"
    FILTER_PARAMS = "/api/1.4/inventory/filterParams"
    SCAN_COMPUTERS = "/api/1.4/inventory/scancomputers"
    COMP_SUMMARY = "/api/1.4/inventory/compdetailssummary"
    SOFTWARE = "/api/1.4/inventory/software"
    PROHIBITED_SW = "/api/1.4/inventory/prohibitedsw"
    HARDWARE = "/api/1.4/inventory/hardware"
    INSTALLED_SW = "/api/1.4/inventory/installedsoftware"
    LICENSES = "/api/1.4/inventory/licenses"
    LICENSED_SW = "/api/1.4/inventory/licensesoftware"
    SW_METERING = "/api/1.4/inventory/swmeteringsummary"
    COMPUTERS = "/api/1.4/inventory/computers"


class SOM:
    SUMMARY = "/api/1.4/som/summary"
    COMPUTERS = "/api/1.4/som/computers"
    REMOTE_OFFICE = "/api/1.4/som/remoteoffice"
    INSTALL_AGENT = "/api/1.4/som/computers/installagent"
    UNINSTALL_AGENT = "/api/1.4/som/computers/uninstallagent"
    REMOVE_COMPUTER = "/api/1.4/som/computers/removecomputer"


class Reports:
    QUERY_REPORTS = "/dcapi/reports/queryReports"
    CUSTOM_REPORTS = "/dcapi/reports/customReports"

    @staticmethod
    def query_data(report_id: int) -> str:
        return f"/dcapi/reports/queryReports/{report_id}/data"

    @staticmethod
    def custom_view(crview: str) -> str:
        return f"/{crview}.ec"


class BitLocker:
    TPM_REPORT = "/api/1.4/bitlocker/tpmreport"
    REPORT = "/api/1.4/bitlocker/bitlockerreports"
    RECOVERY_KEYS = "/api/1.4/bitlocker/recoverykeydetails"


class DLP:
    USB_PRINTER = "/api/1.4/reports/dlp/networkusbprinterreport"
    NETWORK_PRINTER = "/api/1.4/reports/dlp/networkprinterreport"
    FALSE_POSITIVES = "/api/1.4/reports/dlp/networkcbfpreport"
    ENDPOINT_ACTIVITY = "/api/1.4/reports/dlp/endpointactivityreport"
    JUSTIFICATIONS = "/api/1.4/reports/dlp/justificationreport"
    RULES = "/api/1.4/reports/dlp/networkrulesreport"
    EMAIL_DOMAINS = "/api/1.4/reports/dlp/networkemailreport"
    WEB_DOMAINS = "/api/1.4/reports/dlp/networkwebdomainreport"
    DEVICES = "/api/1.4/reports/dlp/networkdevicereport"
    APPLICATIONS = "/api/1.4/reports/dlp/networkproductreport"
    DATA_RULE_VIOLATIONS = "/api/1.4/reports/dlp/networkdcfpreport"


class Common:
    CUSTOM_GROUPS = "/api/1.4/customgroup/getCGList"
    SERVER_PROPERTIES = "/api/1.4/desktop/serverproperties"


class DEX:
    META = "/intelligence/api/common/meta"
    ADDON = "/intelligence/api/addon"
    LAST_UPDATED_TIME = "/intelligence/api/score/lastUpdatedTime"
    NEXT_PROCESS_TIME = "/intelligence/api/score/nextDataProcessTime"

    @staticmethod
    def latest_experience(profile_id: str) -> str:
        return f"/intelligence/api/score/{profile_id}/latestExperience"

    @staticmethod
    def device_profile(profile_id: str, resource_id: str) -> str:
        return f"/intelligence/api/score/device/profile/{profile_id}/{resource_id}"

    @staticmethod
    def device_nodes(profile_id: str, resource_id: str) -> str:
        return f"/intelligence/api/score/device/profile/{profile_id}/{resource_id}/nodes"
