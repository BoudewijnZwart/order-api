from typing import Any

import pytest
from fastapi.testclient import TestClient

from order_api.routes import ORDERS_API_PREFIX, STATS_API_PREFIX

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

_BATCH_ORDER_URL = f"{ORDERS_API_PREFIX}/batch"


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


@pytest.mark.parametrize(
    ("query_params", "expected_response"),
    [
        (
            {
                "min_total": 10,
                "max_total": 200_000,
                "category": "electronics",
                "customer_id": "CUST-8834",
                "limit": 5,
                "offset": 0,
            },
            {
                "orders": [
                    {
                        "currency": "USD",
                        "customer_id": "CUST-8834",
                        "items": [
                            {
                                "category": "furniture",
                                "quantity": 1,
                                "sku": "GAMING-CHAIR-PRO",
                                "unit_price": "349.00",
                            },
                            {
                                "category": "electronics",
                                "quantity": 1,
                                "sku": "GAMING-HEADSET-7.1",
                                "unit_price": "89.99",
                            },
                            {
                                "category": "accessories",
                                "quantity": 1,
                                "sku": "MOUSEPAD-XL",
                                "unit_price": "29.99",
                            },
                        ],
                        "order_id": "ORD-0013",
                        "order_timestamp": "2024-06-07T08:40:00Z",
                        "order_total": "468.98",
                    },
                ],
                "total": 1,
            },
        ),
    ],
)
def test_get_orders_endpoint(
    client: TestClient,
    demo_repository: None,
    query_params: dict[str, Any],
    expected_response: dict[str, Any],
) -> None:
    del demo_repository  # only neede for side-effect
    # GIVEN a test client <client>

    # WHEN the get orders endpoint is called
    response = client.get(f"{ORDERS_API_PREFIX}/", params=query_params)

    # THEN the response status code is 200
    assert response.status_code == 200

    # AND the correct response body is returned (empty list)
    assert response.json() == expected_response


def test_get_stats_endpoint(client: TestClient, demo_repository: None) -> None:
    # GIVEN a test client <client>

    # AND a repository with some orders (see demo_repository fixture)
    del demo_repository  # only neede for side-effect

    # WHEN the get orders endpoint is called
    response = client.get(f"{STATS_API_PREFIX}/summary")

    # THEN the response status code is 200
    assert response.status_code == 200

    # AND the correct response body is returned (empty list)
    assert response.json() == {
        "average_order_value": "396.836",
        "orders_per_category": {
            "accessories": 4,
            "apparel": 2,
            "art supplies": 4,
            "books": 2,
            "electronics": 14,
            "footwear": 1,
            "furniture": 3,
            "garden": 3,
            "grocery": 3,
            "health": 3,
            "home": 2,
            "kitchen": 3,
            "sports": 4,
            "toys": 3,
            "travel": 4,
        },
        "revenue_per_category": {
            "accessories": "179.96",
            "apparel": "179.95",
            "art supplies": "142.95",
            "books": "144.85",
            "electronics": "4113.82",
            "footwear": "89.99",
            "furniture": "1297.00",
            "garden": "79.97",
            "grocery": "167.47",
            "health": "128.94",
            "home": "84.95",
            "kitchen": "882.99",
            "sports": "144.97",
            "toys": "83.96",
            "travel": "214.95",
        },
        "total_orders": 20,
        "total_revenue": "7936.72",
    }
