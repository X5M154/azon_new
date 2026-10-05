import uuid
from unittest.mock import MagicMock
from config.hosts import PRODUCT_URL, MOCK_URL
from api.reviews_api import ReviewsAPI
import pytest
import requests
import json

from data.reviews import ReviewData
from mocks.stubs import JSON_HEADERS, error_body
from models.reviews import ReviewsPage

pytestmark = [pytest.mark.mock, pytest.mark.reviews]

REVIEW_ID = "123dfg"
PRODUCT_ID = "11111111-1111-1111-1111-111111111111"
REVIEWS_PATH = f"/api/v1/products/{PRODUCT_ID}/reviews"

def reviews_page_stub(items):
    return {
        "request": {"method": "GET", "urlPath": REVIEWS_PATH},
        "response": {
            "status": 200,
            "headers": JSON_HEADERS,
            "jsonBody": {"items": items, "total": len(items), "page": 1, "size": 20, "pages": 1},
        },
    }

def review_body(rating=5, **overrides):
    body = {
        "id": "11111111-1111-1111-1111-111111111111",
        "product_id": "11111111-2111-1111-1111-111111111111",
        "user_id": "11111111-3111-1111-1111-111111111111",
        "user_name": "Oleg Olegovich",
        "rating": rating,
        "text": "text",
        "is_seed": False,
        "created_at": "2026-08-06T12:00:00Z",
        "updated_at": "2026-08-06T12:00:00Z",
    }
    return {**body, **overrides}

def reviews_server_error():
    return {
        "request": {"method": "GET", "urlPath": REVIEWS_PATH},
        "response": {
            "status": 500,
            "headers": JSON_HEADERS,
            "jsonBody": error_body("INTERNAL_ERROR", "Internal server error"),
        },
    }

@pytest.fixture
def mock_reviews_api(wiremock):
    session = requests.Session()
    yield ReviewsAPI(session, base_url=MOCK_URL)
    session.close()

def test_delete_review_without_network():

    response = MagicMock()
    response.status_code = 204
    response.text = ""
    response.elapsed.total_seconds.return_value = 0.01
    response.request.method = "DELETE"
    response.request.url = f"{PRODUCT_URL}/api/v1/reviews/{REVIEW_ID}"
    response.request.body = None

    session = MagicMock()
    session.request.return_value = response
    session.headers = {}

    ReviewsAPI(session).delete_review(REVIEW_ID)

    session.request.assert_called_once_with(
        "DELETE", f"{PRODUCT_URL}/api/v1/reviews/{REVIEW_ID}", timeout=10
    )

def test_reviews_page_turns_into_model(wiremock, mock_reviews_api):
    wiremock.add_stub(
        reviews_page_stub([review_body(5), review_body(rating=2, id=str(uuid.uuid4()))])
    )

    response = mock_reviews_api.get_reviews(PRODUCT_ID)

    page = ReviewsPage.model_validate(response.json())
    assert page.total == 2
    assert [review.rating for review in page.items] == [5, 2]

@pytest.mark.negative
def test_broken_service_fails_readably(wiremock, mock_reviews_api):
    wiremock.add_stub(reviews_server_error())

    with pytest.raises(AssertionError) as error:
        mock_reviews_api.get_reviews(PRODUCT_ID)

    assert "ожидали статус 200, получили 500" in str(error.value)
    assert "INTERNAL_ERROR" in str(error.value)


def test_update_sends_only_filled_fields(wiremock):
    wiremock.add_stub(
        {
            "request": {"method": "PATCH", "urlPathPattern": "/api/v1/reviews/.+"},
            "response": {"status": 200, "headers": JSON_HEADERS, "jsonBody": review_body()},
        }
    )
    review_id = uuid.uuid4()
    update = ReviewData.update_review_data()

    with requests.Session() as session:
        ReviewsAPI(session, base_url=MOCK_URL).update_review(review_id, update)

    sent = wiremock.find_requests({"method": "PATCH", "urlPath": f"/api/v1/reviews/{review_id}"})[0]
    assert json.loads(sent["body"]) == {"text": update.text}