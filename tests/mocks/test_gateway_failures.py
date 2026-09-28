import uuid

import pytest
import requests

from mocks.stubs import JSON_HEADERS, PRODUCTS_ENDPOINT, error_body, product_body

pytestmark = [pytest.mark.mock, pytest.mark.negative]

def gateway_error(product_id):
    return {
        "request": {"method": "GET", "urlPath": f"{PRODUCTS_ENDPOINT}/{product_id}"},
        "response": {
            "status": 503,
            "headers": JSON_HEADERS,
            "jsonBody": error_body("GATEWAY_ERROR", "Upstream is unavailable"),
        },
    }


def very_slow_product(product_id, delay_ms=5000):
    return {
        "request": {"method": "GET", "urlPath": f"{PRODUCTS_ENDPOINT}/{product_id}"},
        "response": {
            "status": 200,
            "headers": JSON_HEADERS,
            "jsonBody": product_body(product_id),
            "fixedDelayMilliseconds": delay_ms,
        },
    }


def test_gateway_error_is_reported_clearly(wiremock, mock_products_api):
    product_id = str(uuid.uuid4())
    wiremock.add_stub(gateway_error(product_id))

    with pytest.raises(AssertionError) as error:
        mock_products_api.get_product(product_id)

    assert "ожидали статус 200, получили 503" in str(error.value)
    assert "GATEWAY_ERROR" in str(error.value)


def test_client_gives_up_after_two_seconds(wiremock, mock_products_api):
    product_id = str(uuid.uuid4())
    wiremock.add_stub(very_slow_product(product_id, delay_ms=5000))

    with pytest.raises(requests.exceptions.ReadTimeout):
        mock_products_api.get_product(product_id, timeout=2)