from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import datetime


class OrderItemResponse(BaseModel):
    product_id: UUID
    product_name: str
    unit_price: Decimal
    quantity: int
    subtotal: Decimal


class OrderResponse(BaseModel):
    id: UUID
    user_id: UUID
    status: str
    total_amount: Decimal
    items: list[OrderItemResponse]
    created_at: datetime
    updated_at: datetime


class OrdersPage(BaseModel):
    items: list[OrderResponse]
    total: int
    page: int
    size: int
    pages: int

class PaymentRequest(BaseModel):

    model_config = ConfigDict(extra="forbid")

    card_number: str = Field(min_length=12, max_length=19, pattern=r"^\d+$")
    card_holder: str = Field(min_length=1, max_length=100)
    exp_month: int = Field(ge=1, le=12)
    exp_year: int = Field(ge=2020, le=2100)
    cvc: str = Field(min_length=3, max_length=3, pattern=r"^\d{3}$")

class PaymentResponse(BaseModel):
    payment_id: UUID
    status: str
    order_status: str