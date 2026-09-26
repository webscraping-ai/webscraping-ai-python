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

[Sign up](https://webscraping.ai/auth/sign_up) to get an API key — a free
trial, no credit card required. Your key lives in the
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

# Structured data for a page on a supported site (YouTube, TikTok, X, LinkedIn, Instagram, Reddit, ...)
video = client.data("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
print(video["data"]["title"])

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

`APITimeoutError` and `APIConnectionError` are raised without chaining the
underlying httpx exception (it holds the request URL, which contains your API
key); the original exception type is named in the message instead.

### Logging and your API key

The API key travels in the query string, and httpx logs every request URL at
`INFO` on the `httpx` logger. Importing `webscraping_ai` installs a
`logging.Filter` on that logger that rewrites `api_key=<value>` to
`api_key=[REDACTED]`, so enabling `INFO` logging does not leak the key. The
filter only covers the `httpx` logger; if you log request URLs yourself, redact
them too.

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
| `client.data(...)`              | `GET /data`         | `dict` (`DataResult`)         |
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
so none of the page-fetch parameters above apply. Priced per search (see
[pricing](https://webscraping.ai/docs#serp)); failed searches are not charged. Raises `ValueError` before any request when
`q` is not a non-blank `str` or `page` is not an `int` >= 1 (the server also
rejects it with a 400, not billed; checking client-side saves the round trip).
`q` is sent as given.

| Parameter | Type  | Default    | Description                                   |
| --------- | ----- | ---------- | --------------------------------------------- |
| `q`       | `str` | —          | Search query (required)                       |
| `engine`  | `str` | `"google"` | Search engine; currently only `google`        |
| `gl`      | `str` | `"us"`     | Two-letter country code for the search        |
| `hl`      | `str` | `"en"`     | Two-letter language code for the results      |
| `page`    | `int` | `1`        | Results page number (10 per page); 1–100, server rejects > 100 with a 400 |

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

### Structured data

`client.data(url, *, country=None, transcript=None, transcript_language=None, **params)`
(and `await AsyncClient.data(...)`) returns structured JSON for a public page on a
supported site. Pass the page's normal URL; the site (`provider`) and page kind
(`type`) are detected from it. Priced per site (see
[pricing](https://webscraping.ai/docs#data)), including pages that parse empty
(`parse_status` `"parse_failed"`) or no longer exist (`"not_found"`);
unsupported URLs and failed fetches are not charged. None of the page-fetch parameters above apply.

Supported sites today include, for example, YouTube (video/channel/playlist),
TikTok (video/profile), X/Twitter (tweet/profile), LinkedIn (company/job/profile),
Instagram (post/reel/profile) and Reddit (post/subreddit/user). **More sites are
added server-side** and work with this package without an upgrade: the client
never checks the URL's site. An unsupported URL or page type returns a 400 that
is not charged (`BadRequestError`). Its message lists what is supported.

| Parameter             | Type   | Default | Description |
| --------------------- | ------ | ------- | ----------- |
| `url`                 | `str`  | —       | Page URL (required). A blank or non-str `url` raises `ValueError`; passing `url` twice (e.g. again in `**params`) raises `TypeError` |
| `country`             | `str`  | `"us"`  | Two-letter country code of the proxy used to fetch the page, `us` by default |
| `transcript`          | `bool` | `False` | YouTube videos only. Also fetch the video's transcript into `data.transcript`. It's null when no matching captions are available. If the transcript fetch itself fails, the whole request fails with a 500 and is not charged |
| `transcript_language` | `str`  | —       | Caption language to pick, e.g. `en` or `de`. Without it, English is preferred, then the first available track. If the video has no captions in that language, `data.transcript` is null |
| `**params`            | `str`, `int`, `float`, `bool` | — | Extra query params sent as-is, for provider-specific params added later (`None` omits one). `api_key` raises `ValueError` |

```python
result = client.data("https://www.youtube.com/watch?v=dQw4w9WgXcQ", transcript=True)
result["request_parameters"]  # {"url": "...", "provider": "youtube", "type": "video"}
result["parse_status"]        # "ok" (or "parse_failed" / "not_found")
result["data"]                # shape depends on provider and type; may be None

try:
    client.data("https://example.com/")
except BadRequestError as e:
    print(e.message)  # "Unsupported URL for /data. Supported sites: youtube, tiktok, ..."
```

`provider`, `type` and `parse_status` are open sets of strings, and `data` is
the decoded JSON as-is (no per-site classes), so new sites and fields show up
without a package release.

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

## Smoke testing

`bin/smoke.py` hits every endpoint once against the live API through the sync `Client`, plus one
`account` call through `AsyncClient`. It puts `src/` first on `sys.path`, so it always tests the
working tree (you still need the runtime deps, e.g. from `pip install -e ".[dev]"`). It is not
part of the pytest suite and costs ~47 credits per run: the four page calls run with `js=False`
and `proxy="datacenter"` (1 credit each), `question` and `fields` cost 6 each, and the SERP and
`/data` (YouTube video) calls are 15 each. A second `/data` call on `https://example.com/` must
come back as the server's free 400, proving there is no client-side site filter. Each case checks
the result shape, not just that no exception was raised (SERP must return organic results for the
query sent, `/data` must parse a title, `selected_multiple` must match something, and so on), and
FAIL lines redact the API key.

```bash
WEBSCRAPING_AI_API_KEY=... python bin/smoke.py
```

Each call prints an `ok` or `FAIL` line (any exception counts as a failure, and the sweep
continues); the script exits non-zero if any call fails.

## Links

- [WebScraping.AI](https://webscraping.ai) — features, pricing, signup
- [API documentation](https://webscraping.ai/docs)
- [Dashboard](https://webscraping.ai/dashboard) — API key, usage, request builder
- Other official clients: [JavaScript](https://github.com/webscraping-ai/webscraping-ai-js) · [Ruby](https://github.com/webscraping-ai/webscraping-ai-ruby) · [PHP](https://github.com/webscraping-ai/webscraping-ai-php) · [Go](https://github.com/webscraping-ai/webscraping-ai-go) · [Java](https://github.com/webscraping-ai/webscraping-ai-java) · [.NET](https://github.com/webscraping-ai/webscraping-ai-dotnet) · [CLI](https://github.com/webscraping-ai/webscraping-ai-cli) · [MCP server](https://github.com/webscraping-ai/webscraping-ai-mcp-server) · [n8n node](https://github.com/webscraping-ai/webscraping-ai-n8n)
- Support: [support@webscraping.ai](mailto:support@webscraping.ai)

## License

[MIT](LICENSE).
