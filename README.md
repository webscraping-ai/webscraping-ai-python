# webscraping_ai

[![PyPI](https://img.shields.io/pypi/v/webscraping_ai.svg)](https://pypi.org/project/webscraping_ai/)
[![CI](https://github.com/webscraping-ai/webscraping-ai-python/actions/workflows/ci.yml/badge.svg)](https://github.com/webscraping-ai/webscraping-ai-python/actions/workflows/ci.yml)

Official Python client for the [WebScraping.AI](https://webscraping.ai) API —
web scraping with Chromium JavaScript rendering, rotating
datacenter/residential/stealth proxies, and AI-powered question answering and
structured field extraction on any page. Sync and async clients included. See
the [API documentation](https://webscraping.ai/docs) for the full parameter
reference.

> **4.0 is a hard break from 3.x.** See [CHANGELOG.md](CHANGELOG.md) for the
> migration notes. If you cannot update your call sites yet, stay on
> `webscraping_ai == 3.2.1`.

## Install

```bash
pip install webscraping_ai
```

Requires Python 3.9 or newer.

## Quick start

[Sign up](https://webscraping.ai/auth/sign_up) to get an API key — the free
trial includes 2,000 credits, no credit card required. Your key lives in the
[dashboard](https://webscraping.ai/dashboard).

```python
from webscraping_ai import Client

client = Client(api_key="YOUR_API_KEY")

# Page HTML
html = client.html("https://example.com")

# Visible text, optionally as a structured JSON response
text = client.text("https://example.com", text_format="json", return_links=True)

# CSS-selected HTML
heading = client.selected("https://example.com", selector="h1")
multiple = client.selected_multiple("https://example.com", selectors=["h1", "p"])

# LLM-powered helpers
answer = client.question("https://example.com", question="What is the page title?")
fields = client.fields(
    "https://example.com",
    fields={"title": "Main product title", "price": "Current product price"},
)

# Google search results (SERP) for a query
results = client.serp("coffee machines", gl="us", hl="en", page=1)

# Account quota
info = client.account()
```

The client is also a context manager, which closes the underlying connection
pool on exit:

```python
with Client(api_key="...") as client:
    client.html("https://example.com")
```

## Async usage

`AsyncClient` mirrors `Client` but uses `async def` methods backed by
`httpx.AsyncClient`:

```python
import asyncio
from webscraping_ai import AsyncClient

async def main():
    async with AsyncClient(api_key="YOUR_API_KEY") as client:
        html = await client.html("https://example.com")
        print(html)

asyncio.run(main())
```

## Error handling

Every non-2xx response is mapped to a typed exception so you can `except` on
the situation you actually care about rather than parsing status codes:

```python
from webscraping_ai import (
    Client,
    AuthenticationError,
    RateLimitError,
    PaymentRequiredError,
    APITimeoutError,
    APIConnectionError,
)

client = Client(api_key="YOUR_API_KEY")

try:
    client.html("https://example.com")
except AuthenticationError:
    ...  # 403 — wrong or missing API key
except PaymentRequiredError:
    ...  # 402 — out of credits
except RateLimitError:
    ...  # 429 — too many concurrent requests
except APITimeoutError:
    ...  # request did not complete in time
except APIConnectionError:
    ...  # transport-level failure
```

All exceptions inherit from `WebScrapingAIError`, so you can catch everything
the client raises with a single `except` if you prefer. API errors expose the
parsed error envelope (`message`, `status`, `status_code`, `status_message`,
`body`, `response_body`).

## Endpoint reference

| Method                          | HTTP route          | Returns                       |
| ------------------------------- | ------------------- | ----------------------------- |
| `client.html(...)`              | `GET /html`         | `str` (page HTML)             |
| `client.text(...)`              | `GET /text`         | `str` or `dict` (JSON)        |
| `client.selected(...)`          | `GET /selected`     | `str`                         |
| `client.selected_multiple(...)` | `GET /selected-multiple` | `list`                   |
| `client.question(...)`          | `GET /ai/question`  | `str`                         |
| `client.fields(...)`            | `GET /ai/fields`    | `dict` (wrapped under `result`) |
| `client.serp(...)`              | `GET /serp`         | `dict` (`SerpResult`)         |
| `client.account()`              | `GET /account`      | `dict`                        |

Every page-fetch method accepts the full set of API parameters as keyword
arguments: `headers`, `timeout`, `js`, `js_timeout`, `wait_for`, `proxy`,
`country`, `custom_proxy`, `device`, `error_on_404`, `error_on_redirect`,
`js_script`, plus the per-endpoint extras (`return_script_result`, `format`,
`text_format`, `return_links`, `selector`, `selectors`, `question`, `fields`).
See the [API documentation](https://webscraping.ai/docs) for the full
parameter reference.

### SERP

`client.serp(q, *, engine=None, gl=None, hl=None, page=None)` returns parsed
search engine results for a query. It is query-shaped rather than URL-shaped,
so none of the page-fetch parameters above apply. Flat 15 credits per search;
failed searches are not charged. Raises `ValueError` when `q` is blank.

| Parameter | Type  | Default    | Description                                   |
| --------- | ----- | ---------- | --------------------------------------------- |
| `q`       | `str` | —          | Search query (required)                       |
| `engine`  | `str` | `"google"` | Search engine; currently only `google`        |
| `gl`      | `str` | `"us"`     | Two-letter country code for the search        |
| `hl`      | `str` | `"en"`     | Two-letter language code for the results      |
| `page`    | `int` | `1`        | Results page number (10 results per page)     |

```python
results = client.serp("coffee machines", gl="gb", page=2)
print(results["search_information"]["organic_results_state"])  # "Results for exact spelling"
for r in results["organic_results"]:
    print(r["position"], r["title"], r["link"])
print(results["pagination"])  # {"current": 2, "next": 3}
```

The response dict has `search_parameters` (`engine`, `q`, `gl`, `hl`, `page`),
`search_information` (`query_displayed`, `organic_results_state`, optional
`showing_results_for` and `total_results`), `organic_results` (`position` —
1-based within the page — `title`, `link`, `domain`, `displayed_link`,
optional `snippet` and `date`), optional `related_searches` (`query`), and
`pagination` (`current`, optional `next`). Optional keys are absent when the
engine does not show them, so use `.get()` for those.

### API response-shape notes

Two endpoints return shapes that differ from the OpenAPI spec examples. The
client returns the raw response unchanged, so:

- `/ai/fields` wraps the extracted fields under a `result` key:
  `{"result": {"title": "...", "price": "..."}}`.
- `/selected-multiple` returns `list[list[str]]`, not a flat `list[str]`.

## Development

```bash
mise install                    # or use python 3.13 from any source
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check .
mypy src/webscraping_ai
```

## Links

- [WebScraping.AI](https://webscraping.ai) — features, pricing, signup
- [API documentation](https://webscraping.ai/docs)
- [Dashboard](https://webscraping.ai/dashboard) — API key, usage, request builder
- Other official clients: [JavaScript](https://github.com/webscraping-ai/webscraping-ai-js) · [Ruby](https://github.com/webscraping-ai/webscraping-ai-ruby) · [PHP](https://github.com/webscraping-ai/webscraping-ai-php) · [Go](https://github.com/webscraping-ai/webscraping-ai-go) · [Java](https://github.com/webscraping-ai/webscraping-ai-java) · [.NET](https://github.com/webscraping-ai/webscraping-ai-dotnet) · [CLI](https://github.com/webscraping-ai/webscraping-ai-cli) · [MCP server](https://github.com/webscraping-ai/webscraping-ai-mcp-server) · [n8n node](https://github.com/webscraping-ai/webscraping-ai-n8n)
- Support: [support@webscraping.ai](mailto:support@webscraping.ai)

## License

[MIT](LICENSE).
