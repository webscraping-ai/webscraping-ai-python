"""Unit tests for the custom query-string encoder."""

from webscraping_ai import _query


def test_flat_scalars():
    assert _query.encode({"url": "https://example.com", "timeout": 5000}) == [
        ("url", "https://example.com"),
        ("timeout", "5000"),
    ]


def test_booleans_serialised_as_lowercase_strings():
    assert _query.encode({"js": True, "error_on_404": False}) == [
        ("js", "true"),
        ("error_on_404", "false"),
    ]


def test_dict_uses_deep_object_brackets():
    encoded = _query.encode({"headers": {"Cookie": "session=abc", "X-Foo": "bar"}})
    assert ("headers[Cookie]", "session=abc") in encoded
    assert ("headers[X-Foo]", "bar") in encoded


def test_list_uses_form_explode_with_no_brackets():
    encoded = _query.encode({"selectors": ["h1", ".price"]})
    assert encoded == [("selectors", "h1"), ("selectors", ".price")]


def test_none_values_are_dropped_at_every_level():
    encoded = _query.encode(
        {
            "url": "https://example.com",
            "timeout": None,
            "headers": {"Cookie": "abc", "X-Drop": None},
            "selectors": ["a", None, "b"],
        }
    )
    assert encoded == [
        ("url", "https://example.com"),
        ("headers[Cookie]", "abc"),
        ("selectors", "a"),
        ("selectors", "b"),
    ]


def test_encode_to_string_percent_encodes_spaces_as_pct20():
    s = _query.encode_to_string({"question": "What's the title?"})
    assert "%20" in s
    assert "+" not in s
    assert "%27" in s  # apostrophe


def test_string_value_is_not_iterated_as_chars():
    assert _query.encode({"selector": "h1"}) == [("selector", "h1")]


def test_fields_deep_object_style():
    encoded = _query.encode({"fields": {"title": "Main product title", "price": "Now"}})
    assert ("fields[title]", "Main product title") in encoded
    assert ("fields[price]", "Now") in encoded
