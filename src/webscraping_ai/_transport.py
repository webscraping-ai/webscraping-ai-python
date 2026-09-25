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
from ._logging import redact

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

    The returned error must be raised *outside* the ``except`` block that
    caught ``exc`` (see the clients' ``_get``), so it carries neither
    ``__cause__`` nor ``__context__``: the httpx exception holds the request,
    whose URL contains the API key. The original exception type is kept in
    the message instead, and any ``api_key=...`` in its text is redacted.
    """
    if isinstance(exc, httpx.TimeoutException):
        return APITimeoutError(_describe(exc, "Request timed out"))
    if isinstance(exc, httpx.TransportError):
        return APIConnectionError(_describe(exc, "Connection failed"))
    return None


def _describe(exc: Exception, fallback: str) -> str:
    detail = redact(str(exc)) or fallback
    return f"{type(exc).__name__}: {detail}"


def validate_serp_args(q: Any, page: Any) -> None:
    """Reject ``serp`` arguments the API would misinterpret, before any request.

    ``q`` must be a non-blank ``str`` (it is sent untrimmed). ``page``, when
    given, must be an ``int`` >= 1 (``bool`` is rejected): the server also
    rejects an invalid page with a 400 (not billed); checking client-side saves
    the round trip. Pages above 100 are left to the server, which rejects them
    with a 400.
    """
    if not isinstance(q, str):
        raise ValueError(f"q must be a str, got {type(q).__name__}")
    if not q.strip():
        raise ValueError("q is required")
    if page is not None and (isinstance(page, bool) or not isinstance(page, int) or page < 1):
        raise ValueError(f"page must be an int >= 1, got {page!r}")
