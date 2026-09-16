from config.hosts import PRODUCT_URL
from requester.custom_requester import CustomRequester


class ProductsAPI(CustomRequester):
    """Клиент Product API: каталог товаров."""

    PRODUCTS_ENDPOINT = "/api/v1/products"

    def __init__(self, session):
        super().__init__(session, base_url=PRODUCT_URL)

    def get_products(self, params=None, expected_status=200):
        return self.send_request(
            "GET", self.PRODUCTS_ENDPOINT, params=params, expected_status=expected_status
        )

    def get_product(self, product_id, expected_status=200):
        return self.send_request(
            "GET", f"{self.PRODUCTS_ENDPOINT}/{product_id}", expected_status=expected_status
        )

    def create_product(self, product_data, expected_status=201):
        return self.send_request(
            "POST", self.PRODUCTS_ENDPOINT, json=product_data, expected_status=expected_status
        )

    def update_product(self, product_id, update_data, expected_status=200):
        return self.send_request(
            "PATCH", f"{self.PRODUCTS_ENDPOINT}/{product_id}", json=update_data, expected_status=expected_status
        )

    def update_price(self, product_id, price, expected_status=200):
        return self.send_request(
            "PATCH", f"{self.PRODUCTS_ENDPOINT}/{product_id}/price", json=price, expected_status=expected_status
        )

    def delete_product(self, product_id, expected_status=204):
        return self.send_request(
            "DELETE", f"{self.PRODUCTS_ENDPOINT}/{product_id}", expected_status=expected_status
        )

