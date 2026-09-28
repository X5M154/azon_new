from config.hosts import AUTH_URL
from requester.custom_requester import CustomRequester


class UserAPI(CustomRequester):
    """Клиент User API: профиль и данные пользователей."""

    ME_ENDPOINT = "/api/v1/users/me"
    CHANGE_PASSWORD_ENDPOINT = "/api/v1/users/me/password"

    def __init__(self, session, base_url=AUTH_URL):
        super().__init__(session, base_url)

    def get_user_info(self, expected_status=200):
        return self.send_request(
            "GET", self.ME_ENDPOINT, expected_status=expected_status
        )

    def update_user_info(self, user_data, expected_status=200):
        return self.send_request(
            "PATCH", self.ME_ENDPOINT, json=user_data, expected_status=expected_status
        )

    def change_password(self, passwords_data, expected_status=204):
        return self.send_request(
            "POST", self.CHANGE_PASSWORD_ENDPOINT, json=passwords_data, expected_status=expected_status
        )