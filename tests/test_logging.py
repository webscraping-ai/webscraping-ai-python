"""Tests for the httpx log filter that redacts the API key."""

import logging

import webscraping_ai  # noqa: F401  (importing installs the filter)
from webscraping_ai._logging import RedactAPIKeyFilter, install_httpx_log_filter, redact

KEY = "sk-live-secret-0123456789"


def _record(msg, args):
    return logging.LogRecord("httpx", logging.INFO, __file__, 1, msg, args, None)


def test_redact_replaces_api_key_values():
    url = f"https://api.webscraping.ai/html?url=x&api_key={KEY}&js=false"
    assert redact(url) == "https://api.webscraping.ai/html?url=x&api_key=[REDACTED]&js=false"


def test_filter_redacts_key_in_args():
    record = _record('HTTP Request: %s %s "%s"', ("GET", f"https://h/p?api_key={KEY}", "200 OK"))
    assert RedactAPIKeyFilter().filter(record) is True
    assert KEY not in record.getMessage()
    assert "api_key=[REDACTED]" in record.getMessage()


def test_filter_redacts_key_in_msg():
    record = _record(f"GET https://h/p?api_key={KEY}", None)
    RedactAPIKeyFilter().filter(record)
    assert KEY not in record.getMessage()


def test_filter_leaves_other_records_untouched():
    record = _record("hello %s", ("world",))
    RedactAPIKeyFilter().filter(record)
    assert record.msg == "hello %s"
    assert record.args == ("world",)


def test_filter_handles_malformed_records():
    record = _record(f"api_key={KEY} %s %s", (f"api_key={KEY}",))
    assert RedactAPIKeyFilter().filter(record) is True
    assert KEY not in record.msg
    assert KEY not in str(record.args)


def test_filter_installed_once_on_httpx_logger():
    install_httpx_log_filter()
    install_httpx_log_filter()
    filters = [f for f in logging.getLogger("httpx").filters if isinstance(f, RedactAPIKeyFilter)]
    assert len(filters) == 1
