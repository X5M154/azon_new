import pytest

from data.reviews import ReviewData
from utils.marks import requires_admin, requires_db, requires_manager

pytestmark = [pytest.mark.reviews, pytest.mark.db, requires_db, requires_admin]


def test_review_is_saved_in_db(created_review, db):
    row = db.product.get_review(created_review.id)

    assert row is not None, "отзыв создан через API, но строки в базе нет"
    assert row["rating"] == created_review.rating
    assert row["text"] == created_review.text
    assert row["is_seed"] is False

@pytest.mark.negative
def test_duplicate_review_does_not_create_second_row(
    api_manager, created_product, created_review, db
):
    api_manager.reviews_api.create_review(
        created_product.id, ReviewData.creation_review_data(), expected_status=409
    )

    assert db.product.count_reviews(created_product.id) == 1


@requires_manager
def test_moderation_deletes_row_and_leaves_a_trace(store_manager, created_review, db):

    store_manager.reviews_api.delete_review(created_review.id)

    assert db.product.get_review(created_review.id) is None, "строка отзыва должна исчезнуть"

    record = db.product.get_moderation_record(created_review.id)
    assert record is not None, "модерация чужого отзыва обязана попасть в audit_log"
    assert record["payload"]["author"] == str(created_review.user_id)