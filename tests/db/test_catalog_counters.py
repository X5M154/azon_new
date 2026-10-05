import pytest

from data.products import ProductData
from utils.marks import requires_admin, requires_db

pytestmark = [pytest.mark.db, pytest.mark.products, requires_db, requires_admin]


def test_new_product_increases_category_counter(admin_manager, category_id, db):
    before = db.product.count_active_products(category_id)

    product = admin_manager.products_api.create_product(
        ProductData.creation_product_data(category_id)
    ).json()

    assert db.product.count_active_products(category_id) == before + 1

    admin_manager.products_api.delete_product(product["id"])
    assert db.product.count_active_products(category_id) == before