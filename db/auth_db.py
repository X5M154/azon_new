from db.db_client import DBClient


class AuthDB(DBClient):
    """База azon_auth: пользователи и refresh-токены."""

    def get_user_by_email(self, email):
        return self.fetch_one("SELECT * FROM users WHERE email = %s", (email,))

    def get_user(self, user_id):
        return self.fetch_one("SELECT * FROM users WHERE id = %s", (user_id,))

    def count_users_by_role(self, role):
        row = self.fetch_one("SELECT count(*) AS total FROM users WHERE role = %s", (role,))
        return row["total"]

    def get_refresh_tokens(self, user_id):
        return self.fetch_all(
            "SELECT * FROM refresh_tokens WHERE user_id = %s ORDER BY created_at",
            (user_id,),
        )