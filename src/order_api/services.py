from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Any

from pydantic import ValidationError

from order_api import schemas
from order_api.exceptions import OrderAlreadyExistsError


class OrderRepository(ABC):
    """Base class for all repositories."""

    @abstractmethod
    def add_order(self, order: schemas.Order) -> None:
        """Add an order."""
        ...

    @abstractmethod
    def get_all_orders(self) -> list[schemas.Order]:
        """Return all the orders stored in memory."""


class OrderFilterBase(ABC):
    """Base class for order filters."""

    @abstractmethod
    def apply(self, orders: Iterable[schemas.Order]) -> list[schemas.Order]:
        """Return the filtered orders."""
        ...


class OrderService:
    """Service to store orders using a repository."""

    def __init__(self, repository: OrderRepository) -> None:
        self._repository = repository

    def bulk_create(
        self, raw_orders: list[dict[Any, Any]]
    ) -> schemas.FailedOrderSummary:
        """Create orders in bulk."""
        failed_orders = []
        total_created = 0
        for raw_order in raw_orders:
            # validate the order
            try:
                order = schemas.Order.model_validate(raw_order)
            except ValidationError as e:
                failed_orders.append(
                    schemas.FailedOrder(
                        order_id=raw_order.get("order_id"),
                        reason=", ".join(
                            f"{err.get('loc')}: {err.get('msg')}" for err in e.errors()
                        ),
                    )
                )
                continue

            # attempt to create the order, report failures
            try:
                self._repository.add_order(order)
            except OrderAlreadyExistsError as e:
                failed_orders.append(
                    schemas.FailedOrder(
                        order_id=order.order_id,
                        reason=str(e),
                    )
                )
                continue
            total_created += 1

        return schemas.FailedOrderSummary(ingested=total_created, failed=failed_orders)

    def get_orders(
        self, filters: OrderFilterBase, limit: int, offset: int
    ) -> schemas.OrderList:
        """Return the orders filtered and sorted by timestamp."""
        all_orders = self._repository.get_all_orders()

        # filter
        orders_filtered = filters.apply(all_orders)

        # sort
        orders_sorted = sorted(
            orders_filtered, key=lambda o: o.order_timestamp, reverse=True
        )

        # paginate
        orders_paginated = orders_sorted[offset : offset + limit]
        return schemas.OrderList(total=len(orders_paginated), orders=orders_paginated)
