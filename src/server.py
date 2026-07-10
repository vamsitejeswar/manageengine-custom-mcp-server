"""ManageEngine Endpoint Central MCP Server.

Auth flow:
  Server-managed: ZOHO_REFRESH_TOKEN in .env → token_manager auto-refreshes
  every hour → each tool call uses "Zoho-oauthtoken <token>" header.

  Optional override: if an "Authorization: Bearer <token>" header arrives
  (e.g. from Gemini), that token is used instead for that request.
"""
import uvicorn
from fastmcp import FastMCP
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware

from src.config import settings
from src.context import current_token
from src.utils.logger import logger

from src.tools.patch import register_patch_tools
from src.tools.vulnerability import register_vulnerability_tools
from src.tools.device_control import register_device_control_tools
from src.tools.custom_field import register_custom_field_tools
from src.tools.inventory import register_inventory_tools
from src.tools.som import register_som_tools
from src.tools.reports import register_report_tools
from src.tools.bitlocker import register_bitlocker_tools
from src.tools.dlp import register_dlp_tools
from src.tools.common import register_common_tools
from src.tools.dex import register_dex_tools

mcp = FastMCP(
    name="ManageEngine Endpoint Central",
    instructions=(
        "Tools for ManageEngine Endpoint Central (formerly Desktop Central). "
        "Covers Patch Management, Vulnerability Management, Device Control, "
        "Inventory, SOM, Custom Fields, BitLocker, DLP, DEX, and Reports. "
        "All write operations (approve/decline/install patches, agent ops) are "
        "destructive — confirm before calling them."
    ),
)

register_patch_tools(mcp)
register_vulnerability_tools(mcp)
register_device_control_tools(mcp)
register_custom_field_tools(mcp)
register_inventory_tools(mcp)
register_som_tools(mcp)
register_report_tools(mcp)
register_bitlocker_tools(mcp)
register_dlp_tools(mcp)
register_common_tools(mcp)
register_dex_tools(mcp)


# ── Auth middleware ──────────────────────────────────────────────────────────

class BearerTokenMiddleware(BaseHTTPMiddleware):
    """Extracts Bearer token from Gemini and stores it in request context.

    If no Bearer token is present the server falls back to the server-managed
    Zoho token (auto-refreshed from ZOHO_REFRESH_TOKEN in .env).
    """

    async def dispatch(self, request, call_next):
        auth = request.headers.get("authorization", "")
        token = auth[7:].strip() if auth.lower().startswith("bearer ") else ""
        ctx_var = current_token.set(token)
        try:
            return await call_next(request)
        finally:
            current_token.reset(ctx_var)


# ── App factory ──────────────────────────────────────────────────────────────

def create_app():
    """Build FastMCP HTTP app with Bearer-token middleware."""
    return mcp.http_app(
        path="/mcp",
        middleware=[Middleware(BearerTokenMiddleware)],
    )


def main() -> None:
    logger.info(
        f"Starting ManageEngine Endpoint Central MCP Server "
        f"on http://{settings.host}:{settings.port}/mcp"
    )
    app = create_app()
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()
