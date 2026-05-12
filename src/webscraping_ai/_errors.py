"""Error hierarchy for the WebScraping.AI client.

The class hierarchy mirrors the API's documented response taxonomy:

- :class:`WebScrapingAIError` — base for everything raised by this library.
- :class:`APIError` — non-2xx HTTP response from the API; subclassed per status.
- :class:`APITimeoutError` / :class:`APIConnectionError` — transport-level
  failures, no HTTP response received.

The status-specific subclasses (:class:`BadRequestError` &c.) make it easy to
distinguish billing problems from rate-limits without inspecting status codes.
"""

from typing import Dict, Optional, Type


class WebScrapingAIError(Exception):
    """Base class for every error raised by the WebScraping.AI client."""


class APIError(WebScrapingAIError):
    """The API returned a non-2xx HTTP response.

    Exposes the parsed error envelope fields documented in the OpenAPI spec:
    ``message``, ``status_code``, ``status_message``, ``body`` — the latter
    three are populated when the API surfaces target-page errors as 500s.
    """

    status: int

    def __init__(
        self,
        message: str,
        *,
        status: int,
        status_code: Optional[int] = None,
        status_message: Optional[str] = None,
        body: Optional[str] = None,
        response_body: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status = status
        self.status_code = status_code
        self.status_message = status_message
        self.body = body
        self.response_body = response_body

    def __repr__(self) -> str:
        return f"{type(self).__name__}(status={self.status}, message={self.message!r})"


class BadRequestError(APIError):
    """HTTP 400 — parameters validation error."""


class PaymentRequiredError(APIError):
    """HTTP 402 — billing issue, account is out of credits."""


class AuthenticationError(APIError):
    """HTTP 403 — wrong or missing API key."""


class RateLimitError(APIError):
    """HTTP 429 — too many concurrent requests."""


class ServerError(APIError):
    """HTTP 500 — target page returned a non-2xx HTTP status or unexpected error."""


class GatewayTimeoutError(APIError):
    """HTTP 504 — server-side timeout; try increasing the ``timeout`` parameter."""


class APITimeoutError(WebScrapingAIError):
    """The request timed out before the API could respond."""


class APIConnectionError(WebScrapingAIError):
    """A transport-level error occurred while contacting the API."""


STATUS_TO_ERROR: Dict[int, Type[APIError]] = {
    400: BadRequestError,
    402: PaymentRequiredError,
    403: AuthenticationError,
    429: RateLimitError,
    500: ServerError,
    504: GatewayTimeoutError,
}
