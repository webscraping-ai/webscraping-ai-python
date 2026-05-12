"""Synchronous client for the WebScraping.AI API."""

from types import TracebackType
from typing import Any, List, Mapping, Optional, Type, Union, cast

import httpx

from . import _query
from ._transport import (
    DEFAULT_BASE_URL,
    DEFAULT_TIMEOUT,
    build_params,
    parse_response,
    raise_for_status,
    wrap_transport_error,
)
from ._version import __version__


class Client:
    """Synchronous client for the WebScraping.AI API.

    The client holds a single underlying :class:`httpx.Client`, so reuse a
    single instance across requests when possible. It can also be used as a
    context manager to guarantee connection cleanup::

        with Client(api_key="...") as c:
            html = c.html("https://example.com")
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        http_client: Optional[httpx.Client] = None,
    ) -> None:
        if not api_key:
            raise ValueError("api_key is required")
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._owns_client = http_client is None
        self._http = http_client or httpx.Client(
            timeout=timeout,
            headers={"User-Agent": f"webscraping-ai-python/{__version__}"},
        )

    # ------------------------------------------------------------------
    # Endpoint methods
    # ------------------------------------------------------------------

    def html(
        self,
        url: str,
        *,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[int] = None,
        js: Optional[bool] = None,
        js_timeout: Optional[int] = None,
        wait_for: Optional[str] = None,
        proxy: Optional[str] = None,
        country: Optional[str] = None,
        custom_proxy: Optional[str] = None,
        device: Optional[str] = None,
        error_on_404: Optional[bool] = None,
        error_on_redirect: Optional[bool] = None,
        js_script: Optional[str] = None,
        return_script_result: Optional[bool] = None,
        format: Optional[str] = None,
    ) -> Union[str, Any]:
        """``GET /html`` — full HTML of a page."""
        return self._get(
            "/html",
            url=url,
            headers=headers,
            timeout=timeout,
            js=js,
            js_timeout=js_timeout,
            wait_for=wait_for,
            proxy=proxy,
            country=country,
            custom_proxy=custom_proxy,
            device=device,
            error_on_404=error_on_404,
            error_on_redirect=error_on_redirect,
            js_script=js_script,
            return_script_result=return_script_result,
            format=format,
        )

    def text(
        self,
        url: str,
        *,
        text_format: Optional[str] = None,
        return_links: Optional[bool] = None,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[int] = None,
        js: Optional[bool] = None,
        js_timeout: Optional[int] = None,
        wait_for: Optional[str] = None,
        proxy: Optional[str] = None,
        country: Optional[str] = None,
        custom_proxy: Optional[str] = None,
        device: Optional[str] = None,
        error_on_404: Optional[bool] = None,
        error_on_redirect: Optional[bool] = None,
        js_script: Optional[str] = None,
    ) -> Union[str, Any]:
        """``GET /text`` — visible text of a page."""
        return self._get(
            "/text",
            url=url,
            text_format=text_format,
            return_links=return_links,
            headers=headers,
            timeout=timeout,
            js=js,
            js_timeout=js_timeout,
            wait_for=wait_for,
            proxy=proxy,
            country=country,
            custom_proxy=custom_proxy,
            device=device,
            error_on_404=error_on_404,
            error_on_redirect=error_on_redirect,
            js_script=js_script,
        )

    def selected(
        self,
        url: str,
        *,
        selector: Optional[str] = None,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[int] = None,
        js: Optional[bool] = None,
        js_timeout: Optional[int] = None,
        wait_for: Optional[str] = None,
        proxy: Optional[str] = None,
        country: Optional[str] = None,
        custom_proxy: Optional[str] = None,
        device: Optional[str] = None,
        error_on_404: Optional[bool] = None,
        error_on_redirect: Optional[bool] = None,
        js_script: Optional[str] = None,
        format: Optional[str] = None,
    ) -> Union[str, Any]:
        """``GET /selected`` — HTML of a single selected page area."""
        return self._get(
            "/selected",
            url=url,
            selector=selector,
            headers=headers,
            timeout=timeout,
            js=js,
            js_timeout=js_timeout,
            wait_for=wait_for,
            proxy=proxy,
            country=country,
            custom_proxy=custom_proxy,
            device=device,
            error_on_404=error_on_404,
            error_on_redirect=error_on_redirect,
            js_script=js_script,
            format=format,
        )

    def selected_multiple(
        self,
        url: str,
        *,
        selectors: Optional[List[str]] = None,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[int] = None,
        js: Optional[bool] = None,
        js_timeout: Optional[int] = None,
        wait_for: Optional[str] = None,
        proxy: Optional[str] = None,
        country: Optional[str] = None,
        custom_proxy: Optional[str] = None,
        device: Optional[str] = None,
        error_on_404: Optional[bool] = None,
        error_on_redirect: Optional[bool] = None,
        js_script: Optional[str] = None,
    ) -> Any:
        """``GET /selected-multiple`` — HTML of multiple selected page areas."""
        return self._get(
            "/selected-multiple",
            url=url,
            selectors=selectors,
            headers=headers,
            timeout=timeout,
            js=js,
            js_timeout=js_timeout,
            wait_for=wait_for,
            proxy=proxy,
            country=country,
            custom_proxy=custom_proxy,
            device=device,
            error_on_404=error_on_404,
            error_on_redirect=error_on_redirect,
            js_script=js_script,
        )

    def question(
        self,
        url: str,
        *,
        question: str,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[int] = None,
        js: Optional[bool] = None,
        js_timeout: Optional[int] = None,
        wait_for: Optional[str] = None,
        proxy: Optional[str] = None,
        country: Optional[str] = None,
        custom_proxy: Optional[str] = None,
        device: Optional[str] = None,
        error_on_404: Optional[bool] = None,
        error_on_redirect: Optional[bool] = None,
        js_script: Optional[str] = None,
        format: Optional[str] = None,
    ) -> Union[str, Any]:
        """``GET /ai/question`` — LLM-generated answer about a page."""
        return self._get(
            "/ai/question",
            url=url,
            question=question,
            headers=headers,
            timeout=timeout,
            js=js,
            js_timeout=js_timeout,
            wait_for=wait_for,
            proxy=proxy,
            country=country,
            custom_proxy=custom_proxy,
            device=device,
            error_on_404=error_on_404,
            error_on_redirect=error_on_redirect,
            js_script=js_script,
            format=format,
        )

    def fields(
        self,
        url: str,
        *,
        fields: Mapping[str, str],
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[int] = None,
        js: Optional[bool] = None,
        js_timeout: Optional[int] = None,
        wait_for: Optional[str] = None,
        proxy: Optional[str] = None,
        country: Optional[str] = None,
        custom_proxy: Optional[str] = None,
        device: Optional[str] = None,
        error_on_404: Optional[bool] = None,
        error_on_redirect: Optional[bool] = None,
        js_script: Optional[str] = None,
    ) -> Any:
        """``GET /ai/fields`` — structured fields extracted from a page.

        The live API currently wraps the result under a ``result`` key; this
        client returns the raw response, so callers should expect
        ``{"result": {"title": ..., ...}}``.
        """
        return self._get(
            "/ai/fields",
            url=url,
            fields=fields,
            headers=headers,
            timeout=timeout,
            js=js,
            js_timeout=js_timeout,
            wait_for=wait_for,
            proxy=proxy,
            country=country,
            custom_proxy=custom_proxy,
            device=device,
            error_on_404=error_on_404,
            error_on_redirect=error_on_redirect,
            js_script=js_script,
        )

    def account(self) -> Any:
        """``GET /account`` — quota / billing-cycle info for the API key."""
        return self._get("/account")

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def close(self) -> None:
        if self._owns_client:
            self._http.close()

    def __enter__(self) -> "Client":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        self.close()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _get(self, path: str, **params: Any) -> Any:
        request_params = build_params(self._api_key, **params)
        encoded = _query.encode(request_params)
        try:
            response = self._http.get(f"{self._base_url}{path}", params=cast(Any, encoded))
        except Exception as exc:
            wrapped = wrap_transport_error(exc)
            if wrapped is not None:
                raise wrapped from exc
            raise
        raise_for_status(response)
        return parse_response(response)
