import pytest
from models.products import ProductPage

pytestmark = pytest.mark.products

@pytest.mark.xfail(
        strict=True, reason="AZON-142: фильтр in_stock=false не отбирает товары без остатка"
    )
def test_filter_out_of_stock(self, api_manager):
    response = api_manager.products_api.get_products(params={"in_stock": False, "size": 100})

    items = ProductPage.model_validate(response.json()).items
    assert all(product.stock == 0 for product in items)