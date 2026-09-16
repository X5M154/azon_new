from utils.data_generator import DataGenerator


class UserData:
    """Object Mother для тел запросов Auth API."""

    @staticmethod
    def registration_data(invite_code=None) -> dict:
        data = {
            "email": DataGenerator.generate_email(),
            "password": DataGenerator.generate_password(),
            "full_name": DataGenerator.generate_fullname(),
        }
        if invite_code:
            data["invite_code"] = invite_code
        return data

    @staticmethod
    def login_data(user_data) -> dict:
        return {
            "email": user_data["email"],
            "password": user_data["password"]
        }

    @staticmethod
    def update_profile_data():
        return {"full_name": DataGenerator.generate_fullname()}