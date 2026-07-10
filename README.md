# ManageEngine Endpoint Central — MCP Server

Python FastMCP server exposing 106 ManageEngine Endpoint Central REST API endpoints as MCP tools, integrated with Gemini Enterprise via Zoho OAuth 2.0.

## Architecture

```
User in Gemini Enterprise
        │
        ▼
Gemini Enterprise → Zoho OAuth (accounts.zoho.in)
        │  receives access token
        ▼
MCP Server (Cloud Run)
  Authorization: Bearer <zoho_token>  →  Authorization: Zoho-oauthtoken <zoho_token>
        │
        ▼
ManageEngine Endpoint Central API
        │
        ▼
Response back to Gemini → User
```

## Deployment

### Cloud Run (Production)

```
Service:  verse-manageengine-mcp-server
Region:   asia-south1
Project:  gemini-project-n1
URL:      https://verse-manageengine-mcp-server-852267154002.asia-south1.run.app/mcp
```

To redeploy after code changes:

```bash
gcloud run deploy verse-manageengine-mcp-server \
  --source . \
  --platform managed \
  --region asia-south1 \
  --project gemini-project-n1 \
  --account temp_wohlig.praveen@verse.in \
  --port 8080 \
  --set-env-vars "ME_BASE_URL=https://endpointcentral.manageengine.in,IAM_NAME=AaaServer,CRVIEW=CustomReportView,LOG_LEVEL=INFO,ZOHO_TOKEN_URL=https://accounts.zoho.in/oauth/v2/token"
```

### Local Development

```bash
pip install -e .
python -m src.server
```

Server starts at `http://0.0.0.0:8000/mcp`.

## Environment Variables

| Variable | Description | Required |
|---|---|---|
| `ME_BASE_URL` | ManageEngine Endpoint Central base URL | Yes |
| `IAM_NAME` | Zoho IAM name (default: `AaaServer`) | No |
| `CRVIEW` | Custom report view name | No |
| `PORT` | Server port (default: `8000`, Cloud Run uses `8080`) | No |
| `LOG_LEVEL` | Logging level (default: `INFO`) | No |
| `ZOHO_CLIENT_ID` | Zoho OAuth Client ID (for server-managed token refresh) | Optional |
| `ZOHO_CLIENT_SECRET` | Zoho OAuth Client Secret | Optional |
| `ZOHO_REFRESH_TOKEN` | Zoho OAuth Refresh Token | Optional |
| `ZOHO_TOKEN_URL` | Zoho token endpoint | No |

## OAuth Setup

Register your OAuth application at [api-console.zoho.in](https://api-console.zoho.in):

1. **Add Client** → **Server-based Application**
2. Set the **Redirect URI** to Gemini's callback URL
3. Copy **Client ID** and **Client Secret**

**Scopes** (comma-separated):

```
DesktopCentralCloud.PatchMgmt.READ,DesktopCentralCloud.PatchMgmt.Update,DesktopCentralCloud.VulnerabilityMgmt.READ,DesktopCentralCloud.DeviceControl.READ,DesktopCentralCloud.Inventory.READ,DesktopCentralCloud.SOM.READ,DesktopCentralCloud.SOM.Update,DesktopCentralCloud.CustomField.READ,DesktopCentralCloud.CustomField.Update,DesktopCentralCloud.CustomReport.READ,DesktopCentralCloud.QueryReport.READ,DesktopCentralCloud.DataEncryption.READ,DesktopCentralCloud.EndpointDLP.READ,DesktopCentralCloud.Common.READ,DesktopCentralCloud.DEX.READ
```

## Available Tools (106 total)

### Patch Management (28 tools)
`patch_get_health_policy`, `patch_list_deployment_policies`, `patch_list_downloaded`, `patch_get_scan_details`, `patch_list_all`, `patch_list_all_systems`, `patch_list_all_patch_details`, `patch_list_supported`, `patch_list_configurations`, `patch_list_applicable`, `patch_get_summary`, `patch_get_system_report`, `patch_get_system_patch_report`, `patch_get_approval_settings`, `patch_get_db_update_status`, `patch_approve`, `patch_unapprove`, `patch_decline`, `patch_decline_settings`, `patch_scan_computers`, `patch_scan_all_computers`, `patch_install`, `patch_uninstall`, `patch_apd_create`, `patch_apd_modify`, `patch_apd_delete`, `patch_apd_suspend`, `patch_apd_resume`

### Vulnerability Management (8 tools)
`vuln_list`, `vuln_list_server_misconfigurations`, `vuln_list_system_misconfigurations`, `vuln_get_system_report`, `vuln_get_system_vuln_report`, `vuln_get_server_misconfig_report`, `vuln_get_system_misconfig_report`, `vuln_get_detailed_info`

### Device Control (9 tools)
`dc_get_file_activity`, `dc_get_device_audit`, `dc_get_file_shadow`, `dc_list_unique_devices`, `dc_list_blocked_devices`, `dc_get_mac_device_status`, `dc_get_windows_device_status`, `dc_list_exempted_devices`, `dc_list_exempted_device_types`

### Custom Fields (11 tools)
`cf_list`, `cf_create`, `cf_update`, `cf_update_value`, `cf_delete`, `cf_create_data_type`, `cf_check_udt_name_exists`, `cf_get_udt_length`, `cf_update_computer_value`, `cf_get_computer_fields`, `cf_get_computer_metadata`

### Inventory (17 tools)
`inv_get_summary`, `inv_get_filter_params`, `inv_list_scan_computers`, `inv_get_computer_summary`, `inv_list_software`, `inv_list_prohibited_software`, `inv_list_hardware`, `inv_get_installed_software`, `inv_get_software_licenses`, `inv_list_licensed_software`, `inv_list_software_metering`, `inv_get_computers_by_hardware`, `inv_get_computers_by_software`, `inv_get_computers_by_licensed_software`, `inv_get_computers_by_metering_rule`, `inv_get_computers_by_prohibited_software`, `inv_get_computers_by_license`

### SOM — Systems & OS Management (6 tools)
`som_get_summary`, `som_list_computers`, `som_list_remote_offices`, `som_install_agent`, `som_uninstall_agent`, `som_remove_computer`

### Reports (4 tools)
`report_list_query_reports`, `report_get_query_data`, `report_list_custom_reports`, `report_get_custom_data`

### BitLocker / Data Encryption (3 tools)
`bitlocker_get_tpm_report`, `bitlocker_get_report`, `bitlocker_get_recovery_keys`

### Data Loss Prevention (11 tools)
`dlp_get_usb_printer_report`, `dlp_get_network_printer_report`, `dlp_get_false_positives`, `dlp_get_endpoint_activity`, `dlp_get_justifications`, `dlp_get_rules_report`, `dlp_get_email_domains_report`, `dlp_get_web_domains_report`, `dlp_get_devices_report`, `dlp_get_applications_report`, `dlp_get_data_rule_violations`

### Common (2 tools)
`common_list_custom_groups`, `common_get_server_properties`

### DEX — Digital Experience (7 tools)
`dex_get_config`, `dex_get_addon_info`, `dex_get_last_update_time`, `dex_get_next_process_time`, `dex_get_latest_experience`, `dex_get_device_profile`, `dex_get_device_nodes`
