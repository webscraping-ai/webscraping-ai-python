# webscraping_ai

Official Python client for the [WebScraping.AI](https://webscraping.ai) API.

> **4.0 is a hard break from 3.x.** See [CHANGELOG.md](CHANGELOG.md) for the
> migration notes. If you cannot update your call sites yet, stay on
> `webscraping_ai == 3.2.1`.

## Install

```bash
pip install webscraping_ai
```

Requires Python 3.9 or newer.

## Quick start

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
| `client.account()`              | `GET /account`      | `dict`                        |

Every page-fetch method accepts the full set of API parameters as keyword
arguments: `headers`, `timeout`, `js`, `js_timeout`, `wait_for`, `proxy`,
`country`, `custom_proxy`, `device`, `error_on_404`, `error_on_redirect`,
`js_script`, plus the per-endpoint extras (`return_script_result`, `format`,
`text_format`, `return_links`, `selector`, `selectors`, `question`, `fields`).
See the [API documentation](https://webscraping.ai/docs) for the full
parameter reference.

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

## License

[MIT](LICENSE).
