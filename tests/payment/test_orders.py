import pytest

from models.orders import OrdersPage, OrderResponse, PaymentResponse
from data.orders import OrderData, DECLINED_CARD
from tests.conftest import api_manager
from utils.marks import requires_admin

pytestmark = [pytest.mark.contract, pytest.mark.payment, requires_admin]

class TestOrders:

    def test_new_user_orders_match_contract(self, api_manager, authenticated_user):
        response = api_manager.payment_api.get_orders()

        orders = OrdersPage.model_validate(response.json())
        assert orders.total == 0
        assert orders.items == []

    def test_successful_pay(self, api_manager, created_order):

        payment_data = OrderData.payment()

        pay = api_manager.payment_api.pay_order(created_order.id, payment_data=payment_data)
        paid = PaymentResponse.model_validate(pay.json())
        assert paid.status == "SUCCEEDED"

        response = api_manager.payment_api.get_order(created_order.id)

        order = OrderResponse.model_validate(response.json())
        assert order.status == "PAID"

    @pytest.mark.negative
    def test_declined_card_pay(self, api_manager, created_order):

        payment_data = OrderData.payment(card_number=DECLINED_CARD)

        response = api_manager.payment_api.pay_order(created_order.id, payment_data=payment_data, expected_status=402)
        assert response.json()["error"]["code"] == "PAYMENT_DECLINED"
        assert response.json()["error"]["details"][0]["decline_code"] == "card_declined"

        order = api_manager.payment_api.get_order(created_order.id)
        assert order.json()["status"] == "AWAITING_PAYMENT"


    @pytest.mark.negative
    def test_payment_paid_order(self, api_manager, created_order):

        payment_data = OrderData.payment()

        api_manager.payment_api.pay_order(created_order.id, payment_data=payment_data)

        response = api_manager.payment_api.pay_order(created_order.id, payment_data=payment_data, expected_status=409)
        assert response.json()["error"]["code"] == "ORDER_NOT_PAYABLE"

    @pytest.mark.negative
    def test_cancel_paid_order(self, api_manager, created_order):
        payment_data = OrderData.payment()

        api_manager.payment_api.pay_order(created_order.id, payment_data=payment_data)

        response = api_manager.payment_api.cancel_order(created_order.id, expected_status=409)
        assert response.json()["error"]["code"] == "INVALID_ORDER_STATUS"

    @pytest.mark.negative
    def test_get_wrong_order(self, api_manager, created_order, second_user):

        response = second_user.payment_api.get_order(created_order.id, expected_status=404)

        assert response.json()["error"]["code"] == "ORDER_NOT_FOUND"

    @pytest.mark.negative
    def test_empty_cart(self, api_manager, authenticated_user):

        response = api_manager.payment_api.checkout(expected_status=400)

        assert response.json()["error"]["code"] == "CART_EMPTY"