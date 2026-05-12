"""Unit tests for the error hierarchy."""

from webscraping_ai import (
    APIError,
    AuthenticationError,
    BadRequestError,
    GatewayTimeoutError,
    PaymentRequiredError,
    RateLimitError,
    ServerError,
    WebScrapingAIError,
)
from webscraping_ai._errors import STATUS_TO_ERROR


def test_api_error_exposes_full_envelope():
    err = APIError(
        message="Invalid CSS selector",
        status=400,
        status_code=None,
        status_message=None,
        body=None,
        response_body='{"message":"Invalid CSS selector"}',
    )
    assert str(err) == "Invalid CSS selector"
    assert err.status == 400
    assert err.response_body == '{"message":"Invalid CSS selector"}'


def test_status_to_error_maps_each_documented_status():
    expected = {
        400: BadRequestError,
        402: PaymentRequiredError,
        403: AuthenticationError,
        429: RateLimitError,
        500: ServerError,
        504: GatewayTimeoutError,
    }
    assert expected == STATUS_TO_ERROR


def test_every_error_subclass_inherits_from_webscraping_ai_error():
    for cls in STATUS_TO_ERROR.values():
        assert issubclass(cls, APIError)
        assert issubclass(cls, WebScrapingAIError)
