from config.credentials import MANAGER_INVITE, ADMIN_INVITE
from data.users import UserData
import pytest
from models.users import TokenPairResponse, UserResponse


pytestmark = pytest.mark.auth

class TestAuth:

    @pytest.mark.smoke
    def test_register_and_login(self, api_manager):
        user_data = UserData.registration_data()

        register_response = api_manager.auth_api.register_user(user_data)
        assert register_response.json()["role"] == "USER"

        api_manager.auth_api.authenticate((user_data.email, user_data.password))
        me_response = api_manager.user_api.get_user_info()

        user = UserResponse.model_validate(me_response.json())
        assert user.email == user_data.email

    def test_login_returns_token_pair(self, api_manager, registered_user):
        response = api_manager.auth_api.login_user(
            UserData.login_data(registered_user.registration)
        )

        tokens = TokenPairResponse.model_validate(response.json())
        assert tokens.token_type == "bearer"
        assert tokens.expires_in == 43200
        assert tokens.access_token.count(".") == 2

    @pytest.mark.negative
    def test_register_with_exciting_email(self, api_manager, registered_user):
        user_data = UserData.registration_data()
        user_data.email = registered_user.profile.email

        response = api_manager.auth_api.register_user(user_data, expected_status=409)
        assert response.json()["error"]["code"] == "EMAIL_EXISTS"

    @pytest.mark.roles
    @pytest.mark.negative
    def test_register_with_exciting_email_manager(self, api_manager, registered_manager):
        user_data = UserData.registration_data(invite_code=ADMIN_INVITE)
        user_data.email = registered_manager.profile.email

        response = api_manager.auth_api.register_user(user_data, expected_status=409)
        assert response.json()["error"]["code"] == "EMAIL_EXISTS"

    @pytest.mark.negative
    def test_login_with_wrong_password(self, api_manager, registered_user):
        credentials = UserData.login_data(registered_user.registration)
        credentials.password = "wr0ng_PASSword"

        response = api_manager.auth_api.login_user(credentials, expected_status=401)
        assert response.json()["error"]["code"] == "INVALID_CREDENTIALS"

    @pytest.mark.roles
    @pytest.mark.negative
    def test_login_with_wrong_password_manager(self, api_manager, registered_manager):
        credentials = UserData.login_data(registered_manager.registration)
        credentials.password = "Wrong_p@ssword_MANAGer"

        response = api_manager.auth_api.login_user(credentials, expected_status=401)
        assert response.json()["error"]["code"] == "INVALID_CREDENTIALS"

    @pytest.mark.roles
    @pytest.mark.negative
    def test_login_with_wrong_password_admin(self, api_manager, registered_admin):
        credentials = UserData.login_data(registered_admin.registration)
        credentials.password = "Admin_Password_ISWRONG"

        response = api_manager.auth_api.login_user(credentials, expected_status=401)
        assert response.json()["error"]["code"] == "INVALID_CREDENTIALS"

    @pytest.mark.negative
    def test_register_with_wrong_invite(self, api_manager):
        user_data = UserData.registration_data(invite_code="HUM_TA")

        response = api_manager.auth_api.register_user(user_data, expected_status=403)
        assert response.json()["error"]["code"] == "INVALID_INVITE_CODE"