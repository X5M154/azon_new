from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ReviewCreateRequest(BaseModel):
    """Тело POST /api/v1/products/{product_id}/reviews - ограничения списаны со Swagger."""

    model_config = ConfigDict(extra="forbid")

    rating: int = Field(ge=1, le=5)
    text: str = Field(min_length=1, max_length=2000)


class ReviewUpdateRequest(BaseModel):
    """Тело PATCH /api/v1/reviews/{review_id}: оба поля необязательные."""

    model_config = ConfigDict(extra="forbid")

    rating: int | None = Field(None, ge=1, le=5)
    text: str | None = Field(None, min_length=1, max_length=2000)


class ReviewResponse(BaseModel):
    """Отзыв в ответе стенда."""

    id: UUID
    product_id: UUID
    user_id: UUID
    user_name: str
    rating: int
    text: str
    is_seed: bool
    created_at: datetime
    updated_at: datetime


class ReviewsPage(BaseModel):
    """Страница отзывов: GET /api/v1/products/{product_id}/reviews."""

    items: list[ReviewResponse]
    total: int
    page: int
    size: int
    pages: int

class StrictReviewResponse(ReviewResponse):
    """Для контрактного теста: про новое поле в ответе хотим узнать первыми."""

    model_config = ConfigDict(extra="forbid")