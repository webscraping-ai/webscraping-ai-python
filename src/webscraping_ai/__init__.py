"""Official Python client for the WebScraping.AI API."""

from ._async_client import AsyncClient
from ._errors import (
    APIConnectionError,
    APIError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    GatewayTimeoutError,
    PaymentRequiredError,
    RateLimitError,
    ServerError,
    WebScrapingAIError,
)
from ._logging import install_httpx_log_filter
from ._version import __version__
from .client import Client

install_httpx_log_filter()

__all__ = [
    "APIConnectionError",
    "APIError",
    "APITimeoutError",
    "AsyncClient",
    "AuthenticationError",
    "BadRequestError",
    "Client",
    "GatewayTimeoutError",
    "PaymentRequiredError",
    "RateLimitError",
    "ServerError",
    "WebScrapingAIError",
    "__version__",
]
