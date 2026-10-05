import json

import pytest
import requests

from api.auth_api import AuthAPI
from api.user_api import UserAPI
from config.hosts import MOCK_URL
from data.users import UserData
from mocks.stubs import JSON_HEADERS, LOGIN_ENDPOINT, ME_ENDPOINT, AuthStubs, user_body

pytestmark = [pytest.mark.mock, pytest.mark.auth]

TOKEN = "mock-access-token"


def patch_me_ok():
    """PATCH профиля отдаём только с нашим токеном - как и GET."""
    return {
        "request": {
            "method": "PATCH",
            "urlPath": ME_ENDPOINT,
            "headers": {"Authorization": {"equalTo": f"Bearer {TOKEN}"}},
        },
        "response": {"status": 200, "headers": JSON_HEADERS, "jsonBody": user_body()},
    }


def test_token_travels_with_every_request(wiremock, mock_apis):
    auth_api, user_api = mock_apis
    wiremock.add_stub(AuthStubs.login_ok(TOKEN))
    wiremock.add_stub(AuthStubs.me_requires_bearer(TOKEN))
    wiremock.add_stub(patch_me_ok())

    auth_api.authenticate(("mock@example.com", "SuperSecret123"))
    user_api.get_user_info()
    user_api.update_user_info(UserData.update_profile_data())

    with_token = {
        "urlPath": ME_ENDPOINT,
        "headers": {"Authorization": {"equalTo": f"Bearer {TOKEN}"}},
    }
    assert wiremock.count_requests(with_token) == 2


def test_password_goes_only_into_the_body(wiremock, mock_apis):
    auth_api, _ = mock_apis
    wiremock.add_stub(AuthStubs.login_ok(TOKEN))

    auth_api.authenticate(("mock@example.com", "SuperSecret123"))

    sent = wiremock.find_requests({"method": "POST", "urlPath": LOGIN_ENDPOINT})[0]
    assert sent["url"] == LOGIN_ENDPOINT, "пароль уехал бы в query - и осел в логах прокси"
    assert "SuperSecret123" not in json.dumps(sent["headers"], ensure_ascii=False)
    assert json.loads(sent["body"])["password"] == "SuperSecret123"