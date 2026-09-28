import pytest

from utils.marks import requires_db

pytestmark = [pytest.mark.db, pytest.mark.auth, requires_db]


class TestUsersInDB:

    def test_registered_user_is_saved_in_db(self, registered_user, db):
        row = db.auth.get_user_by_email(registered_user.registration.email)

        assert row is not None, "API вернул 201, но строки в azon_auth.users нет"
        assert row["id"] == registered_user.profile.id
        assert row["full_name"] == registered_user.registration.full_name
        assert row["role"] == "USER"
        assert row["is_active"] is True
        assert row["is_seed"] is False

    def test_password_is_stored_as_hash(self, registered_user, db):
        row = db.auth.get_user_by_email(registered_user.registration.email)

        assert row["password_hash"] != registered_user.registration.password
        assert row["password_hash"].startswith("$2b$"), "пароль должен лежать bcrypt-хешем"

    def test_email_column_is_case_insensitive(self, registered_user, db):
        row = db.auth.get_user_by_email(registered_user.registration.email.upper())

        assert row is not None, "email в базе должен искаться без учёта регистра"

    def test_logout_revokes_refresh_tokens(self, api_manager, authenticated_user, db):
        user_id = authenticated_user.profile.id
        tokens = db.auth.get_refresh_tokens(user_id)
        assert tokens, "после входа у пользователя есть refresh-токен"
        assert all(token["revoked_at"] is None for token in tokens)

        api_manager.auth_api.logout()

        tokens_after = db.auth.get_refresh_tokens(user_id)
        assert all(token["revoked_at"] is not None for token in tokens_after)