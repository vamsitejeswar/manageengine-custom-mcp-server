from contextvars import ContextVar

# Set by BearerTokenMiddleware on every incoming HTTP request.
# Tools read this via current_token.get() to call the ManageEngine API.
current_token: ContextVar[str] = ContextVar("current_token", default="")
