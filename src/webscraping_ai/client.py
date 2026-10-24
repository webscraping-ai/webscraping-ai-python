"""Synchronous client for the WebScraping.AI API."""

from types import TracebackType
from typing import Any, List, Mapping, Optional, Type, Union, cast

import httpx

from . import _query
from ._transport import (
    DEFAULT_BASE_URL,
    DEFAULT_TIMEOUT,
    build_data_params,
    build_params,
    build_serp_locations_params,
    build_serp_params,
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

    def serp(
        self,
        q: str,
        *,
        engine: Optional[str] = None,
        gl: Optional[str] = None,
        hl: Optional[str] = None,
        page: Optional[int] = None,
        pages: Optional[int] = None,
        location: Optional[str] = None,
        uule: Optional[str] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        radius: Optional[int] = None,
    ) -> Any:
        """``GET /serp`` — parsed search engine results for a query.

        Query-shaped rather than URL-shaped, so none of the page-fetch options
        apply. Returns the decoded ``SerpResult`` dict (``search_parameters``,
        ``search_information``, ``organic_results``, ``related_searches``,
        ``pagination``); optional keys are absent when the engine shows none.
        Billed per results page returned (see https://webscraping.ai/docs#serp);
        failed searches are not charged.

        Every search runs from one fixed location: ``location`` (a name such as
        ``"Austin,Texas,United States"`` or ``"Austin, TX"``, or an id from
        :meth:`serp_locations`), ``lat`` + ``lon`` (decimal degrees, optionally
        with ``radius`` in meters) or ``uule``; otherwise the capital of the
        ``gl`` country. So repeats and later pages are consistent. ``gl``
        defaults to the location's country. ``search_parameters`` echoes
        ``location_requested``/``location_used`` (and ``lat``, ``lon``,
        ``radius``). Combining ``location``, ``uule`` and ``lat``/``lon``, or an
        unknown location, gets a 400 from the server (not billed).

        ``pages`` (1-5) fetches that many consecutive pages, starting at
        ``page``, as one de-duplicated list: ``position`` counts through the
        combined list, each organic result gets a ``page`` key and
        ``pagination.pages_returned`` says how many pages came back.

        Raises :class:`ValueError` before any request when ``q`` is not a
        non-blank ``str``, ``page``, ``pages`` or ``radius`` is not an ``int``
        >= 1, or ``lat``/``lon`` is not a finite number. ``q`` and ``location``
        are sent untrimmed. Upper bounds (``page`` 100, ``pages`` 5,
        ``radius`` 1000) are left to the server, which rejects them with a 400
        (not billed).
        """
        query = build_serp_params(q, engine, gl, hl, page, pages, location, uule, lat, lon, radius)
        return self._request("/serp", query)

    def serp_locations(self, q: Optional[str] = None, *, limit: Optional[int] = None) -> Any:
        """``GET /serp/locations`` — look up names for :meth:`serp`'s ``location``.

        Returns a list of ``SerpLocation`` dicts, most populous first: ``id``
        (a ``str``), ``google_id``, ``google_parent_id`` (may be ``None`` or
        absent), ``name``, ``canonical_name`` (pass it, or ``id``, as
        ``location``), ``country_code``, ``target_type`` (e.g. ``"City"``; an
        open set), ``reach`` and ``gps`` (``[longitude, latitude]``).

        ``q`` is part of an English location name (e.g. ``"austin"``); without
        it the most populous locations are returned. ``limit`` caps the count
        (the server allows up to 10). Free; the API key is sent but not needed.

        Raises :class:`ValueError` before any request when ``limit`` is not an
        ``int`` >= 1.
        """
        query = build_serp_locations_params(q, limit)
        return self._request("/serp/locations", query)

    def data(
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
        shape depends on provider and type and which may be ``None``. Priced
        per site (see https://webscraping.ai/docs#data); unsupported URLs and
        failed fetches are not charged. None of the page-fetch options apply.

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
        return self._request("/data", query)

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
        return self._request(path, params)

    def _request(self, path: str, params: Mapping[str, Any]) -> Any:
        request_params = build_params(self._api_key, **params)
        encoded = _query.encode(request_params)
        wrapped: Optional[Exception] = None
        try:
            response = self._http.get(f"{self._base_url}{path}", params=cast(Any, encoded))
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
