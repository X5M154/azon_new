from data.users import UserData
import pytest
from models.users import UserResponse
from utils.data_generator import DataGenerator

pytestmark = pytest.mark.users

class TestUsers:

    @pytest.mark.negative
    def test_get_user_info_without_token(self, api_manager):

        response = api_manager.user_api.get_user_info(expected_status=401)

        assert response.json()["error"]["code"] == "TOKEN_MISSING"

    def test_get_user_info(self, api_manager, authenticated_user):
        response = api_manager.user_api.get_user_info()
        user = UserResponse.model_validate(response.json())

        assert user.email == authenticated_user.profile.email
        assert user.id == authenticated_user.profile.id

    def test_update_fullname(self, api_manager, authenticated_user):
        new_profile = UserData.update_profile_data()

        response = api_manager.user_api.update_user_info(new_profile)
        assert response.json()["full_name"] == new_profile["full_name"]
        assert api_manager.user_api.get_user_info().json()["full_name"] == new_profile["full_name"]

    def test_change_password(self, api_manager, authenticated_user):
        new_password = DataGenerator.generate_password()

        api_manager.user_api.change_password(
            UserData.change_password_data(authenticated_user.registration, new_password)
        )

        old_credentials = UserData.login_data(authenticated_user.registration)
        response = api_manager.auth_api.login_user(old_credentials, expected_status=401)
        assert response.json()["error"]["code"] == "INVALID_CREDENTIALS"

        api_manager.auth_api.authenticate((authenticated_user.registration.email, new_password))