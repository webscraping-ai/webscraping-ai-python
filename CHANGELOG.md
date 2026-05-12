# Changelog

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
