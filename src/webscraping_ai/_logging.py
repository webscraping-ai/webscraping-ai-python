"""Keep the API key out of httpx's request logs.

httpx logs every request at INFO as ``HTTP Request: GET https://...?api_key=KEY...``.
The API key travels in the query string, so :func:`install_httpx_log_filter`
(called once when :mod:`webscraping_ai` is imported) attaches a filter to the
``httpx`` logger that rewrites ``api_key=<value>`` to ``api_key=[REDACTED]``.
"""

import logging
import re

_API_KEY_PATTERN = re.compile(r"(api_key=)[^&\s\"'#]*")
REDACTED = "[REDACTED]"


def redact(text: str) -> str:
    """Replace the value of every ``api_key=...`` query parameter in ``text``."""
    return _API_KEY_PATTERN.sub(rf"\g<1>{REDACTED}", text)


class RedactAPIKeyFilter(logging.Filter):
    """Logging filter that redacts ``api_key=<value>`` in a record's message and args."""

    def filter(self, record: logging.LogRecord) -> bool:
        try:
            message = record.getMessage()
        except Exception:
            # Malformed record (msg/args mismatch): redact the pieces we can see.
            if isinstance(record.msg, str):
                record.msg = redact(record.msg)
            if isinstance(record.args, tuple):
                record.args = tuple(redact(str(a)) for a in record.args)
            return True
        if "api_key=" in message:
            record.msg = redact(message)
            record.args = None
        return True


def install_httpx_log_filter() -> None:
    """Attach :class:`RedactAPIKeyFilter` to the ``httpx`` logger (idempotent)."""
    logger = logging.getLogger("httpx")
    if not any(isinstance(f, RedactAPIKeyFilter) for f in logger.filters):
        logger.addFilter(RedactAPIKeyFilter())
