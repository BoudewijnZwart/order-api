from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, computed_field, field_validator


class FailedOrder(BaseModel):
    """Information about a failed order."""

    order_id: str | None
    reason: str


class FailedOrderSummary(BaseModel):
    """Response schema for the bulk creation of orders."""

    ingested: int
    failed: list[FailedOrder]


class Item(BaseModel):
    """Schema for an inventory item."""

    sku: str
    quantity: int = Field(gt=0)
    unit_price: Decimal = Field(ge=0)
    category: str

    @field_validator("category")
    @classmethod
    def normalize_category(cls, v: str) -> str:
        return v.lower()


class Order(BaseModel):
    """Schema for an order."""

    order_id: str
    customer_id: str
    order_timestamp: datetime
    items: list[Item] = Field(min_length=1)
    currency: str

    @computed_field
    def order_total(self) -> Decimal:
        """Calculate the total price of the order."""
        return sum(  # type: ignore[return-value]
            item.quantity * item.unit_price for item in self.items
        )
