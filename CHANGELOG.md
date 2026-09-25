# Changelog

## 4.1.0 — 2026-09-25

### Added

- `Client.serp(q, *, engine, gl, hl, page)` and `AsyncClient.serp(...)` for the
  new `GET /serp` endpoint — parsed Google search results (organic results,
  related searches, pagination) as a dict. Flat 15 credits per search. Raises
  `ValueError` before any request when `q` is not a non-blank `str` (e.g.
  `serp(123)`), or when `page` is not an `int` >= 1 (`bool`, floats, 0 and
  negatives are rejected; the server would silently fall back to page 1 and
  still bill). The server caps `page` at 100. `q` is sent untrimmed.
- `bin/smoke.py` live smoke script: asserts result shapes (not just the absence
  of exceptions), catches every exception per case, runs page tools with
  `js=False` on datacenter proxies (~32 credits per sweep), and redacts the API
  key from its output.

### Fixed

- The API key no longer leaks through transport errors. `APITimeoutError` and
  `APIConnectionError` were raised `from` the httpx exception, whose
  `request.url` carries `api_key`; they are now raised with no `__cause__` or
  `__context__`, name the original exception type in the message, and redact
  `api_key=...` from its text.
- The API key no longer leaks through httpx's `INFO` request log. Importing
  `webscraping_ai` installs a `logging.Filter` on the `httpx` logger that
  rewrites `api_key=<value>` to `api_key=[REDACTED]`.
- `_query` docstrings claimed spaces are sent as `%20`; httpx actually sends
  `+`. Docs corrected, encoding unchanged.

## 4.0.1 — 2026-07-17

### Changed

- Documentation: expanded README — API docs, signup/dashboard links, badges, and links to the other official clients.

## 4.0.0 — unreleased

Complete rewrite of the official Python client. The previous 3.x releases were
generated from the OpenAPI specification; 4.0 is a hand-authored, idiomatic
Python package with a much smaller public surface.

### Breaking changes

There is no migration shim — 3.x and 4.x are different libraries that happen
to share a name on PyPI. Stay on `webscraping_ai == 3.2.1` if you cannot
update your call sites yet.

- The class-per-tag layout (`AIApi`, `HTMLApi`, `SelectedHTMLApi`, `TextApi`,
  `AccountApi`) is gone. Use a single `Client` (or `AsyncClient`) instead.
- All endpoint methods now live directly on the client and use snake_case
  names matching the URL path:
  - `Client.html(...)`, `Client.text(...)`
  - `Client.selected(...)`, `Client.selected_multiple(...)`
  - `Client.question(...)`, `Client.fields(...)`
  - `Client.account()`
- The configuration object is gone. Pass `api_key` (and optionally `base_url`,
  `timeout`, `http_client`) directly to `Client(...)`.
- The transport stack moved from `urllib3` to `httpx`. The only runtime
  dependency is now `httpx`.
- Errors moved from a single `ApiException` to a typed hierarchy mirroring the
  documented HTTP status codes: `BadRequestError` (400), `PaymentRequiredError`
  (402), `AuthenticationError` (403), `RateLimitError` (429), `ServerError`
  (500), `GatewayTimeoutError` (504), plus `APITimeoutError` and
  `APIConnectionError` for transport failures. They all share a
  `WebScrapingAIError` base class.

### Added

- `AsyncClient` — async/await counterpart to `Client`, sharing the same method
  signatures and error hierarchy.
- Native support for the API's mixed query-string encodings (deepObject for
  `headers` / `fields`, form+explode for `selectors`, flat for everything
  else) via a custom encoder.
- `py.typed` marker; the package ships with type information.
