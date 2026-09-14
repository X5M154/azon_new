from config.hosts import PAYMENT_URL
from requester.custom_requester import CustomRequester



class PaymentAPI(CustomRequester):
    """Клиент Payment API: заказы и платежи."""

    ORDERS_ENDPOINT = "/api/v1/orders"

    def __init__(self, session):
        super().__init__(session, base_url=PAYMENT_URL)

    def get_orders(self, params=None, expected_status=200):
        return self.send_request(
            "GET", self.ORDERS_ENDPOINT, params=params, expected_status=expected_status
        )
