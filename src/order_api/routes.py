from typing import Annotated, Any

from fastapi import APIRouter, Query

from order_api import schemas
from order_api.dependencies import OrderFiltersDep, OrderServiceDep

ORDERS_API_PREFIX = "/orders"

router = APIRouter(prefix=ORDERS_API_PREFIX)


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


@router.get("/", response_model=schemas.OrderList)
def get_orders(
    order_service: OrderServiceDep,
    filters: OrderFiltersDep,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> Any:
    """Retrieve orders with optional filtering and pagination."""
    return order_service.get_orders(
        filters=filters,
        limit=limit,
        offset=offset,
    )
