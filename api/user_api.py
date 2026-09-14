from config.hosts import AUTH_URL
from requester.custom_requester import CustomRequester

class UserAPI(CustomRequester):
    """Клиент User API: профиль и данные пользователей."""

    ME_ENDPOINT = "/api/v1/users/me"

    def __init__(self, session):
        super().__init__(session, base_url=AUTH_URL)

    def get_user_info(self, expected_status=200):
        return self.send_request(
            "GET", self.ME_ENDPOINT, expected_status=expected_status
        )

    def update_user_info(self, user_data, expected_status=200):
        return self.send_request(
            "PATCH", self.ME_ENDPOINT, json=user_data, expected_status=expected_status
        )