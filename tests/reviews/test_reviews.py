import pytest

from models.reviews import ReviewResponse
from utils.marks import requires_admin
from data.reviews import ReviewData

pytestmark = [pytest.mark.reviews, pytest.mark.regression, requires_admin]


class TestReviews:

    @pytest.mark.smoke
    def test_user_can_leave_review(self, api_manager, authenticated_user, created_product):
        review_data = ReviewData.creation_review_data()
        response = api_manager.reviews_api.create_review(created_product.id, review_data)

        review = ReviewResponse.model_validate(response.json())

        assert review.product_id == created_product.id
        assert review.rating == review_data.rating
        assert review.text == review_data.text

    @pytest.mark.negative
    def test_second_review_from_same_user_is_rejected(
        self, api_manager, created_product, created_review
    ):
        review_data = ReviewData.creation_review_data()

        response = api_manager.reviews_api.create_review(created_product.id, review_data, expected_status=409)

        assert response.json()["error"]["code"] == "REVIEW_EXISTS"

    @pytest.mark.negative
    @pytest.mark.roles
    def test_foreign_review_cannot_be_edited(self, second_user, created_review):
        review_data = ReviewData.creation_review_data()

        response = second_user.reviews_api.update_review(created_review.id, review_data, expected_status=403)

        assert response.json()["error"]["code"] == "NOT_REVIEW_OWNER"

    @pytest.mark.negative
    def test_extra_field_is_rejected(self, api_manager, authenticated_user, created_product):
        response = api_manager.reviews_api.create_review(
            created_product.id, ReviewData.review_with_extra_field(), expected_status=422
        )

        assert response.json()["detail"][0]["type"] == "extra_forbidden"