import pytest
from data.products import ProductData
from models.products import ProductPage
from utils.marks import requires_admin

pytestmark = [pytest.mark.products, requires_admin]

@pytest.fixture
def out_of_stock_product(admin_manager, category_id):
    """Товар с нулевым остатком: под него и написан фильтр in_stock."""
    product_request = ProductData.creation_product_data(category_id)
    product = admin_manager.products_api.create_product(product_request).json()
    admin_manager.products_api.update_product(product["id"], {"stock": 0})

    yield product

    admin_manager.products_api.delete_product(product["id"])


def test_in_stock_true_hides_empty_stock(api_manager, out_of_stock_product):
    response = api_manager.products_api.get_products(
        params={"search": out_of_stock_product["name"], "in_stock": "true"}
    )

    page = ProductPage.model_validate(response.json())
    assert page.total == 0, "товар с нулевым остатком не должен попадать в in_stock=true"