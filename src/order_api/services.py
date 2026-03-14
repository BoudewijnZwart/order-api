from abc import ABC, abstractmethod
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
