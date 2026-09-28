from db.db_client import DBClient


class ProductDB(DBClient):
    """База azon_product: каталог, корзины, отзывы."""

    def get_product(self, product_id):
        return self.fetch_one("SELECT * FROM products WHERE id = %s", (product_id,))

    def get_product_by_sku(self, sku):
        return self.fetch_one("SELECT * FROM products WHERE sku = %s", (sku,))

    def get_cart_items(self, user_id):
        # корзина и позиции лежат в разных таблицах - собираем их JOIN'ом
        return self.fetch_all(
            """
            SELECT ci.product_id, ci.quantity, ci.price_at_add, p.name
            FROM cart_items ci
            JOIN carts c ON c.id = ci.cart_id
            JOIN products p ON p.id = ci.product_id
            WHERE c.user_id = %s
            ORDER BY ci.added_at
            """,
            (user_id,),
        )

    def get_moderation_record(self, review_id):
        """Запись журнала о модерации: сервис пишет её при удалении чужого отзыва."""
        return self.fetch_one(
            """
            SELECT action, actor_user_id, payload
            FROM audit_log
            WHERE action = 'REVIEW_MODERATE_DELETE' AND entity_id = %s
            """,
            (str(review_id),),
        )

    def count_active_products(self, category_id):
        row = self.fetch_one(
            """
            SELECT count(*) AS total FROM products
            WHERE category_id = %s AND deleted_at IS NULL
            """,
            (category_id,),
        )
        return row["total"]

    def get_review(self, review_id):
        return self.fetch_one("SELECT * FROM reviews WHERE id = %s", (review_id,))

    def count_reviews(self, product_id):
        row = self.fetch_one(
            "SELECT count(*) AS total FROM reviews WHERE product_id = %s", (product_id,)
        )
        return row["total"]

    def avg_rating(self, product_id):
        row = self.fetch_one(
            "SELECT round(avg(rating), 2) AS avg_rating FROM reviews WHERE product_id = %s",
            (product_id,),
        )
        return row["avg_rating"]