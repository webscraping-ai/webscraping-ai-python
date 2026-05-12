"""Tests for the sync :class:`Client` against mocked HTTP responses."""

import httpx
import pytest
import respx

from webscraping_ai import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    Client,
    GatewayTimeoutError,
    PaymentRequiredError,
    RateLimitError,
    ServerError,
)

BASE = "https://api.webscraping.ai"
API_KEY = "test-key"


@pytest.fixture
def client():
    with Client(api_key=API_KEY) as c:
        yield c


def test_requires_api_key():
    with pytest.raises(ValueError):
        Client(api_key="")


@respx.mock
def test_html_returns_text(client):
    route = respx.get(f"{BASE}/html").mock(
        return_value=httpx.Response(
            200, text="<html></html>", headers={"content-type": "text/html"}
        )
    )
    out = client.html("https://example.com", js=False)
    assert out == "<html></html>"
    assert route.called
    request = route.calls.last.request
    assert "api_key=test-key" in request.url.query.decode()
    assert "url=https%3A%2F%2Fexample.com" in request.url.query.decode()
    assert "js=false" in request.url.query.decode()


@respx.mock
def test_text_passes_text_format_param(client):
    route = respx.get(f"{BASE}/text").mock(
        return_value=httpx.Response(
            200,
            json={"title": "T", "content": "C"},
            headers={"content-type": "application/json"},
        )
    )
    out = client.text("https://example.com", text_format="json", return_links=True)
    assert out == {"title": "T", "content": "C"}
    qs = route.calls.last.request.url.query.decode()
    assert "text_format=json" in qs
    assert "return_links=true" in qs


@respx.mock
def test_selected_returns_text(client):
    respx.get(f"{BASE}/selected").mock(
        return_value=httpx.Response(200, text="<h1>x</h1>", headers={"content-type": "text/html"})
    )
    assert client.selected("https://example.com", selector="h1") == "<h1>x</h1>"


@respx.mock
def test_question_passes_question_param(client):
    route = respx.get(f"{BASE}/ai/question").mock(
        return_value=httpx.Response(200, text="Some answer", headers={"content-type": "text/html"})
    )
    assert client.question("https://example.com", question="What?") == "Some answer"
    qs = route.calls.last.request.url.query.decode()
    assert "question=What%3F" in qs


@respx.mock
def test_fields_uses_deep_object_encoding(client):
    route = respx.get(f"{BASE}/ai/fields").mock(
        return_value=httpx.Response(
            200,
            json={"result": {"title": "T"}},
            headers={"content-type": "application/json"},
        )
    )
    out = client.fields("https://example.com", fields={"title": "Main product title"})
    assert out == {"result": {"title": "T"}}
    qs = route.calls.last.request.url.query.decode()
    assert "fields%5Btitle%5D=Main+product+title" in qs or "fields[title]=Main+product+title" in qs


@respx.mock
def test_headers_uses_deep_object_encoding(client):
    route = respx.get(f"{BASE}/html").mock(
        return_value=httpx.Response(200, text="<html/>", headers={"content-type": "text/html"})
    )
    client.html("https://example.com", headers={"Cookie": "session=abc"})
    qs = route.calls.last.request.url.query.decode()
    # respx/httpx canonicalises percent-escapes; accept either form
    assert "headers[Cookie]" in qs or "headers%5BCookie%5D" in qs


@respx.mock
def test_account_returns_json(client):
    respx.get(f"{BASE}/account").mock(
        return_value=httpx.Response(
            200,
            json={"remaining_api_calls": 1000, "remaining_concurrency": 5},
            headers={"content-type": "application/json"},
        )
    )
    out = client.account()
    assert out["remaining_api_calls"] == 1000


@pytest.mark.parametrize(
    ("status", "error_class"),
    [
        (400, BadRequestError),
        (402, PaymentRequiredError),
        (403, AuthenticationError),
        (429, RateLimitError),
        (500, ServerError),
        (504, GatewayTimeoutError),
    ],
)
@respx.mock
def test_error_status_codes_map_to_typed_errors(client, status, error_class):
    respx.get(f"{BASE}/html").mock(
        return_value=httpx.Response(
            status,
            json={"message": "boom"},
            headers={"content-type": "application/json"},
        )
    )
    with pytest.raises(error_class) as exc_info:
        client.html("https://example.com")
    assert exc_info.value.status == status
    assert exc_info.value.message == "boom"


@respx.mock
def test_500_with_target_page_details_exposes_fields(client):
    respx.get(f"{BASE}/html").mock(
        return_value=httpx.Response(
            500,
            json={
                "message": "Unexpected HTTP code on the target page",
                "status_code": 503,
                "status_message": "Service Unavailable",
                "body": "...",
            },
            headers={"content-type": "application/json"},
        )
    )
    with pytest.raises(ServerError) as exc_info:
        client.html("https://example.com")
    err = exc_info.value
    assert err.status == 500
    assert err.status_code == 503
    assert err.status_message == "Service Unavailable"
    assert err.body == "..."


@respx.mock
def test_timeout_raises_api_timeout_error(client):
    respx.get(f"{BASE}/html").mock(side_effect=httpx.ReadTimeout("read timeout"))
    with pytest.raises(APITimeoutError):
        client.html("https://example.com")


@respx.mock
def test_connection_failure_raises_api_connection_error(client):
    respx.get(f"{BASE}/html").mock(side_effect=httpx.ConnectError("refused"))
    with pytest.raises(APIConnectionError):
        client.html("https://example.com")
