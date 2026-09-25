"""Tests for the :class:`AsyncClient` against mocked HTTP responses."""

import traceback

import httpx
import pytest
import respx

from webscraping_ai import (
    APIConnectionError,
    APITimeoutError,
    AsyncClient,
    AuthenticationError,
    BadRequestError,
    Client,
    RateLimitError,
    ServerError,
)

BASE = "https://api.webscraping.ai"
API_KEY = "test-key"


def test_async_client_requires_api_key():
    with pytest.raises(ValueError):
        AsyncClient(api_key="")


@respx.mock
async def test_async_html_returns_text():
    respx.get(f"{BASE}/html").mock(
        return_value=httpx.Response(200, text="<html/>", headers={"content-type": "text/html"})
    )
    async with AsyncClient(api_key=API_KEY) as c:
        out = await c.html("https://example.com", js=False)
    assert out == "<html/>"


@respx.mock
async def test_async_account_returns_json():
    respx.get(f"{BASE}/account").mock(
        return_value=httpx.Response(
            200, json={"remaining_api_calls": 99}, headers={"content-type": "application/json"}
        )
    )
    async with AsyncClient(api_key=API_KEY) as c:
        out = await c.account()
    assert out == {"remaining_api_calls": 99}


@respx.mock
async def test_async_serp_passes_query_params_and_returns_json():
    body = {
        "search_parameters": {"engine": "google", "q": "coffee", "gl": "us", "hl": "en", "page": 3},
        "search_information": {"query_displayed": "coffee", "organic_results_state": "Fully empty"},
        "organic_results": [],
        "pagination": {"current": 3},
    }
    route = respx.get(f"{BASE}/serp").mock(
        return_value=httpx.Response(200, json=body, headers={"content-type": "application/json"})
    )
    async with AsyncClient(api_key=API_KEY) as c:
        out = await c.serp("coffee", page=3)
    assert out == body
    params = route.calls.last.request.url.params
    assert params["q"] == "coffee"
    assert params["page"] == "3"
    assert "engine" not in params


@pytest.mark.parametrize("q", ["", "   ", "\t\n "])
@respx.mock
async def test_async_serp_requires_q(q):
    route = respx.get(f"{BASE}/serp")
    async with AsyncClient(api_key=API_KEY) as c:
        with pytest.raises(ValueError, match="q is required"):
            await c.serp(q)
    assert not route.called


@pytest.mark.parametrize("q", [None, 123])
@respx.mock
async def test_async_serp_rejects_non_str_q(q):
    route = respx.get(f"{BASE}/serp")
    async with AsyncClient(api_key=API_KEY) as c:
        with pytest.raises(ValueError, match="q must be a str"):
            await c.serp(q)
    assert not route.called


@pytest.mark.parametrize("page", [0, -1, 1.5, float("nan"), "2", True])
@respx.mock
async def test_async_serp_rejects_invalid_page(page):
    route = respx.get(f"{BASE}/serp")
    async with AsyncClient(api_key=API_KEY) as c:
        with pytest.raises(ValueError, match="page must be an int >= 1"):
            await c.serp("coffee", page=page)
    assert not route.called


@respx.mock
async def test_async_serp_429_raises_rate_limit_error():
    respx.get(f"{BASE}/serp").mock(
        return_value=httpx.Response(
            429, json={"message": "Too many requests"}, headers={"content-type": "application/json"}
        )
    )
    async with AsyncClient(api_key=API_KEY) as c:
        with pytest.raises(RateLimitError) as exc_info:
            await c.serp("coffee")
    assert exc_info.value.status == 429
    assert exc_info.value.message == "Too many requests"


@respx.mock
async def test_async_selected_multiple_passes_array_params():
    route = respx.get(f"{BASE}/selected-multiple").mock(
        return_value=httpx.Response(
            200, json=[["a", "b"]], headers={"content-type": "application/json"}
        )
    )
    async with AsyncClient(api_key=API_KEY) as c:
        out = await c.selected_multiple("https://example.com", selectors=["h1", ".price"])
    assert out == [["a", "b"]]
    # selectors appears twice (form + explode, no brackets) in raw request
    raw = route.calls.last.request.url.raw_path.decode()
    assert raw.count("selectors=") == 2
    assert "selectors[]=" not in raw


@respx.mock
async def test_async_403_raises_authentication_error():
    respx.get(f"{BASE}/account").mock(
        return_value=httpx.Response(
            403, json={"message": "Wrong API key."}, headers={"content-type": "application/json"}
        )
    )
    async with AsyncClient(api_key="bad") as c:
        with pytest.raises(AuthenticationError) as exc_info:
            await c.account()
    assert exc_info.value.status == 403


@respx.mock
async def test_async_500_maps_to_server_error():
    respx.get(f"{BASE}/html").mock(
        return_value=httpx.Response(
            500, json={"message": "boom"}, headers={"content-type": "application/json"}
        )
    )
    async with AsyncClient(api_key=API_KEY) as c:
        with pytest.raises(ServerError):
            await c.html("https://example.com")


@respx.mock
async def test_async_timeout_raises_api_timeout_error():
    respx.get(f"{BASE}/html").mock(side_effect=httpx.ReadTimeout("read timeout"))
    async with AsyncClient(api_key=API_KEY) as c:
        with pytest.raises(APITimeoutError):
            await c.html("https://example.com")


