import uuid
from decimal import Decimal
from data.products import ProductData
import pytest

class TestProducts:

    def test_get_products_returns_paginated_catalog(self, api_manager):
        response = api_manager.products_api.get_products()

        data = response.json()
        assert data["total"] > 0
        assert len(data["items"]) <= data["size"]

    def test_products_price_filter(self, api_manager):
        response = api_manager.products_api.get_products(
            params={"price_min": 5000, "size": 100}
        )

        products = response.json()["items"]
        assert products
        for product in products:
            assert Decimal(product["price"]) >= 5000

    def test_get_product_by_id(self, api_manager):
        products = api_manager.products_api.get_products().json()["items"]
        product_id = products[0]["id"]

        response = api_manager.products_api.get_product(product_id)
        assert response.json()["id"] == product_id

    def test_get_product_invalid_id(self, api_manager):
        response = api_manager.products_api.get_product(uuid.uuid4(), expected_status=404)
        assert response.json()["error"]["code"] == "PRODUCT_NOT_FOUND"

    def test_create_product(self, api_manager, authenticated_admin, category_id):
        product_data = ProductData.creation_product_data(category_id)
        response = api_manager.products_api.create_product(product_data)
        product = response.json()

        assert product["name"] == product_data["name"]
        assert product["sku"] == product_data["sku"]
        assert product["description"] == product_data["description"]
        assert product["price"] == product_data["price"]
        assert product["stock"] == product_data["stock"]
        assert product["category_id"] == product_data["category_id"]

    def test_create_product_by_user(self, api_manager, authenticated_user, category_id):
        product_data = ProductData.creation_product_data(category_id)
        response = api_manager.products_api.create_product(product_data, expected_status=403)

        assert response.json()["error"]["code"] == "FORBIDDEN"


    def test_create_product_without_token(self, api_manager, category_id):
        product_data = ProductData.creation_product_data(category_id)
        response = api_manager.products_api.create_product(product_data, expected_status=401)

        assert response.json()["error"]["code"] == "TOKEN_MISSING"

    def test_update_product(self, api_manager, created_product):
        product_id = created_product["id"]
        new_data = ProductData.update_product_data()

        response = api_manager.products_api.update_product(product_id, new_data)
        assert response.json()["name"] == new_data["name"]
        assert response.json()["description"] == new_data["description"]
        assert response.json()["stock"] == new_data["stock"]

    def test_update_product_price(self, api_manager, created_product):
        product_id = created_product["id"]
        new_price = ProductData.update_product_price()

        response = api_manager.products_api.update_price(product_id, new_price)
        assert response.json()["price"] == new_price["price"]

    def test_update_product_price_by_manager(self, manager_manager, created_product):
        product_id = created_product["id"]
        new_price = ProductData.update_product_price()

        response = manager_manager.products_api.update_price(product_id, new_price, expected_status=403)
        assert response.json()["error"]["code"] == "FORBIDDEN"

    def test_delete_product(self, api_manager, created_product):
        product_id = created_product["id"]

        api_manager.products_api.delete_product(product_id)

    def test_delete_seed(self, api_manager, authenticated_admin):
        products = api_manager.products_api.get_products().json()["items"]
        seed = [product for product in products if product["is_seed"] is True]

        product_id = seed[0]["id"]

        response = api_manager.products_api.delete_product(product_id, expected_status=403)
        assert response.json()["error"]["code"] == "SEED_PROTECTED"

    def test_product_search(self, api_manager, created_product):
        product = created_product["name"]

        response = api_manager.products_api.get_products(
            params={"search": product}
        )

        result = response.json()["items"]
        assert len(result) == 1

        result = result[0]
        assert product == result["name"]

    @pytest.mark.skip(reason="AZON-101: экспорт каталога в CSV ещё не реализован")
    def test_export_catalog_to_csv():
        assert False



