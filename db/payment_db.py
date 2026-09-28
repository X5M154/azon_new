from db.db_client import DBClient


class PaymentDB(DBClient):
    """База azon_payment: заказы, позиции заказов, платежи."""

    def get_order(self, order_id):
        return self.fetch_one("SELECT * FROM orders WHERE id = %s", (order_id,))

    def get_order_items(self, order_id):
        return self.fetch_all(
            "SELECT * FROM order_items WHERE order_id = %s ORDER BY product_name",
            (order_id,),
        )

    def count_orders(self, user_id):
        row = self.fetch_one(
            "SELECT count(*) AS total FROM orders WHERE user_id = %s", (user_id,)
        )
        return row["total"]