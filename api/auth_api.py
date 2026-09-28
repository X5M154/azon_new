from config.hosts import AUTH_URL
from requester.custom_requester import CustomRequester


class AuthAPI(CustomRequester):
    """Клиент Auth API: регистрация, вход, профиль."""

    REGISTER_ENDPOINT = "/api/v1/auth/register"
    LOGIN_ENDPOINT = "/api/v1/auth/login"
    LOGOUT_ENDPOINT = "/api/v1/auth/logout"

    def __init__(self, session, base_url=AUTH_URL):
        super().__init__(session, base_url)

    def register_user(self, user_data, expected_status=201):
        return self.send_request(
            "POST", self.REGISTER_ENDPOINT, json=user_data, expected_status=expected_status
        )

    def login_user(self, credentials, expected_status=200):
        return self.send_request(
            "POST", self.LOGIN_ENDPOINT, json=credentials, expected_status=expected_status
        )

    def authenticate(self, user_creds):
        email, password = user_creds
        response = self.login_user({"email": email, "password": password})
        token = response.json()["access_token"]
        self._update_session_headers(Authorization=f"Bearer {token}")
        return response

    def logout(self, expected_status=204):
        return self.send_request("POST", self.LOGOUT_ENDPOINT, expected_status=expected_status)