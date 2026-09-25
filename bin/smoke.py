#!/usr/bin/env python3
"""Hand-run smoke test against the live API. Not part of the test suite —
costs ~47 credits per full sweep: 4 page calls x 1 (js=False, datacenter
proxy), question + fields 2 x 6, serp 15, data 15, data_unsupported free
(the server's 400), account free.

Every endpoint runs once through the sync ``Client``; ``account`` also
runs through ``AsyncClient`` so the async transport is exercised too.

Usage:
    WEBSCRAPING_AI_API_KEY=... python bin/smoke.py
"""

import asyncio
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple

# Load the package from the working tree, not a site-packages install.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from webscraping_ai import AsyncClient, BadRequestError, Client

TARGET = "https://example.com"
# Page tools run without JS on datacenter proxies so each call costs the documented
# 1 credit (AI tools 6); the API default js=True would cost several times more.
PAGE_OPTS: Dict[str, Any] = {"js": False, "proxy": "datacenter"}
SERP_QUERY = "coffee machines"
DATA_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


class SmokeCheckFailed(Exception):
    pass


def check(condition: bool, message: str) -> None:
    if not condition:
        raise SmokeCheckFailed(message)


def non_empty_str(name: str, result: Any) -> Any:
    check(isinstance(result, str) and bool(result.strip()), f"{name} returned an empty result")
    return result


def check_selected_multiple(result: Any) -> Any:
    matched = isinstance(result, list) and any(
        isinstance(inner, list) and len(inner) > 0 for inner in result
    )
    check(matched, f"selected_multiple returned no matches: {json.dumps(result)}")
    return result


def check_fields(result: Any) -> Any:
    check(isinstance(result, dict) and "result" in result, "fields response has no result key")
    return result


def check_serp(result: Any) -> str:
    organic: Any = result.get("organic_results") if isinstance(result, dict) else None
    check(isinstance(organic, list) and len(organic) > 0, "serp returned no organic_results")
    actual_q = (result.get("search_parameters") or {}).get("q")
    check(actual_q == SERP_QUERY, f"serp search_parameters.q was {actual_q!r}")
    first = organic[0].get("title") if isinstance(organic[0], dict) else None
    return f"{len(organic)} organic results, first: {json.dumps(first)}"


def check_data(result: Any) -> str:
    check(isinstance(result, dict), f"data returned {type(result).__name__}")
    status = result.get("parse_status")
    check(status == "ok", f"data parse_status was {status!r}")
    request_parameters = result.get("request_parameters") or {}
    provider = request_parameters.get("provider")
    check(provider == "youtube", f"data request_parameters.provider was {provider!r}")
    payload = result.get("data")
    title = payload.get("title") if isinstance(payload, dict) else None
    check(isinstance(title, str) and bool(title.strip()), "data returned no data.title")
    return f"{provider}/{request_parameters.get('type')} {status}, title: {json.dumps(title)}"


def check_data_unsupported(client: Client) -> str:
    # No client-side site filter: the URL must reach the server and get its free 400.
    try:
        client.data("https://example.com/")
    except BadRequestError as e:
        check(e.status == 400, f"data_unsupported status was {e.status}")
        check("Unsupported URL" in e.message, f"data_unsupported message was {e.message!r}")
        return f"server 400: {e.message}"
    raise SmokeCheckFailed("data on https://example.com/ unexpectedly succeeded")


def preview(result: Any) -> str:
    text = result if isinstance(result, str) else json.dumps(result)
    return re.sub(r"\s+", " ", text[:120])


def redact(text: str, api_key: str) -> str:
    text = text.replace(api_key, "[REDACTED]")
    return re.sub(r"api_key=[^&\s\"'#]*", "api_key=[REDACTED]", text)


def report(name: str, call: Callable[[], Any], api_key: str) -> bool:
    try:
        result = call()
    except Exception as e:
        status = getattr(e, "status", None)
        suffix = f" ({status})" if status is not None else ""
        message = redact(f"{type(e).__name__}{suffix}: {e}", api_key)
        print(f"  FAIL {name:<18}  {message}")
        return False
    print(f"  ok   {name:<18}  {redact(preview(result), api_key)}")
    return True


async def async_account(api_key: str) -> Any:
    async with AsyncClient(api_key) as client:
        return await client.account()


def main() -> int:
    api_key = os.environ.get("WEBSCRAPING_AI_API_KEY") or os.environ.get("WEBSCRAPING_AI_KEY")
    if not api_key:
        print("WEBSCRAPING_AI_API_KEY env var is required", file=sys.stderr)
        return 2

    with Client(api_key) as client:
        cases: List[Tuple[str, Callable[[], Any]]] = [
            ("account", client.account),
            ("html", lambda: non_empty_str("html", client.html(TARGET, **PAGE_OPTS))),
            ("text", lambda: non_empty_str("text", client.text(TARGET, **PAGE_OPTS))),
            (
                "selected",
                lambda: non_empty_str(
                    "selected", client.selected(TARGET, selector="h1", **PAGE_OPTS)
                ),
            ),
            (
                "selected_multiple",
                lambda: check_selected_multiple(
                    client.selected_multiple(TARGET, selectors=["h1", "p"], **PAGE_OPTS)
                ),
            ),
            (
                "question",
                lambda: non_empty_str(
                    "question",
                    client.question(
                        TARGET,
                        question="What is this page about? Answer in one sentence.",
                        **PAGE_OPTS,
                    ),
                ),
            ),
            (
                "fields",
                lambda: check_fields(
                    client.fields(
                        TARGET,
                        fields={"title": "Page title", "description": "Short description"},
                        **PAGE_OPTS,
                    )
                ),
            ),
            ("serp", lambda: check_serp(client.serp(SERP_QUERY))),
            ("data", lambda: check_data(client.data(DATA_URL))),
            ("data_unsupported", lambda: check_data_unsupported(client)),
            ("account (async)", lambda: asyncio.run(async_account(api_key))),
        ]
        failures = sum(not report(name, call, api_key) for name, call in cases)

    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
