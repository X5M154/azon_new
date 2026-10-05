from utils.data_generator import DataGenerator
from models.users import RegisterRequest, LoginRequest

class UserData:
    """Object Mother для тел запросов Auth API."""

    @staticmethod
    def registration_data(invite_code=None) -> RegisterRequest:
        return RegisterRequest(
            email=DataGenerator.generate_email(),
            password=DataGenerator.generate_password(),
            full_name=DataGenerator.generate_fullname(),
            invite_code=invite_code,
        )

    @staticmethod
    def login_data(registration: RegisterRequest) -> LoginRequest:
        return LoginRequest(email=registration.email, password=registration.password)

    @staticmethod
    def update_profile_data():
        return {"full_name": DataGenerator.generate_fullname()}

    @staticmethod
    def change_password_data(user_data, new_password) -> dict:
        return {"old_password": user_data.password, "new_password": new_password}