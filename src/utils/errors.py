class ManageEngineError(Exception):
    def __init__(self, message: str, status_code: int | None = None, response_code: str | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_code = response_code


class AuthError(Exception):
    pass


class ConfigError(Exception):
    pass


def format_error(exc: Exception) -> str:
    if isinstance(exc, ManageEngineError):
        parts = ["ManageEngine API Error"]
        if exc.status_code:
            parts.append(f"(HTTP {exc.status_code})")
        if exc.response_code:
            parts.append(f"[{exc.response_code}]")
        parts.append(str(exc))
        return " ".join(parts)
    if isinstance(exc, AuthError):
        return f"Authentication Error: {exc}"
    return str(exc)
