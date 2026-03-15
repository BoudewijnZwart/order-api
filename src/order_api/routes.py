from typing import Any

from fastapi import APIRouter

from order_api import schemas
from order_api.dependencies import OrderServiceDep

API_VERSION_PREFIX = "/orders"

router = APIRouter(prefix=API_VERSION_PREFIX)


@router.post("/batch", response_model=schemas.FailedOrderSummary)
def create_orders_in_batch(
    raw_orders: list[dict[Any, Any]], order_service: OrderServiceDep
) -> Any:
    """
    Endpoint to create orders in bulk.

    The endpoint will not outright deny a request when an order does not
    pass validation, but will return a list of failed requests.
    """
    return order_service.bulk_create(raw_orders=raw_orders)
