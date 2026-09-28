import pytest
from pydantic import ValidationError

from data.reviews import ReviewData
from models.reviews import ReviewsPage, StrictReviewResponse
from utils.marks import requires_admin

pytestmark = [pytest.mark.reviews, pytest.mark.contract, requires_admin]


def test_created_review_matches_contract(api_manager, authenticated_user, created_product):
    review_request = ReviewData.creation_review_data()

    response = api_manager.reviews_api.create_review(created_product.id, review_request)

    review = StrictReviewResponse.model_validate(response.json())
    assert review.user_name == authenticated_user.registration.email


def test_reviews_page_matches_contract(api_manager, created_product, created_review):
    response = api_manager.reviews_api.get_reviews(created_product.id)

    page = ReviewsPage.model_validate(response.json())
    assert page.total == 1
    assert page.items[0].id == created_review.id


def test_model_notices_missing_rating(created_review):
    broken = created_review.model_dump(mode="json")
    del broken["rating"]

    with pytest.raises(ValidationError, match="rating"):
        StrictReviewResponse.model_validate(broken)