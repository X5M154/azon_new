import uuid
import pytest
import requests

from mocks.stubs import ProductStubs

pytestmark = [pytest.mark.mock, pytest.mark.negative]

def test_server_error_message_is_readable(wiremock, mock_products_api):
    product_id = str(uuid.uuid4())
    wiremock.add_stub(ProductStubs.server_error(product_id))

    with pytest.raises(AssertionError) as error:
        mock_products_api.get_product(product_id)

    assert "ожидали статус 200, получили 500" in str(error.value)
    assert "INTERNAL_ERROR" in str(error.value)

def test_slow_service_hits_client_timeout(wiremock, mock_products_api):
    product_id = str(uuid.uuid4())
    wiremock.add_stub(ProductStubs.slow_product(product_id, delay_ms=3000))

    with pytest.raises(requests.exceptions.ReadTimeout):
        mock_products_api.get_product(product_id, timeout=1)