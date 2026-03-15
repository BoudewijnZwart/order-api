from order_api import schemas
from order_api.exceptions import OrderAlreadyExistsError
from order_api.services import OrderRepository


class InternalMemoryRepository(OrderRepository):
    """Repository to store orders in-memory."""

    def __init__(self) -> None:
        self._orders: dict[str, schemas.Order] = {}

    def add_order(self, order: schemas.Order) -> None:
        """Add an order."""
        body = order.model_dump()
        key = body.get("order_id")
        if key in self._orders:
            raise OrderAlreadyExistsError(order_id=key)
        self._orders[key] = body

    def get_all_orders(self) -> list[schemas.Order]:
        """Return all the orders stored in memory."""
        return [schemas.Order(**order) for order in self._orders.values()]
