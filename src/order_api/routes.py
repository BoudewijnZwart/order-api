from typing import Annotated, Any

from fastapi import APIRouter, Query

from order_api import schemas
from order_api.dependencies import OrderFiltersDep, OrderServiceDep

ORDERS_API_PREFIX = "/orders"
STATS_API_PREFIX = "/stats"

orders_router = APIRouter(prefix=ORDERS_API_PREFIX)
stats_router = APIRouter(prefix=STATS_API_PREFIX)


@orders_router.post("/batch", response_model=schemas.FailedOrderSummary)
def create_orders_in_batch(
    raw_orders: list[dict[Any, Any]], order_service: OrderServiceDep
) -> Any:
    """
    Endpoint to create orders in bulk.

    The endpoint will not outright deny a request when an order does not
    pass validation, but will return a list of failed requests.
    """
    return order_service.bulk_create(raw_orders=raw_orders)


@orders_router.get("/", response_model=schemas.OrderList)
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


@stats_router.get("/summary", response_model=schemas.OrderSummary)
def get_order_summary(order_service: OrderServiceDep) -> Any:
    """Endpoint to retrieve a summary of the orders."""
    return order_service.get_stats()
