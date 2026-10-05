from data.products import ProductData
import pytest

from utils.marks import requires_db, requires_admin

pytestmark = [pytest.mark.db, requires_db, requires_admin]

def test_cart_item_keeps_price_at_add(
    api_manager, admin_manager, authenticated_user, created_product, db):

    api_manager.cart_api.add_item(ProductData.cart_item_data(created_product.id, quantity=2))
    new_price = ProductData.price_data(current_price=created_product.price)

    admin_manager.products_api.update_price(created_product.id, new_price)

    items = db.product.get_cart_items(authenticated_user.profile.id)
    assert len(items) == 1
    assert items[0]["quantity"] == 2
    assert items[0]["price_at_add"] == created_product.price, "в корзине - цена на момент добавления"

    cart = api_manager.cart_api.get_cart().json()
    assert cart["items"][0]["current_price"] == str(new_price.price)
    assert cart["items"][0]["price_changed"] is True