#!/usr/bin/env python3
"""Hand-run smoke test against the live API. Not part of the test suite —
costs ~32 credits per full sweep (the SERP call alone is 15).

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
from typing import Any, Callable, List, Tuple

# Load the package from the working tree, not a site-packages install.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from webscraping_ai import AsyncClient, Client, WebScrapingAIError

TARGET = "https://example.com"


def serp_preview(result: Any) -> str:
    organic = (result.get("organic_results") or []) if isinstance(result, dict) else []
    first = organic[0].get("title") if organic and isinstance(organic[0], dict) else None
    return f"{len(organic)} organic results, first: {json.dumps(first)}"


def preview(result: Any) -> str:
    text = result if isinstance(result, str) else json.dumps(result)
    return re.sub(r"\s+", " ", text[:120])


def report(name: str, call: Callable[[], Any]) -> bool:
    try:
        result = call()
    except WebScrapingAIError as e:
        status = getattr(e, "status", None)
        suffix = f" ({status})" if status is not None else ""
        print(f"  FAIL {name:<18}  {type(e).__name__}{suffix}: {e}")
        return False
    print(f"  ok   {name:<18}  {preview(result)}")
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
            ("html", lambda: client.html(TARGET)),
            ("text", lambda: client.text(TARGET)),
            ("selected", lambda: client.selected(TARGET, selector="h1")),
            ("selected_multiple", lambda: client.selected_multiple(TARGET, selectors=["h1", "p"])),
            (
                "question",
                lambda: client.question(
                    TARGET, question="What is this page about? Answer in one sentence."
                ),
            ),
            (
                "fields",
                lambda: client.fields(
                    TARGET, fields={"title": "Page title", "description": "Short description"}
                ),
            ),
            ("serp", lambda: serp_preview(client.serp("coffee machines"))),
            ("account (async)", lambda: asyncio.run(async_account(api_key))),
        ]
        failures = sum(not report(name, call) for name, call in cases)

    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
