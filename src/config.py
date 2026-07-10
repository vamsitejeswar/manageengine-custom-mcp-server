from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # ManageEngine Endpoint Central base URL — no trailing slash
    me_base_url: str

    # IAM name prefix for OAuth scope strings (e.g. AaaServer)
    iam_name: str = "AaaServer"

    # Custom report view name (for POST /{crview}.ec endpoint)
    crview: str = "CustomReportView"

    # Zoho OAuth credentials for server-managed token refresh
    zoho_client_id: str = ""
    zoho_client_secret: str = ""
    zoho_refresh_token: str = ""
    zoho_token_url: str = "https://accounts.zoho.in/oauth/v2/token"

    # HTTP server
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "INFO"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
