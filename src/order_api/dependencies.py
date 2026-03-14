from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from order_api.repository import InternalMemoryRepository
from order_api.services import OrderService


@lru_cache
def get_repository() -> InternalMemoryRepository:
    """Return"""
    return InternalMemoryRepository()


def get_order_service() -> OrderService:
    """Return an order service with a repository."""
    return OrderService(get_repository())


OrderServiceDep = Annotated[OrderService, Depends(get_order_service)]
