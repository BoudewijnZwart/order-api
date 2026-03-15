from typing import Any

import pytest
from fastapi.testclient import TestClient

from order_api.routes import API_VERSION_PREFIX

_TWO_VALID_ORDERS = [
    {
        "order_id": "A123",
        "customer_id": "C001",
        "order_timestamp": "2024-01-12T14:23:03Z",
        "items": [
            {"sku": "SKU-1", "quantity": 2, "unit_price": 10.5, "category": "books"},
        ],
        "currency": "EUR",
    },
    {
        "order_id": "A124",
        "customer_id": "C002",
        "order_timestamp": "2024-01-12T15:40:00Z",
        "items": [
            {
                "sku": "SKU-2",
                "quantity": 1,
                "unit_price": 25.0,
                "category": "electronics",
            },
        ],
        "currency": "EUR",
    },
]

_INVALID_ORDER_NEGATIVE_UNIT_PRICE = {
    "order_id": "A125",
    "customer_id": "C003",
    "order_timestamp": "2025-01-12T14:23:03Z",
    "items": [
        {"sku": "SKU-5", "quantity": 6, "unit_price": -4.30, "category": "books"},
    ],
    "currency": "EUR",
}

_INVALID_ORDERS_NONPOSITIVE_QUANTITY = [
    {
        "order_id": "A127",
        "customer_id": "C001",
        "order_timestamp": "2024-01-12T14:23:03Z",
        "items": [
            {"sku": "SKU-1", "quantity": 0, "unit_price": 10.5, "category": "books"},
        ],
        "currency": "EUR",
    },
    {
        "order_id": "A128",
        "customer_id": "C002",
        "order_timestamp": "2024-01-12T15:40:00Z",
        "items": [
            {
                "sku": "SKU-2",
                "quantity": -5,
                "unit_price": 25.0,
                "category": "electronics",
            },
        ],
        "currency": "EUR",
    },
]

_INVALID_ORDER_NO_ITEMS = {
    "order_id": "A129",
    "customer_id": "C003",
    "order_timestamp": "2025-01-12T14:23:03Z",
    "items": [],
    "currency": "EUR",
}

_TWO_ORDERS_WITH_DUPLICATE_ORDER_ID = [
    {
        "order_id": "A126",
        "customer_id": "C001",
        "order_timestamp": "2024-01-12T14:23:03Z",
        "items": [
            {"sku": "SKU-1", "quantity": 2, "unit_price": 10.5, "category": "books"},
        ],
        "currency": "EUR",
    },
    {
        "order_id": "A126",
        "customer_id": "C002",
        "order_timestamp": "2024-01-12T15:40:00Z",
        "items": [
            {
                "sku": "SKU-2",
                "quantity": 1,
                "unit_price": 25.0,
                "category": "electronics",
            },
        ],
        "currency": "EUR",
    },
]

_BATCH_ORDER_URL = f"{API_VERSION_PREFIX}/batch"


# --- Tests ---


@pytest.mark.parametrize(
    ("orders", "expected_response"),
    [
        (_TWO_VALID_ORDERS, {"failed": [], "ingested": 2}),
        (
            [_INVALID_ORDER_NEGATIVE_UNIT_PRICE],
            {
                "failed": [
                    {
                        "order_id": "A125",
                        "reason": "('items', 0, 'unit_price'): Input should be greater than or equal to 0",
                    },
                ],
                "ingested": 0,
            },
        ),
        (
            _INVALID_ORDERS_NONPOSITIVE_QUANTITY,
            {
                "failed": [
                    {
                        "order_id": "A127",
                        "reason": "('items', 0, 'quantity'): Input should be greater than 0",
                    },
                    {
                        "order_id": "A128",
                        "reason": "('items', 0, 'quantity'): Input should be greater than 0",
                    },
                ],
                "ingested": 0,
            },
        ),
        (
            [_INVALID_ORDER_NO_ITEMS],
            {
                "failed": [
                    {
                        "order_id": "A129",
                        "reason": "('items',): List should have at least 1 item after validation, not 0",
                    },
                ],
                "ingested": 0,
            },
        ),
        (
            [*_TWO_VALID_ORDERS, _INVALID_ORDER_NO_ITEMS],
            {
                "failed": [
                    {
                        "order_id": "A129",
                        "reason": "('items',): List should have at least 1 item after validation, not 0",
                    },
                ],
                "ingested": 2,
            },
        ),
        (
            _TWO_ORDERS_WITH_DUPLICATE_ORDER_ID,
            {
                "failed": [
                    {
                        "order_id": "A126",
                        "reason": "Order with id 'A126' already exists",
                    },
                ],
                "ingested": 1,
            },
        ),
    ],
)
def test_order_validation_bulk_order_endpoint(
    orders: list[dict[str, Any]],
    expected_response: dict[str, Any],
    client: TestClient,
    repository: None,
) -> None:
    del repository  # only neede for side-effect of clearing the cache before each test
    # GIVEN a list of orders <orders> that might contains invalid orders

    # AND a test client <client>

    # WHEN the batch orders endpoint is called with the list of orders
    response = client.post(_BATCH_ORDER_URL, json=orders)

    # THEN the response status code is 200
    assert response.status_code == 200

    # AND the correct response body is returned
    assert response.json() == expected_response
