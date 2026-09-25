"""Asynchronous client for the WebScraping.AI API."""

from types import TracebackType
from typing import Any, List, Mapping, Optional, Type, Union, cast

import httpx

from . import _query
from ._transport import (
    DEFAULT_BASE_URL,
    DEFAULT_TIMEOUT,
    build_data_params,
    build_params,
    parse_response,
    raise_for_status,
    validate_serp_args,
    wrap_transport_error,
)
from ._version import __version__


class AsyncClient:
    """Asynchronous client for the WebScraping.AI API.

    Mirrors :class:`webscraping_ai.Client` but uses ``async def`` methods and
    an :class:`httpx.AsyncClient` under the hood. Use as an async context
    manager to guarantee connection cleanup::

        async with AsyncClient(api_key="...") as c:
            html = await c.html("https://example.com")
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        http_client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        if not api_key:
            raise ValueError("api_key is required")
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._owns_client = http_client is None
        self._http = http_client or httpx.AsyncClient(
            timeout=timeout,
            headers={"User-Agent": f"webscraping-ai-python/{__version__}"},
        )

    # ------------------------------------------------------------------
    # Endpoint methods
    # ------------------------------------------------------------------

    async def html(
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
        return await self._get(
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

    async def text(
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
        return await self._get(
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

    async def selected(
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
        return await self._get(
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

    async def selected_multiple(
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
        return await self._get(
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

    async def question(
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
        return await self._get(
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

    async def fields(
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
        return await self._get(
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

    async def serp(
        self,
        q: str,
        *,
        engine: Optional[str] = None,
        gl: Optional[str] = None,
        hl: Optional[str] = None,
        page: Optional[int] = None,
    ) -> Any:
        """``GET /serp`` — parsed search engine results for a query.

        Query-shaped rather than URL-shaped, so none of the page-fetch options
        apply. Returns the decoded ``SerpResult`` dict (``search_parameters``,
        ``search_information``, ``organic_results``, ``related_searches``,
        ``pagination``); optional keys are absent when the engine shows none.
        Flat 15 credits per search.

        Raises :class:`ValueError` before any request when ``q`` is not a
        non-blank ``str`` or ``page`` is not an ``int`` >= 1. ``q`` is sent
        untrimmed. Pages are 1-100; the server rejects a ``page`` above 100
        with a 400 (not billed).
        """
        validate_serp_args(q, page)
        return await self._get("/serp", q=q, engine=engine, gl=gl, hl=hl, page=page)

    async def data(
        self,
        url: str,
        *,
        country: Optional[str] = None,
        transcript: Optional[bool] = None,
        transcript_language: Optional[str] = None,
        **params: Any,
    ) -> Any:
        """``GET /data`` — structured JSON for a page on a supported site.

        Returns the decoded ``DataResult`` dict: ``request_parameters``
        (``url``, ``provider``, ``type``), ``parse_status`` (``"ok"``,
        ``"parse_failed"`` or ``"not_found"``, all billed) and ``data``, whose
        shape depends on provider and type and which may be ``None``. Flat 15
        credits per request. None of the page-fetch options apply.

        Supported sites (e.g. YouTube, TikTok, X/Twitter, LinkedIn, Instagram,
        Reddit) are added server-side, so the URL's site is never checked here.
        An unsupported URL or page type returns a 400 that is not charged
        (:class:`BadRequestError`); its message lists what is supported.
        ``provider``, ``type`` and ``parse_status`` are open sets of strings.

        ``country``: two-letter country code of the proxy used to fetch the
        page, ``us`` by default.

        ``transcript``: YouTube videos only. Also fetch the video's transcript
        into ``data.transcript``. It's null when no matching captions are
        available. If the transcript fetch itself fails, the whole request
        fails with a 500 and is not charged.

        ``transcript_language``: caption language to pick, e.g. ``en`` or
        ``de``. Without it, English is preferred, then the first available
        track. If the video has no captions in that language,
        ``data.transcript`` is null.

        Any other keyword arguments are sent as-is as extra query params (for
        provider-specific params added later); they must be scalars. ``api_key``
        raises :class:`ValueError`; a second ``url`` is a :class:`TypeError`
        (Python's duplicate-argument error), so neither can be overridden.

        Raises :class:`ValueError` before any request when ``url`` is not a
        non-blank ``str`` or an extra param is invalid.
        """
        query = build_data_params(url, country, transcript, transcript_language, params)
        return await self._request("/data", query)

    async def account(self) -> Any:
        """``GET /account`` — quota / billing-cycle info for the API key."""
        return await self._get("/account")

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def aclose(self) -> None:
        if self._owns_client:
            await self._http.aclose()

    async def __aenter__(self) -> "AsyncClient":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        await self.aclose()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    async def _get(self, path: str, **params: Any) -> Any:
        return await self._request(path, params)

    async def _request(self, path: str, params: Mapping[str, Any]) -> Any:
        request_params = build_params(self._api_key, **params)
        encoded = _query.encode(request_params)
        wrapped: Optional[Exception] = None
        try:
            response = await self._http.get(f"{self._base_url}{path}", params=cast(Any, encoded))
        except httpx.TransportError as exc:
            wrapped = wrap_transport_error(exc)
            if wrapped is None:
                raise
        if wrapped is not None:
            # Raised outside the except block so the httpx exception (whose
            # request URL contains the API key) is neither __cause__ nor __context__.
            raise wrapped from None
        raise_for_status(response)
        return parse_response(response)
