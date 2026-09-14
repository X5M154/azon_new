from config.credentials import MANAGER_INVITE, ADMIN_INVITE
from data.users import UserData

class TestAuth:

    def test_register_and_login(self, api_manager):
        user_data = UserData.registration_data()

        register_response = api_manager.auth_api.register_user(user_data)
        assert register_response.json()["role"] == "USER"

        api_manager.auth_api.authenticate((user_data["email"], user_data["password"]))

        me_response = api_manager.user_api.get_user_info()
        assert me_response.json()["email"] == user_data["email"]

    def test_register_with_exciting_email(self, api_manager, registered_user):
        user_data = UserData.registration_data()
        user_data["email"] = registered_user["email"]

        response = api_manager.auth_api.register_user(user_data, expected_status=409)
        assert response.json()["error"]["code"] == "EMAIL_EXISTS"

    def test_register_with_exciting_email_manager(self, api_manager, registered_manager):
        user_data = UserData.registration_data(invite_code=ADMIN_INVITE)
        user_data["email"] = registered_manager["email"]

        response = api_manager.auth_api.register_user(user_data, expected_status=409)
        assert response.json()["error"]["code"] == "EMAIL_EXISTS"

    def test_login_with_wrong_password(self, api_manager, registered_user):
        credentials = UserData.login_data(registered_user)
        credentials["password"] = "wr0ng_PASSword"

        response = api_manager.auth_api.login_user(credentials, expected_status=401)
        assert response.json()["error"]["code"] == "INVALID_CREDENTIALS"

    def test_login_with_wrong_password_manager(self, api_manager, registered_manager):
        credentials = UserData.login_data(registered_manager)
        credentials["password"] = "Wrong_p@ssword_MANAGer"

        response = api_manager.auth_api.login_user(credentials, expected_status=401)
        assert response.json()["error"]["code"] == "INVALID_CREDENTIALS"

    def test_login_with_wrong_password_admin(self, api_manager, registered_admin):
        credentials = UserData.login_data(registered_admin)
        credentials["password"] = "Admin_Password_ISWRONG"

        response = api_manager.auth_api.login_user(credentials, expected_status=401)
        assert response.json()["error"]["code"] == "INVALID_CREDENTIALS"

    def test_register_with_wrong_invite(self, api_manager):
        user_data = UserData.registration_data(invite_code="HUM_TA")

        response = api_manager.auth_api.register_user(user_data, expected_status=403)
        assert response.json()["error"]["code"] == "INVALID_INVITE_CODE"







