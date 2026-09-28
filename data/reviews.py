from models.reviews import ReviewCreateRequest, ReviewUpdateRequest
from utils.data_generator import DataGenerator


class ReviewData:
    """Object Mother для тел запросов домена отзывов."""

    @staticmethod
    def creation_review_data(rating=5) -> ReviewCreateRequest:
        return ReviewCreateRequest(rating=rating, text=DataGenerator.generate_review_text())

    @staticmethod
    def update_review_data(rating=None) -> ReviewUpdateRequest:
        # rating=None не уедет на сервер: за это отвечает exclude_none в send_request
        return ReviewUpdateRequest(rating=rating, text=DataGenerator.generate_review_text())

    @staticmethod
    def review_with_extra_field() -> dict:
        # намеренно словарь: модель с extra="forbid" такое просто не соберёт,
        # а проверить надо ответ сервиса
        return {"rating": 5, "text": "Пробуем лишнее поле", "user_id": "no-such-field"}