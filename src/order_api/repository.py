from order_api import schemas
from order_api.exceptions import OrderAlreadyExistsError
from order_api.services import OrderRepository


class InternalMemoryRepository(OrderRepository):
    """Repository to store orders in-memory."""

    def __init__(self) -> None:
        self.orders: dict[str, schemas.Order] = {}

    def add_order(self, order: schemas.Order) -> None:
        """Add an order."""
        body = order.model_dump()
        key = body.pop("order_id")
        if key in self.orders:
            raise OrderAlreadyExistsError(order_id=key)
        self.orders[key] = body
