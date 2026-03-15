class OrderAlreadyExistsError(Exception):
    """Raised when an order already exists."""

    def __init__(self, order_id: str) -> None:
        self.order_id = order_id
        super().__init__(f"Order with id '{order_id}' already exists")
