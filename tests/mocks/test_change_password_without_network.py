from unittest.mock import MagicMock

import pytest

from api.user_api import UserAPI
from config.hosts import AUTH_URL
from data.users import UserData

pytestmark = [pytest.mark.mock, pytest.mark.users]

def fake_response(status_code, text=""):
    response = MagicMock()
    response.status_code = status_code
    response.text = text
    response.elapsed.total_seconds.return_value = 0.01
    response.request.method = "POST"
    response.request.url = f"{AUTH_URL}/api/v1/users/me/password"
    response.request.body = None
    return response


def passwords_data():
    return UserData.change_password_data(UserData.registration_data(), "NewSecret123")


def test_change_password_sends_one_post():
    session = MagicMock()
    session.request.return_value = fake_response(204)
    session.headers = {}
    passwords = passwords_data()

    UserAPI(session).change_password(passwords)

    session.request.assert_called_once_with(
        "POST",
        f"{AUTH_URL}/api/v1/users/me/password",
        json={
            "old_password": passwords["old_password"],
            "new_password": passwords["new_password"],
        },
        timeout=10,
    )

@pytest.mark.negative
def test_change_password_reports_unexpected_status():
    session = MagicMock()
    session.request.return_value = fake_response(400, '{"error": {"code": "WRONG_OLD_PASSWORD"}}')
    session.headers = {}

    with pytest.raises(AssertionError) as error:
        UserAPI(session).change_password(passwords_data())

    assert "ожидали статус 204, получили 400" in str(error.value)
    assert "WRONG_OLD_PASSWORD" in str(error.value)