import pytest

from data.orders import OrderData
from data.products import ProductData
from models.orders import PaymentResponse, OrderResponse
from utils.marks import requires_db, requires_admin

pytestmark = [pytest.mark.db, pytest.mark.payment, requires_db, requires_admin]


class TestOrdersInDB:

    def test_order_and_items_are_saved_in_db(self, created_order, created_product, db):
        order = db.payment.get_order(created_order.id)

        assert order is not None, "заказ оформлен, но строки в azon_payment.orders нет"
        assert order["status"] == "AWAITING_PAYMENT"
        assert order["total_amount"] == created_product.price

        items = db.payment.get_order_items(order["id"])
        assert len(items) == 1
        assert items[0]["product_id"] == created_product.id
        assert items[0]["quantity"] == 1
        assert items[0]["subtotal"] == created_product.price

    def test_order_item_keeps_price_snapshot(
        self, admin_manager, created_order, created_product, db):
        new_price = ProductData.price_data()

        admin_manager.products_api.update_price(created_product.id, new_price)

        product_row = db.product.get_product(created_product.id)
        item = db.payment.get_order_items(created_order.id)[0]

        assert product_row["price"] == new_price.price, "в каталоге цена новая"
        assert item["unit_price"] == created_product.price, "в заказе цена осталась прежней"

    def test_checkout_reserves_stock(self, created_order, created_product, db):
        row = db.product.get_product(created_product.id)

        assert row["stock"] == created_product.stock - 1, "оформление заказа списывает сток"