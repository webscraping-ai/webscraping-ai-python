"""Tests for the sync :class:`Client` against mocked HTTP responses."""

import logging
import traceback

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


SERP_BODY = {
    "search_parameters": {
        "engine": "google",
        "q": "coffee machines",
        "gl": "de",
        "hl": "de",
        "page": 2,
    },
    "search_information": {
        "query_displayed": "coffee machines",
        "organic_results_state": "Results for exact spelling",
    },
    "organic_results": [
        {
            "position": 1,
            "title": "Best Coffee Machines",
            "link": "https://www.example.com/best",
            "domain": "example.com",
            "displayed_link": "www.example.com \u203a Reviews",
        }
    ],
    "pagination": {"current": 2, "next": 3},
}


@respx.mock
def test_serp_passes_query_params_and_returns_json(client):
    route = respx.get(f"{BASE}/serp").mock(
        return_value=httpx.Response(
            200, json=SERP_BODY, headers={"content-type": "application/json"}
        )
    )
    out = client.serp("coffee machines", engine="google", gl="de", hl="de", page=2)
    assert out == SERP_BODY
    params = route.calls.last.request.url.params
    assert params["api_key"] == API_KEY
    assert params["q"] == "coffee machines"
    assert params["engine"] == "google"
    assert params["gl"] == "de"
    assert params["hl"] == "de"
    assert params["page"] == "2"


@respx.mock
def test_serp_omits_unset_params(client):
    route = respx.get(f"{BASE}/serp").mock(
        return_value=httpx.Response(
            200, json=SERP_BODY, headers={"content-type": "application/json"}
        )
    )
    client.serp(q="coffee machines")
    params = route.calls.last.request.url.params
    assert sorted(params.keys()) == ["api_key", "q"]


@pytest.mark.parametrize("q", ["", "   ", "\t\n "])
@respx.mock
def test_serp_requires_q(client, q):
    route = respx.get(f"{BASE}/serp")
    with pytest.raises(ValueError, match="q is required"):
        client.serp(q)
    assert not route.called


@pytest.mark.parametrize("q", [None, 123, b"coffee", ["coffee"]])
@respx.mock
def test_serp_rejects_non_str_q(client, q):
    route = respx.get(f"{BASE}/serp")
    with pytest.raises(ValueError, match="q must be a str"):
        client.serp(q)
    assert not route.called


@respx.mock
def test_serp_sends_q_untrimmed(client):
    route = respx.get(f"{BASE}/serp").mock(
        return_value=httpx.Response(
            200, json=SERP_BODY, headers={"content-type": "application/json"}
        )
    )
    client.serp("  coffee machines ")
    assert route.calls.last.request.url.params["q"] == "  coffee machines "


@pytest.mark.parametrize("page", [0, -1, 1.5, 2.0, float("nan"), "2", True, False])
@respx.mock
def test_serp_rejects_invalid_page(client, page):
    route = respx.get(f"{BASE}/serp")
    with pytest.raises(ValueError, match="page must be an int >= 1"):
        client.serp("coffee machines", page=page)
    assert not route.called


@respx.mock
def test_serp_accepts_pages_above_server_cap(client):
    route = respx.get(f"{BASE}/serp").mock(
        return_value=httpx.Response(
            200, json=SERP_BODY, headers={"content-type": "application/json"}
        )
    )
    client.serp("coffee machines", page=1)
    client.serp("coffee machines", page=150)  # server caps at 100; not the client's job
    assert route.calls.last.request.url.params["page"] == "150"


@respx.mock
def test_serp_error_message_from_message_body(client):
    respx.get(f"{BASE}/serp").mock(
        return_value=httpx.Response(
            402,
            json={"message": "Not enough credits"},
            headers={"content-type": "application/json"},
        )
    )
    with pytest.raises(PaymentRequiredError) as exc_info:
        client.serp("coffee machines")
    assert exc_info.value.status == 402
    assert exc_info.value.message == "Not enough credits"


@respx.mock
def test_serp_tolerates_non_standard_error_body(client):
    respx.get(f"{BASE}/serp").mock(
        return_value=httpx.Response(
            402, json={"error": "Not enough credits"}, headers={"content-type": "application/json"}
        )
    )
    with pytest.raises(PaymentRequiredError) as exc_info:
        client.serp("coffee machines")
    assert exc_info.value.status == 402
    assert exc_info.value.status_code is None
    assert "Not enough credits" in exc_info.value.response_body


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


SECRET_KEY = "sk-live-secret-0123456789"


def _assert_key_not_leaked(err: BaseException) -> None:
    formatted = "".join(traceback.format_exception(type(err), err, err.__traceback__))
    assert SECRET_KEY not in str(err)
    assert SECRET_KEY not in repr(err)
    assert SECRET_KEY not in formatted
    assert err.__cause__ is None
    assert err.__context__ is None


@pytest.mark.parametrize(
    ("httpx_error", "expected"),
    [(httpx.ReadTimeout, APITimeoutError), (httpx.ConnectError, APIConnectionError)],
)
@respx.mock
def test_transport_errors_do_not_leak_api_key(httpx_error, expected):
    def raise_with_url(request: httpx.Request) -> httpx.Response:
        # Worst case: the transport error's own message embeds the request URL.
        raise httpx_error(f"failed for {request.url}", request=request)

    respx.get(f"{BASE}/html").mock(side_effect=raise_with_url)
    with Client(api_key=SECRET_KEY) as c, pytest.raises(expected) as exc_info:
        c.html("https://example.com")
    err = exc_info.value
    assert httpx_error.__name__ in str(err)
    assert "api_key=[REDACTED]" in str(err)
    _assert_key_not_leaked(err)


@respx.mock
def test_httpx_request_log_redacts_api_key(caplog):
    respx.get(f"{BASE}/html").mock(
        return_value=httpx.Response(200, text="<html/>", headers={"content-type": "text/html"})
    )
    with caplog.at_level(logging.INFO, logger="httpx"), Client(api_key=SECRET_KEY) as c:
        c.html("https://example.com")
    messages = [r.getMessage() for r in caplog.records if r.name == "httpx"]
    assert messages, "expected httpx to log the request"
    assert any("api_key=[REDACTED]" in m for m in messages)
    assert all(SECRET_KEY not in m for m in messages)
    assert all(SECRET_KEY not in str(r.args) for r in caplog.records)
