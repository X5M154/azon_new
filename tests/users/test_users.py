from data.users import UserData


class TestUsers:

    def test_get_user_info_without_token(self, api_manager):

        response = api_manager.user_api.get_user_info(expected_status=401)

        assert response.json()["error"]["code"] == "TOKEN_MISSING"

    def test_get_user_info(self, api_manager, authenticated_user):
        response = api_manager.user_api.get_user_info()

        assert response.json()["email"] == authenticated_user["email"]
        assert response.json()["id"] == authenticated_user["id"]

    def test_update_fullname(self, api_manager, authenticated_user):
        new_profile = UserData.update_profile_data()

        response = api_manager.user_api.update_user_info(new_profile)
        assert response.json()["full_name"] == new_profile["full_name"]
        assert api_manager.user_api.get_user_info().json()["full_name"] == new_profile["full_name"]


