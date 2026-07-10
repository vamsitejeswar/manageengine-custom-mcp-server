# ManageEngine Endpoint Central — Gemini Enterprise Setup

## MCP Server URL
```
https://verse-manageengine-mcp-server-852267154002.asia-south1.run.app/mcp
```

## Name
```
ManageEngine Endpoint Central
```

## MCP Server Description
```
Provides AI-powered access to ManageEngine Endpoint Central for endpoint management. Supports patch management, vulnerability assessment, device control, software and hardware inventory, BitLocker encryption, data loss prevention (DLP), and digital experience monitoring (DEX) across Windows, Mac, and Linux endpoints.
```

## MCP Agent Instructions
```
You have access to ManageEngine Endpoint Central tools for managing organizational endpoints.

Tool categories available:
- Patch Management: check health policy, scan systems, approve and install patches
- Vulnerability Management: list and remediate vulnerabilities across endpoints
- Inventory: query hardware, software, OS, and license details
- Device Control: manage USB and peripheral device policies
- BitLocker: check drive encryption status and key escrow details
- DLP: review endpoint activity, USB printers, web/email domain policies
- DEX: get digital experience scores and device metric nodes
- Custom Fields: read and update custom computer attributes
- Reports: fetch custom and query report data
- Common: list custom groups and server properties

Rules:
- Always confirm before calling any tool that installs, patches, or modifies endpoints
- For write operations (install patches, update fields, agent actions) ask the user to confirm the target device or group first
- When a resource ID is needed, first call the relevant list tool to find it
```

---

## Authentication (OAuth 2.0)

| Field | Value |
|---|---|
| **Authorization URL** | `https://accounts.zoho.in/oauth/v2/auth` |
| **Token URL** | `https://accounts.zoho.in/oauth/v2/token` |
| **Client ID** | From Zoho API Console ([api-console.zoho.in](https://api-console.zoho.in)) |
| **Client Secret** | From Zoho API Console |
| **Scopes** | *(see below)* |
| **PKCE** | Enabled |

**Scopes** (comma-separated):
```
DesktopCentralCloud.PatchMgmt.READ,DesktopCentralCloud.PatchMgmt.Update,DesktopCentralCloud.VulnerabilityMgmt.READ,DesktopCentralCloud.DeviceControl.READ,DesktopCentralCloud.Inventory.READ,DesktopCentralCloud.SOM.READ,DesktopCentralCloud.SOM.Update,DesktopCentralCloud.CustomField.READ,DesktopCentralCloud.CustomField.Update,DesktopCentralCloud.CustomReport.READ,DesktopCentralCloud.QueryReport.READ,DesktopCentralCloud.DataEncryption.READ,DesktopCentralCloud.EndpointDLP.READ,DesktopCentralCloud.Common.READ,DesktopCentralCloud.DEX.READ
```

---

## OAuth App Registration Steps

1. Go to [api-console.zoho.in](https://api-console.zoho.in)
2. **Add Client** → **Server-based Application**
3. Fill in:
   - **Client Name**: Gemini Enterprise
   - **Homepage URL**: `https://gemini.google.com`
   - **Redirect URI**: *(paste the callback URL shown in Gemini Enterprise's OAuth config screen)*
4. Save → copy **Client ID** and **Client Secret**
5. Paste them into the Gemini Enterprise OAuth fields above

---

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `Failed to reload custom actions` | IAM policy not propagated yet | Wait 1–2 min and retry |
| `Invalid OAuth Scope` | Wrong scope prefix | Use `DesktopCentralCloud.*` scopes, not `AaaServer.*` |
| `INVALID_OAUTHTOKEN` | Token expired | Re-authenticate in Gemini Enterprise |
| `INVALID_OAUTHSCOPE` | Token issued without correct scopes | Disconnect and reconnect in GE to get fresh token with full scopes |
| `403 Forbidden` | Gemini SA missing invoker role | Grant `service-852267154002@gcp-sa-discoveryengine.iam.gserviceaccount.com` the `roles/run.invoker` role |
