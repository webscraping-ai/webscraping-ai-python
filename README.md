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

# Search from a fixed location, two results pages in one call
local = client.serp("coffee machines", location="Austin, TX", pages=2)

# Look up names for `location`
austin = client.serp_locations("austin")[0]["canonical_name"]  # "Austin,Texas,United States"

# Structured data for any public web page
page = client.data("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
print(page["data"]["title"])

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
| `client.serp_locations(...)`    | `GET /serp/locations` | `list` (`SerpLocation`)     |
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

`client.serp(q, *, engine=None, gl=None, hl=None, page=None, pages=None, location=None,
uule=None, lat=None, lon=None, radius=None)` returns parsed search engine results for a
query. It is query-shaped rather than URL-shaped, so none of the page-fetch parameters
above apply. Billed per results page returned (see
[pricing](https://webscraping.ai/docs#serp)); failed searches are not charged. Raises
`ValueError` before any request when `q` is not a non-blank `str`, `page`, `pages` or
`radius` is not an `int` >= 1, or `lat`/`lon` is not a finite number (the server also
rejects these with a 400, not billed; checking client-side saves the round trip). `q`
and `location` are sent as given.

| Parameter  | Type    | Default    | Description                                   |
| ---------- | ------- | ---------- | --------------------------------------------- |
| `q`        | `str`   | —          | Search query (required)                       |
| `engine`   | `str`   | `"google"` | Search engine; currently only `google`        |
| `gl`       | `str`   | location's country, else `"us"` | Two-letter country code for the search |
| `hl`       | `str`   | `"en"`     | Two-letter language code for the results      |
| `page`     | `int`   | `1`        | Results page number (10 per page); 1–100, server rejects > 100 with a 400 |
| `pages`    | `int`   | `1`        | Consecutive pages to fetch from `page`, 1–5, as one de-duplicated list |
| `location` | `str`   | —          | Location name (`"Austin,Texas,United States"`, `"Austin, TX"`, `"Москва"`) or an id from `serp_locations` |
| `uule`     | `str`   | —          | Google-encoded location (`w+CAIQICI…` or `a+…`) |
| `lat`      | `float` | —          | Latitude in decimal degrees (with `lon`)      |
| `lon`      | `float` | —          | Longitude in decimal degrees (with `lat`)     |
| `radius`   | `int`   | —          | Meters around `location` or `lat`/`lon`, 1–1000 |

Every search runs from one fixed location: `location`, `lat` + `lon` or `uule`,
otherwise the capital of the `gl` country, so repeats and later pages are consistent.
`gl` defaults to the location's country. Use only one of `location`, `uule` or
`lat`/`lon`; an unknown location or a bad combination gets a 400 from the server (not
billed). `lat`/`lon` are sent as plain decimals rounded to 7 places. `pages` fetches
consecutive pages as one de-duplicated list, billed per page returned.

```python
results = client.serp("coffee machines", gl="gb", page=2)
print(results["search_information"]["organic_results_state"])  # "Results for exact spelling"
for r in results["organic_results"]:
    print(r["position"], r["title"], r["link"])
print(results["pagination"])  # {"current": 2, "next": 3}

local = client.serp("coffee machines", location="Austin, TX", pages=2)
print(local["search_parameters"]["location_used"])  # "Austin,Texas,United States"
for r in local["organic_results"]:
    print(r["page"], r["position"], r["title"])  # position counts 1..N across both pages
print(local["pagination"]["pages_returned"])  # 2
```

The response dict has `search_parameters` (`engine`, `q`, `gl`, `hl`, `page`, plus
`pages` when > 1 and `location_requested`, `location_used`, `lat`, `lon`, `radius`
when relevant), `search_information` (`query_displayed`, `organic_results_state`,
optional `showing_results_for` and `total_results`), `organic_results` (`position`,
`title`, `link`, `domain`, `displayed_link`, optional `snippet` and `date`, and `page`
when `pages` > 1), optional `related_searches` (`query`), and `pagination` (`current`,
optional `next`, and `pages_returned` when `pages` > 1). `position` is 1-based within
the page, or counts through the combined list when `pages` > 1. Optional keys are
absent when the engine does not show them, so use `.get()` for those.

### SERP locations

`client.serp_locations(q=None, *, limit=None)` looks up names for `serp`'s
`location`. It is free and needs no API key (the client still sends it). Without `q`
the most populous locations are returned; `limit` caps the count (the server allows
up to 10). Raises `ValueError` before any request when `limit` is not an `int` >= 1.
`q` matches English names (e.g. `"petersburg"`); `serp`'s `location` also accepts
local names for large cities.

```python
locations = client.serp_locations("austin", limit=3)
best = locations[0]
print(best["canonical_name"], best["target_type"], best["gps"])
# Austin,Texas,United States City [-97.7431, 30.2672]   (gps is [longitude, latitude])
results = client.serp("coffee machines", location=best["canonical_name"])  # or best["id"]
```

Each entry has `id` (a `str`), `google_id`, `google_parent_id` (may be `None`),
`name`, `canonical_name`, `country_code`, `target_type` (e.g. `City`, `State`,
`Country`; an open set), `reach` (approximate population) and `gps`.

### Structured data

`client.data(url, *, country=None, transcript=None, transcript_language=None, **params)`
(and `await AsyncClient.data(...)`) returns structured JSON for any public web page.
Pass the page's normal URL; the site the page belongs to (`provider`, e.g.
`toscrape.com`) and the kind of page (`type`, e.g. `product`) are detected from it.
Some popular sites have dedicated parsers with fixed fields; for any other site,
an AI model learns the structure of each kind of page the first time it is
requested, and from then on pages of that kind on that site return data straight
away for every user. See [pricing](https://webscraping.ai/docs#data); pages that
parse empty (`parse_status` `"parse_failed"`) or no longer exist (`"not_found"`)
are charged, failed fetches are not. The client never checks the URL's site.

| Parameter             | Type   | Default | Description |
| --------------------- | ------ | ------- | ----------- |
| `url`                 | `str`  | —       | Page URL (required). A blank or non-str `url` raises `ValueError`; passing `url` twice (e.g. again in `**params`) raises `TypeError` |
| `country`             | `str`  | `"us"`  | Two-letter country code of the proxy used to fetch the page, `us` by default |
| `transcript`          | `bool` | `False` | Video pages on sites with a dedicated parser only. Also fetch the video's transcript into `data.transcript`. It's null when no matching captions are available. If the transcript fetch itself fails, the whole request fails with a 500 and is not charged |
| `transcript_language` | `str`  | —       | With `transcript=True`. Caption language to pick, e.g. `en` or `de`. Without it, English is preferred, then the first available track. If the video has no captions in that language, `data.transcript` is null |
| `**params`            | `str`, `int`, `float`, `bool` | — | Extra query params sent as-is (`None` omits one). For pages without a dedicated parser the API also accepts `timeout`, `js_timeout`, `wait_for` and `device`, which can be passed this way. There are no `js` or `proxy` options: `/data` renders pages with JavaScript where the site needs it and always uses `proxy=auto`. `api_key` raises `ValueError` |

```python
result = client.data("https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
result["request_parameters"]  # {"url": "...", "provider": "toscrape.com", "type": "product"}
result["parse_status"]        # "ok" (or "parse_failed" / "not_found")
result["data"]                # {"title": "A Light in the Attic", "price": 51.77, "currency": "GBP", ...}
```

`provider`, `type` and `parse_status` are open sets of strings, and `data` is
the decoded JSON as-is (no per-site classes), so new sites and fields show up
without a package release.

**First request for a new kind of page.** The first request for a new kind of
page also learns its structure, so it can take up to about 45 seconds; keep the
client timeout (`Client(timeout=...)`, 60 seconds by default) above that. When
learning takes longer, or another request is already learning that site, the
API answers `503` with
`{"message": "...", "error_code": "structure_processing", "retry_after": 30}`
(plus a `Retry-After` header). It is not charged. There is no dedicated error
class for 503, so it raises the base `APIError` with `e.status == 503` (the
`error_code` and `retry_after` are in the raw JSON of `e.response_body`). Wait
`retry_after` seconds and call again; the retry can return data (if
learning failed meanwhile, it may learn again or answer the 422 below):

```python
import json
import time

from webscraping_ai import APIError

try:
    result = client.data(url)
except APIError as e:
    if e.status != 503:
        raise
    time.sleep(json.loads(e.response_body).get("retry_after", 30))
    result = client.data(url)
```

**No structured data found (HTTP 422).** When a page has nothing to extract
(an empty page, a login wall), the API answers `422` with
`error_code: "structure_unavailable"`, not charged. There is no dedicated error
class for 422, so it raises the base `APIError` with `e.status == 422` (the
`error_code` is in the raw JSON of `e.response_body`); use `client.fields(...)`
for such pages instead.

**Other `/data` errors.** Redirects within the same site (http→https, `www`,
trailing slash) are followed; a redirect to another site answers `500`
(`ServerError`) with `error_code: "target_redirect"` (the target is in the
message), not charged.
Starting too many new kinds of pages in an hour answers `429` with
`error_code: "rate_limited"` (`RateLimitError`).

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
part of the pytest suite and uses real credits: the four page calls run with `js=False` and
`proxy="datacenter"` to keep the cost down, the two SERP calls (one plain, one with
`location="Austin, TX", pages=2`) are billed per results page returned, the `/data` call uses a
page on a site with a dedicated parser (see [pricing](https://webscraping.ai/docs#data)), and
`serp_locations` and `account` are free. A second `/data` call on `https://example.com/` (a site
without a dedicated parser) passes if it returns a success envelope, a 503 `structure_processing`
error, or a 422 `structure_unavailable` error. Each case checks the result shape, not just that no
exception was raised (SERP must return organic results for the query sent, the located SERP must
report an Austin `location_used`, `serp_locations("austin")` must put Austin first, `/data` must
parse a title, `selected_multiple` must match something, and so on), and FAIL lines redact the API
key.

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
