from collections.abc import Iterable
from functools import lru_cache
from typing import Annotated

from fastapi import Depends, Query

from order_api import schemas
from order_api.repository import InternalMemoryRepository
from order_api.services import OrderFilterBase, OrderService


@lru_cache
def get_repository() -> InternalMemoryRepository:
    """Return"""
    return InternalMemoryRepository()


def get_order_service() -> OrderService:
    """Return an order service with a repository."""
    return OrderService(get_repository())


OrderServiceDep = Annotated[OrderService, Depends(get_order_service)]


class OrderFilters(OrderFilterBase):
    """Filters for listing the orders."""

    def __init__(
        self,
        min_total: int | None = Query(None),
        max_total: int | None = Query(None),
        category: str | None = Query(None),
        customer_id: str | None = Query(None),
    ) -> None:
        """
        Initialize the order filter.

        Raises:
            ValueError: If the supplied filter parameters are not valid.

        """
        if max_total is not None and min_total is not None and max_total <= min_total:
            msg = "Max_total should be larger then min_total"
            raise ValueError(msg)

        self.min_total = min_total
        self.max_total = max_total
        self.category = category
        self.customer_id = customer_id

    def apply(self, orders: Iterable[schemas.Order]) -> list[schemas.Order]:
        """Filter the orders by the supplied query parameters."""
        # Filter for orders where the order_total is larger than the max_total
        if self.min_total is not None:
            orders = [o for o in orders if o.order_total >= self.min_total]

        # Filter for orders where the order_total is smaller than the max_total
        if self.max_total is not None:
            orders = [o for o in orders if o.order_total <= self.max_total]

        # Filter for orders with at least one item with the supplied category
        if self.category is not None:
            orders = [
                o
                for o in orders
                if any(item.category == self.category for item in o.items)
            ]

        # Filter for orders by customer_id
        if self.customer_id is not None:
            orders = [o for o in orders if o.customer_id == self.customer_id]

        return list(orders)


OrderFiltersDep = Annotated[OrderFilters, Depends()]