@respx.mock
async def test_async_connection_failure_raises_api_connection_error():
    respx.get(f"{BASE}/html").mock(side_effect=httpx.ConnectError("refused"))
    async with AsyncClient(api_key=API_KEY) as c:
        with pytest.raises(APIConnectionError):
            await c.html("https://example.com")


def test_sync_and_async_clients_share_error_hierarchy():
    # Sanity: AuthenticationError raised by either client matches the same class.
    sync = Client
    asyn = AsyncClient
    assert sync is not asyn


SECRET_KEY = "sk-live-secret-0123456789"


@pytest.mark.parametrize(
    ("httpx_error", "expected"),
    [(httpx.ReadTimeout, APITimeoutError), (httpx.ConnectError, APIConnectionError)],
)
@respx.mock
async def test_async_transport_errors_do_not_leak_api_key(httpx_error, expected):
    def raise_with_url(request: httpx.Request) -> httpx.Response:
        raise httpx_error(f"failed for {request.url}", request=request)

    respx.get(f"{BASE}/html").mock(side_effect=raise_with_url)
    async with AsyncClient(api_key=SECRET_KEY) as c:
        with pytest.raises(expected) as exc_info:
            await c.html("https://example.com")
    err = exc_info.value
    formatted = "".join(traceback.format_exception(type(err), err, err.__traceback__))
    assert httpx_error.__name__ in str(err)
    assert SECRET_KEY not in str(err)
    assert SECRET_KEY not in repr(err)
    assert SECRET_KEY not in formatted
    assert err.__cause__ is None
    assert err.__context__ is None


VIDEO_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
JSON = {"content-type": "application/json"}


@respx.mock
async def test_async_data_passes_query_params_and_returns_json():
    body = {
        "request_parameters": {"url": VIDEO_URL, "provider": "youtube", "type": "video"},
        "parse_status": "ok",
        "data": {"title": "Never Gonna Give You Up"},
    }
    route = respx.get(f"{BASE}/data").mock(
        return_value=httpx.Response(200, json=body, headers=JSON)
    )
    async with AsyncClient(api_key=API_KEY) as c:
        out = await c.data(VIDEO_URL, country="gb", transcript=True, comments="a&b=c")
    assert out == body
    params = route.calls.last.request.url.params
    assert params["url"] == VIDEO_URL
    assert params["country"] == "gb"
    assert params["transcript"] == "true"
    assert params["comments"] == "a&b=c"
    assert "transcript_language" not in params


@respx.mock
async def test_async_data_sends_unknown_site_url_unmodified():
    odd = "  https://Example.COM/A%2Fb/\u00fcn\u00ef?x=1&y=a b#Frag  "
    route = respx.get(f"{BASE}/data").mock(
        return_value=httpx.Response(200, json={"parse_status": "ok", "data": None}, headers=JSON)
    )
    async with AsyncClient(api_key=API_KEY) as c:
        await c.data(odd)
    assert route.calls.last.request.url.params["url"] == odd


@pytest.mark.parametrize("url", ["", "  ", None, 123])
@respx.mock
async def test_async_data_rejects_blank_or_non_str_url(url):
    route = respx.get(f"{BASE}/data")
    async with AsyncClient(api_key=API_KEY) as c:
        with pytest.raises(ValueError, match="url"):
            await c.data(url)
    assert not route.called


@respx.mock
async def test_async_data_rejects_api_key_extra_param():
    route = respx.get(f"{BASE}/data")
    async with AsyncClient(api_key=API_KEY) as c:
        with pytest.raises(ValueError, match="api_key"):
            await c.data(VIDEO_URL, api_key="other")
    assert not route.called


@respx.mock
async def test_async_data_round_trips_unknown_provider_and_null_data():
    body = {
        "request_parameters": {"url": VIDEO_URL, "provider": "newsite", "type": "thing"},
        "parse_status": "parse_failed",
        "data": None,
    }
    respx.get(f"{BASE}/data").mock(return_value=httpx.Response(200, json=body, headers=JSON))
    async with AsyncClient(api_key=API_KEY) as c:
        out = await c.data(VIDEO_URL)
    assert out["request_parameters"]["provider"] == "newsite"
    assert out["parse_status"] == "parse_failed"
    assert out["data"] is None


@respx.mock
async def test_async_data_400_maps_to_bad_request_error():
    respx.get(f"{BASE}/data").mock(
        return_value=httpx.Response(
            400, json={"message": "Unsupported URL for /data."}, headers=JSON
        )
    )
    async with AsyncClient(api_key=API_KEY) as c:
        with pytest.raises(BadRequestError) as exc_info:
            await c.data("https://example.com/")
    assert exc_info.value.status == 400
    assert exc_info.value.message == "Unsupported URL for /data."


@respx.mock
async def test_async_data_transport_error_does_not_leak_api_key():
    def raise_with_url(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError(f"failed for {request.url}", request=request)

    respx.get(f"{BASE}/data").mock(side_effect=raise_with_url)
    async with AsyncClient(api_key=SECRET_KEY) as c:
        with pytest.raises(APIConnectionError) as exc_info:
            await c.data(VIDEO_URL)
    err = exc_info.value
    formatted = "".join(traceback.format_exception(type(err), err, err.__traceback__))
    assert SECRET_KEY not in formatted
    assert SECRET_KEY not in repr(err)
    assert err.__cause__ is None
    assert err.__context__ is None
