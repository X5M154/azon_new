"""Моки внутри процесса: unittest.mock и monkeypatch, сети нет вообще."""

from unittest.mock import MagicMock

import pytest

from api.auth_api import AuthAPI
from config.hosts import AUTH_URL
from data.users import UserData
from utils.data_generator import DataGenerator

pytestmark = [pytest.mark.mock, pytest.mark.auth]


def fake_login_response():
    """Заглушка ответа requests: заполняем только то, что реально трогает код."""
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {
        "access_token": "test-token",
        "refresh_token": "test-refresh",
        "token_type": "bearer",
        "expires_in": 43200,
    }
    # это нужно только логгеру из CustomRequester
    response.text = '{"access_token": "test-token"}'
    response.elapsed.total_seconds.return_value = 0.01
    response.request.method = "POST"
    response.request.url = f"{AUTH_URL}/api/v1/auth/login"
    response.request.body = None
    return response


def test_authenticate_saves_token_in_session_headers():
    """Stub-режим: подсунули готовый ответ и проверили результат."""
    session = MagicMock()
    session.request.return_value = fake_login_response()
    session.headers = {}

    AuthAPI(session).authenticate(("user@example.com", "SuperSecret123"))

    assert session.headers["Authorization"] == "Bearer test-token"


def test_authenticate_sends_exactly_one_login_request():
    """Mock-режим: проверяем не результат, а сами вызовы зависимости."""
    session = MagicMock()
    session.request.return_value = fake_login_response()
    session.headers = {}

    AuthAPI(session).authenticate(("user@example.com", "SuperSecret123"))

    session.request.assert_called_once_with(
        "POST",
        f"{AUTH_URL}/api/v1/auth/login",
        json={"email": "user@example.com", "password": "SuperSecret123"},
        timeout=10,
    )

def test_registration_data_uses_generated_email(monkeypatch):
    """monkeypatch подменяет генератор на время теста и сам всё возвращает назад."""
    monkeypatch.setattr(DataGenerator, "generate_email", lambda: "fixed@example.com")

    registration = UserData.registration_data()

    assert registration.email == "fixed@example.com"