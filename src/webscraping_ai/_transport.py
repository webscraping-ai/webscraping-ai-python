"""Internal helpers shared by the sync and async clients.

This module contains the response-parsing and error-mapping logic so both
:class:`webscraping_ai.Client` and :class:`webscraping_ai.AsyncClient` produce
identical results for the same API response.
"""

import json
from typing import Any, Mapping, MutableMapping, Optional

import httpx

from ._errors import (
    STATUS_TO_ERROR,
    APIConnectionError,
    APIError,
    APITimeoutError,
)

DEFAULT_BASE_URL = "https://api.webscraping.ai"
DEFAULT_TIMEOUT = 60.0


def build_params(api_key: str, **params: Any) -> MutableMapping[str, Any]:
    """Add ``api_key`` to a params mapping, dropping ``None`` entries.

    The per-endpoint encoding (deepObject/form/flat) happens in
    :mod:`webscraping_ai._query`, which is invoked by httpx via the
    ``params=`` argument with our pre-flattened list of tuples.
    """
    out: MutableMapping[str, Any] = {"api_key": api_key}
    for key, value in params.items():
        if value is not None:
            out[key] = value
    return out


def parse_response(response: httpx.Response) -> Any:
    """Return the response body parsed according to its Content-Type."""
    content_type = response.headers.get("content-type", "")
    if "application/json" in content_type:
        return response.json()
    return response.text


def raise_for_status(response: httpx.Response) -> None:
    """Raise a typed :class:`APIError` subclass for any non-2xx response."""
    if 200 <= response.status_code < 300:
        return

    error_class = STATUS_TO_ERROR.get(response.status_code, APIError)
    payload = _safe_parse_error_body(response)
    raise error_class(
        message=payload.get("message") or response.text or response.reason_phrase,
        status=response.status_code,
        status_code=payload.get("status_code"),
        status_message=payload.get("status_message"),
        body=payload.get("body"),
        response_body=response.text,
    )


def _safe_parse_error_body(response: httpx.Response) -> Mapping[str, Any]:
    text = response.text
    if not text:
        return {}
    try:
        parsed = json.loads(text)
    except (ValueError, json.JSONDecodeError):
        return {}
    if isinstance(parsed, Mapping):
        return parsed
    return {}


def wrap_transport_error(exc: Exception) -> Optional[Exception]:
    """Translate an httpx transport exception into one of our typed errors.

    Returns the wrapped exception, or ``None`` if ``exc`` is not a recognised
    httpx transport error (in which case the caller should let it propagate).
    """
    if isinstance(exc, httpx.TimeoutException):
        return APITimeoutError(str(exc) or "Request timed out")
    if isinstance(exc, httpx.TransportError):
        return APIConnectionError(str(exc) or "Connection failed")
    return None
