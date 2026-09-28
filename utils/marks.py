import pytest
from config.credentials import ADMIN_INVITE, MANAGER_INVITE
from config.db import DB_PASSWORD


requires_admin = pytest.mark.skipif(
    not ADMIN_INVITE,
    reason="В .env нет админского кода, тест пропускаем"
)

requires_manager = pytest.mark.skipif(
    not MANAGER_INVITE,
    reason="В .env нет менеджерского кода, тест пропускаем"
)

requires_db = pytest.mark.skipif(
    not DB_PASSWORD,
    reason="в .env нет DB_PASSWORD - тесты с базой пропускаем",
)