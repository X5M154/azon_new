from config.hosts import PAYMENT_URL
from requester.custom_requester import CustomRequester


class PaymentAPI(CustomRequester):
    """Клиент Payment API: заказы и платежи."""

    ORDERS_ENDPOINT = "/api/v1/orders"

    def __init__(self, session, base_url=PAYMENT_URL):
        super().__init__(session, base_url)

    def get_orders(self, params=None, expected_status=200):
        return self.send_request(
            "GET", self.ORDERS_ENDPOINT, params=params, expected_status=expected_status,
        )

    def checkout(self, accept_price_changes=False, expected_status=201):
        return self.send_request(
            "POST",
            f"{self.ORDERS_ENDPOINT}/checkout",
            json={"accept_price_changes": accept_price_changes},
            expected_status=expected_status,
        )

    def get_order(self, order_id, expected_status=200, **kwargs):
        return self.send_request(
            "GET", f"{self.ORDERS_ENDPOINT}/{order_id}", expected_status=expected_status,
        **kwargs)

    def pay_order(self, order_id, payment_data, expected_status=201, **kwargs):
        return self.send_request(
            "POST", f"{self.ORDERS_ENDPOINT}/{order_id}/pay", json=payment_data, expected_status=expected_status,
        **kwargs)

    def cancel_order(self, order_id, expected_status=200, **kwargs):
        return self.send_request(
            "POST", f"{self.ORDERS_ENDPOINT}/{order_id}/cancel", expected_status=expected_status,
        **kwargs)

    def get_order_payments(self, order_id, expected_status=200, **kwargs):
        return self.send_request(
            "GET", f"{self.ORDERS_ENDPOINT}/{order_id}/payments", expected_status=expected_status,
        **kwargs)
