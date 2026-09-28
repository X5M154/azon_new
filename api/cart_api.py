from config.hosts import PRODUCT_URL
from requester.custom_requester import CustomRequester


class CartAPI(CustomRequester):

    CART_ENDPOINT = "/api/v1/cart"

    def __init__(self, session, base_url=PRODUCT_URL):
        super().__init__(session, base_url=PRODUCT_URL)

    def get_cart(self, expected_status=200):
        return self.send_request(
            "GET", self.CART_ENDPOINT, expected_status=expected_status)

    def add_item(self, data, expected_status=201):
        return self.send_request(
            "POST",
            f"{self.CART_ENDPOINT}/items",
            json=data,
            expected_status=expected_status,
        )