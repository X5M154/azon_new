from data.orders import OrderData
from mocks.stubs import PaymentStubs
import pytest


ORDER_ID = "11111111-1111-1111-1111-111111111111"

pytestmark = [pytest.mark.mock, pytest.mark.negative, pytest.mark.payment]

def test_service_unavailable(wiremock, mock_payment_api):
    wiremock.add_stub(PaymentStubs.service_unavailable(ORDER_ID))
    payment_data = OrderData.payment()

    response = mock_payment_api.pay_order(ORDER_ID, payment_data, expected_status=503)

    assert response.status_code == 503