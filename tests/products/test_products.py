import uuid
import pytest
from decimal import Decimal
from data.products import ProductData
from models.categories import CategoryResponse
from models.products import ProductRequest, ProductResponse
from utils.marks import requires_admin, requires_manager
from pydantic import ValidationError

pytestmark = [pytest.mark.products, requires_admin]

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

    @pytest.mark.xfail(reason="AZON-142: фильтр in_stock=false не отбирает товары без остатка")
    def test_filter_out_of_stock(self, api_manager):
        response = api_manager.products_api.get_products(
            params={"in_stock": False, "size": 100}
        )

        items = response.json()["items"]
        assert all(item["stock"] == 0 for item in items)

    def test_get_product_by_id(self, api_manager):
        products = api_manager.products_api.get_products().json()["items"]
        product_id = products[0]["id"]

        response = api_manager.products_api.get_product(product_id)
        assert response.json()["id"] == product_id

    @pytest.mark.negative
    def test_get_product_invalid_id(self, api_manager):
        response = api_manager.products_api.get_product(uuid.uuid4(), expected_status=404)
        assert response.json()["error"]["code"] == "PRODUCT_NOT_FOUND"

    def test_create_product(self, admin_manager, category_id):
        product_data = ProductData.creation_product_data(category_id)
        response = admin_manager.products_api.create_product(product_data)
        product = ProductResponse.model_validate(response.json())

        try:
            assert product.name == product_data.name
            assert product.sku == product_data.sku
            assert product.price == product_data.price
            assert product.stock == product_data.stock
        finally:
            admin_manager.products_api.delete_product(product.id)

    @pytest.mark.roles
    @pytest.mark.negative
    def test_create_product_by_user(self, api_manager, authenticated_user, category_id):
        product_data = ProductData.creation_product_data(category_id)
        response = api_manager.products_api.create_product(product_data, expected_status=403)

        assert response.json()["error"]["code"] == "FORBIDDEN"

    @pytest.mark.negative
    def test_create_product_without_token(self, api_manager, category_id):
        product_data = ProductData.creation_product_data(category_id)
        response = api_manager.products_api.create_product(product_data, expected_status=401)

        assert response.json()["error"]["code"] == "TOKEN_MISSING"

    def test_update_product(self, admin_manager, created_product):
        product_id = created_product.id
        new_data = ProductData.update_product_data()

        response = admin_manager.products_api.update_product(product_id, new_data)
        updated_product = ProductResponse.model_validate(response.json())

        assert updated_product.name == new_data.name
        assert updated_product.description == new_data.description
        assert updated_product.stock == new_data.stock

    def test_update_product_price(self, admin_manager, created_product):
        product_id = created_product.id
        new_price = ProductData.update_product_price()

        response = admin_manager.products_api.update_price(product_id, new_price)
        updated_product = ProductResponse.model_validate(response.json())
        assert updated_product.price == new_price.price

    @requires_manager
    @pytest.mark.roles
    @pytest.mark.slow
    def test_update_product_price_by_manager(self, managers_api, created_product):
        product_id = created_product.id
        new_price = ProductData.update_product_price()

        response = managers_api.products_api.update_price(product_id, new_price, expected_status=403)
        assert response.json()["error"]["code"] == "FORBIDDEN"

    def test_delete_product(self, admin_manager, created_product):
        product_id = created_product.id

        admin_manager.products_api.delete_product(product_id)

        response = admin_manager.products_api.get_product(product_id)
        assert response.json()["is_available"] is False

    @pytest.mark.negative
    def test_delete_seed(self, admin_manager, authenticated_admin):
        products = admin_manager.products_api.get_products(params={"size": 100}).json()["items"]
        seed = [product for product in products if product["is_seed"] is True]
        assert seed
        product_id = seed[0]["id"]

        response = admin_manager.products_api.delete_product(product_id, expected_status=403)
        assert response.json()["error"]["code"] == "SEED_PROTECTED"

    def test_product_search(self, api_manager, created_product):
        product_name = created_product.name

        response = api_manager.products_api.get_products(
            params={"search": product_name}
        )
        items = response.json()["items"]

        assert items
        for item in items:
            assert product_name in item["name"]

    @pytest.mark.negative
    def test_create_product_sku_exists(self, admin_manager, category_id, created_product):
        product_data = ProductData.creation_product_data(category_id)
        product_data.sku = created_product.sku
        response = admin_manager.products_api.create_product(product_data, expected_status=409)

        assert response.json()["error"]["code"] == "SKU_EXISTS"

    @pytest.mark.negative
    def test_create_product_with_wrong_data(self, admin_manager, authenticated_admin, category_id):
        product_data = ProductData.creation_product_data(category_id).model_dump(mode="json")
        product_data["name"] = 0

        response = admin_manager.products_api.create_product(product_data, expected_status=422)
        detail = response.json()['detail']
        assert any(error['loc'] == ['body', 'name'] for error in detail)

    @pytest.mark.slow
    def test_catalog_keeps_all_created_products(self, admin_manager, category_id):
        created = []
        for _ in range(10):
            product_data = ProductData.creation_product_data(category_id)
            created.append(admin_manager.products_api.create_product(product_data).json())

        response = admin_manager.products_api.get_products(
            params={"category_id": category_id, "size": 100, "sort_by": "created_at"}
        )
        catalog_ids = {item["id"] for item in response.json()["items"]}

        try:
            assert {product["id"] for product in created} <= catalog_ids
        finally:
            for product in created:
                admin_manager.products_api.delete_product(product["id"])

    @pytest.mark.negative
    def test_model_rejects_zero_price(self):
        product_request = ProductData.creation_product_data(uuid.uuid4())

        with pytest.raises(ValidationError) as error:
            ProductRequest.model_validate({**product_request.model_dump(), "price": 0})

        assert error.value.errors()[0]["type"] == "greater_than"

    def test_all_categories_match_contract(self, api_manager):
        response = api_manager.categories_api.get_categories()

        categories = [CategoryResponse.model_validate(item) for item in response.json()]

        assert categories, "На стенде нет ни одной категории"
        assert all(category.slug for category in categories)

    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "field, value, expected_type",
        [
            ("sku", "AZ 001 с пробелами", "string_pattern_mismatch"),
            ("name", "", "string_too_short"),
            ("stock", -1, "greater_than_equal"),
            ("price", "1000001", "less_than_equal"),
        ],
    )
    def test_model_rejects_bad_field(self, field, value, expected_type):
        good = ProductData.creation_product_data(uuid.uuid4()).model_dump()

        with pytest.raises(ValidationError) as error:
            ProductRequest.model_validate({**good, field: value})

        assert error.value.errors()[0]["type"] == expected_type
        assert error.value.errors()[0]["loc"] == (field,)