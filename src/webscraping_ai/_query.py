"""Query-string encoding for the WebScraping.AI API.

The API mixes three OpenAPI query-string styles, and no stock encoder handles
the combination correctly:

- ``deepObject`` + ``explode`` for ``headers`` and ``fields`` dicts
  → ``headers[Cookie]=foo&fields[title]=bar``
- ``form`` + ``explode`` for the ``selectors`` array
  → ``selectors=h1&selectors=.price`` (no ``[]`` brackets)
- flat ``key=value`` for everything else, with booleans serialised as
  the strings ``"true"`` / ``"false"``.

``None`` values are dropped at every level.

:func:`encode` does no percent-encoding: the clients hand its (key, value)
pairs to httpx, which form-encodes them on the wire, so spaces are sent as
``+`` (and a literal ``+`` as ``%2B``). The API decodes both forms the same
way. :func:`encode_to_string` is a separate helper that percent-encodes
spaces as ``%20``; the clients do not use it for requests.
"""

from typing import Any, List, Mapping, Sequence, Tuple
from urllib.parse import quote

Params = List[Tuple[str, str]]


def _quote(value: str) -> str:
    return quote(value, safe="")


def _scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def encode(params: Mapping[str, Any]) -> Params:
    """Encode a mapping of API parameters into a list of (key, value) pairs.

    The output values are *not* percent-encoded. httpx accepts a list of
    tuples for ``params=`` and applies its own form encoding (spaces become
    ``+``), so returning raw values avoids double-encoding.

    Use :func:`encode_to_string` to get a fully percent-encoded query string.
    """
    out: Params = []
    for key, value in params.items():
        if value is None:
            continue
        if isinstance(value, Mapping):
            for sub_key, sub_value in value.items():
                if sub_value is None:
                    continue
                out.append((f"{key}[{sub_key}]", _scalar(sub_value)))
        elif isinstance(value, (list, tuple)) and not isinstance(value, (str, bytes)):
            for item in value:
                if item is None:
                    continue
                out.append((key, _scalar(item)))
        else:
            out.append((key, _scalar(value)))
    return out


def encode_to_string(params: Mapping[str, Any]) -> str:
    """Return a fully percent-encoded query string (without leading ``?``).

    Spaces are encoded as ``%20`` here, unlike the ``+`` httpx sends for
    requests built from :func:`encode`. For callers that want explicit control
    over the URL rather than letting httpx assemble it.
    """
    parts: List[str] = []
    for key, value in encode(params):
        parts.append(f"{_quote(key)}={_quote(value)}")
    return "&".join(parts)


# Keep a non-public alias for callers that prefer a sequence return type.
def encode_pairs(params: Mapping[str, Any]) -> Sequence[Tuple[str, str]]:
    return encode(params)
