"""Tests for the :class:`AsyncClient` against mocked HTTP responses."""

import httpx
import pytest
import respx

from webscraping_ai import (
    APIConnectionError,
    APITimeoutError,
    AsyncClient,
    AuthenticationError,
    Client,
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
