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
        """Normalize the category by making is all lowercase."""
        return v.lower()


class Order(BaseModel):
    """Schema for an order."""

    order_id: str
    customer_id: str
    order_timestamp: datetime
    items: list[Item] = Field(min_length=1)
    currency: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def order_total(self) -> Decimal:
        """Calculate the total price of the order."""
        return sum(  # type: ignore[return-value]
            item.quantity * item.unit_price for item in self.items
        )


class OrderList(BaseModel):
    """List of orders with total attribute."""

    total: int
    orders: list[Order]


class OrderSummary(BaseModel):
    """Summary of the orders."""

    total_orders: int
    total_revenue: Decimal
    average_order_value: Decimal
    orders_per_category: dict[str, int]
    revenue_per_category: dict[str, Decimal]
