from typing import Any, Generator

import pytest
from fastapi.testclient import TestClient

from order_api import schemas
from order_api.dependencies import get_order_service, get_repository
from order_api.main import app
from order_api.schemas import Item, Order
from datetime import datetime, timezone
from decimal import Decimal

from order_api.services import OrderService


@pytest.fixture(name="client")
def _test_client_fixture() -> TestClient:
    return TestClient(app=app)


@pytest.fixture(name="repository")
def _repository_fixture() -> None:
    """Clear the repository cache before each test."""
    return get_repository.cache_clear()


_DEMO_ORDERS: list[Order] = [
    Order(
        order_id="ORD-0001",
        customer_id="CUST-1042",
        order_timestamp=datetime(2024, 6, 1, 9, 15, 0, tzinfo=timezone.utc),
        currency="USD",
        items=[
            Item(
                sku="LAPTOP-PRO-15",
                quantity=1,
                unit_price=Decimal("1299.99"),
                category="Electronics",
            ),
            Item(
                sku="MOUSE-WIRELESS",
                quantity=1,
                unit_price=Decimal("39.99"),
                category="Electronics",
            ),
        ],
    ),
    Order(
        order_id="ORD-0002",
        customer_id="CUST-2371",
        order_timestamp=datetime(2024, 6, 1, 10, 30, 0, tzinfo=timezone.utc),
        currency="USD",
        items=[
            Item(
                sku="DESK-STANDING-ADJ",
                quantity=1,
                unit_price=Decimal("549.00"),
                category="Furniture",
            ),
            Item(
                sku="CHAIR-ERGONOMIC",
                quantity=1,
                unit_price=Decimal("399.00"),
                category="Furniture",
            ),
            Item(
                sku="MONITOR-27IN-4K",
                quantity=2,
                unit_price=Decimal("449.99"),
                category="Electronics",
            ),
        ],
    ),
    Order(
        order_id="ORD-0003",
        customer_id="CUST-0891",
        order_timestamp=datetime(2024, 6, 2, 8, 0, 0, tzinfo=timezone.utc),
        currency="GBP",
        items=[
            Item(
                sku="BOOK-PYTHON-ADV",
                quantity=2,
                unit_price=Decimal("49.95"),
                category="Books",
            ),
            Item(
                sku="BOOK-CLEAN-CODE",
                quantity=1,
                unit_price=Decimal("44.95"),
                category="Books",
            ),
        ],
    ),
    Order(
        order_id="ORD-0004",
        customer_id="CUST-3304",
        order_timestamp=datetime(2024, 6, 2, 14, 45, 0, tzinfo=timezone.utc),
        currency="EUR",
        items=[
            Item(
                sku="HEADPHONES-NC700",
                quantity=1,
                unit_price=Decimal("379.00"),
                category="Electronics",
            ),
        ],
    ),
    Order(
        order_id="ORD-0005",
        customer_id="CUST-1190",
        order_timestamp=datetime(2024, 6, 3, 11, 20, 0, tzinfo=timezone.utc),
        currency="USD",
        items=[
            Item(
                sku="TSHIRT-BASIC-M",
                quantity=3,
                unit_price=Decimal("19.99"),
                category="Apparel",
            ),
            Item(
                sku="JEANS-SLIM-32",
                quantity=2,
                unit_price=Decimal("59.99"),
                category="Apparel",
            ),
            Item(
                sku="SNEAKERS-RUN-42",
                quantity=1,
                unit_price=Decimal("89.99"),
                category="Footwear",
            ),
        ],
    ),
    Order(
        order_id="ORD-0006",
        customer_id="CUST-5577",
        order_timestamp=datetime(2024, 6, 3, 16, 0, 0, tzinfo=timezone.utc),
        currency="USD",
        items=[
            Item(
                sku="COFFEE-ARABICA-1KG",
                quantity=5,
                unit_price=Decimal("18.50"),
                category="Grocery",
            ),
            Item(
                sku="TEA-GREEN-100G",
                quantity=3,
                unit_price=Decimal("9.99"),
                category="Grocery",
            ),
            Item(
                sku="FRENCH-PRESS-800ML",
                quantity=1,
                unit_price=Decimal("34.99"),
                category="Kitchen",
            ),
        ],
    ),
    Order(
        order_id="ORD-0007",
        customer_id="CUST-2048",
        order_timestamp=datetime(2024, 6, 4, 9, 5, 0, tzinfo=timezone.utc),
        currency="CAD",
        items=[
            Item(
                sku="TABLET-10IN-128GB",
                quantity=1,
                unit_price=Decimal("499.00"),
                category="Electronics",
            ),
            Item(
                sku="TABLET-CASE-10IN",
                quantity=1,
                unit_price=Decimal("29.99"),
                category="Accessories",
            ),
            Item(
                sku="STYLUS-PEN-PRO",
                quantity=1,
                unit_price=Decimal("79.99"),
                category="Accessories",
            ),
        ],
    ),
    Order(
        order_id="ORD-0008",
        customer_id="CUST-6612",
        order_timestamp=datetime(2024, 6, 4, 13, 30, 0, tzinfo=timezone.utc),
        currency="USD",
        items=[
            Item(
                sku="YOGA-MAT-PRO",
                quantity=1,
                unit_price=Decimal("65.00"),
                category="Sports",
            ),
            Item(
                sku="RESISTANCE-BAND-SET",
                quantity=1,
                unit_price=Decimal("24.99"),
                category="Sports",
            ),
            Item(
                sku="WATER-BOTTLE-1L",
                quantity=2,
                unit_price=Decimal("14.99"),
                category="Sports",
            ),
            Item(
                sku="GYM-TOWEL-MICRO",
                quantity=2,
                unit_price=Decimal("12.50"),
                category="Sports",
            ),
        ],
    ),
    Order(
        order_id="ORD-0009",
        customer_id="CUST-3389",
        order_timestamp=datetime(2024, 6, 5, 7, 50, 0, tzinfo=timezone.utc),
        currency="USD",
        items=[
            Item(
                sku="SSD-EXTERNAL-1TB",
                quantity=2,
                unit_price=Decimal("109.99"),
                category="Electronics",
            ),
        ],
    ),
    Order(
        order_id="ORD-0010",
        customer_id="CUST-7723",
        order_timestamp=datetime(2024, 6, 5, 15, 10, 0, tzinfo=timezone.utc),
        currency="EUR",
        items=[
            Item(
                sku="PLANT-MONSTERA-LG",
                quantity=1,
                unit_price=Decimal("45.00"),
                category="Garden",
            ),
            Item(
                sku="PLANT-POT-25CM",
                quantity=2,
                unit_price=Decimal("12.99"),
                category="Garden",
            ),
            Item(
                sku="POTTING-MIX-5L",
                quantity=1,
                unit_price=Decimal("8.99"),
                category="Garden",
            ),
        ],
    ),
    Order(
        order_id="ORD-0011",
        customer_id="CUST-4401",
        order_timestamp=datetime(2024, 6, 6, 10, 0, 0, tzinfo=timezone.utc),
        currency="USD",
        items=[
            Item(
                sku="WEBCAM-4K-USB",
                quantity=1,
                unit_price=Decimal("149.99"),
                category="Electronics",
            ),
            Item(
                sku="MIC-CONDENSER-USB",
                quantity=1,
                unit_price=Decimal("99.99"),
                category="Electronics",
            ),
            Item(
                sku="RING-LIGHT-12IN",
                quantity=1,
                unit_price=Decimal("54.99"),
                category="Electronics",
            ),
            Item(
                sku="DESK-MOUNT-ARM",
                quantity=1,
                unit_price=Decimal("39.99"),
                category="Accessories",
            ),
        ],
    ),
    Order(
        order_id="ORD-0012",
        customer_id="CUST-0055",
        order_timestamp=datetime(2024, 6, 6, 12, 25, 0, tzinfo=timezone.utc),
        currency="GBP",
        items=[
            Item(
                sku="CANDLE-SOY-LAVENDER",
                quantity=4,
                unit_price=Decimal("14.99"),
                category="Home",
            ),
            Item(
                sku="DIFFUSER-REED-200ML",
                quantity=1,
                unit_price=Decimal("24.99"),
                category="Home",
            ),
        ],
    ),
    Order(
        order_id="ORD-0013",
        customer_id="CUST-8834",
        order_timestamp=datetime(2024, 6, 7, 8, 40, 0, tzinfo=timezone.utc),
        currency="USD",
        items=[
            Item(
                sku="GAMING-CHAIR-PRO",
                quantity=1,
                unit_price=Decimal("349.00"),
                category="Furniture",
            ),
            Item(
                sku="GAMING-HEADSET-7.1",
                quantity=1,
                unit_price=Decimal("89.99"),
                category="Electronics",
            ),
            Item(
                sku="MOUSEPAD-XL",
                quantity=1,
                unit_price=Decimal("29.99"),
                category="Accessories",
            ),
        ],
    ),
    Order(
        order_id="ORD-0014",
        customer_id="CUST-2267",
        order_timestamp=datetime(2024, 6, 7, 17, 55, 0, tzinfo=timezone.utc),
        currency="AUD",
        items=[
            Item(
                sku="SUNSCREEN-SPF50-200ML",
                quantity=3,
                unit_price=Decimal("12.99"),
                category="Health",
            ),
            Item(
                sku="VITAMIN-D3-90CAPS",
                quantity=2,
                unit_price=Decimal("19.99"),
                category="Health",
            ),
            Item(
                sku="PROTEIN-POWDER-1KG",
                quantity=1,
                unit_price=Decimal("49.99"),
                category="Health",
            ),
        ],
    ),
    Order(
        order_id="ORD-0015",
        customer_id="CUST-9910",
        order_timestamp=datetime(2024, 6, 8, 9, 30, 0, tzinfo=timezone.utc),
        currency="USD",
        items=[
            Item(
                sku="KEYBOARD-MECH-TKL",
                quantity=1,
                unit_price=Decimal("129.99"),
                category="Electronics",
            ),
        ],
    ),
    Order(
        order_id="ORD-0016",
        customer_id="CUST-1563",
        order_timestamp=datetime(2024, 6, 8, 14, 0, 0, tzinfo=timezone.utc),
        currency="USD",
        items=[
            Item(
                sku="SKETCHBOOK-A4-200PG",
                quantity=2,
                unit_price=Decimal("16.99"),
                category="Art Supplies",
            ),
            Item(
                sku="WATERCOLOR-SET-24",
                quantity=1,
                unit_price=Decimal("34.99"),
                category="Art Supplies",
            ),
            Item(
                sku="BRUSH-SET-PRO-12PC",
                quantity=1,
                unit_price=Decimal("28.99"),
                category="Art Supplies",
            ),
            Item(
                sku="EASEL-TABLETOP",
                quantity=1,
                unit_price=Decimal("44.99"),
                category="Art Supplies",
            ),
        ],
    ),
    Order(
        order_id="ORD-0017",
        customer_id="CUST-6078",
        order_timestamp=datetime(2024, 6, 9, 11, 10, 0, tzinfo=timezone.utc),
        currency="EUR",
        items=[
            Item(
                sku="ESPRESSO-MACHINE-PRO",
                quantity=1,
                unit_price=Decimal("699.00"),
                category="Kitchen",
            ),
            Item(
                sku="COFFEE-GRINDER-BURR",
                quantity=1,
                unit_price=Decimal("149.00"),
                category="Kitchen",
            ),
            Item(
                sku="COFFEE-BEANS-BLEND-1KG",
                quantity=2,
                unit_price=Decimal("22.50"),
                category="Grocery",
            ),
        ],
    ),
    Order(
        order_id="ORD-0018",
        customer_id="CUST-3345",
        order_timestamp=datetime(2024, 6, 9, 16, 45, 0, tzinfo=timezone.utc),
        currency="USD",
        items=[
            Item(
                sku="PUZZLE-1000PC-WORLD",
                quantity=1,
                unit_price=Decimal("22.99"),
                category="Toys",
            ),
            Item(
                sku="BOARD-GAME-SETTLERS",
                quantity=1,
                unit_price=Decimal("44.99"),
                category="Toys",
            ),
            Item(
                sku="PLAYING-CARDS-2PK",
                quantity=2,
                unit_price=Decimal("7.99"),
                category="Toys",
            ),
        ],
    ),
    Order(
        order_id="ORD-0019",
        customer_id="CUST-5521",
        order_timestamp=datetime(2024, 6, 10, 8, 20, 0, tzinfo=timezone.utc),
        currency="USD",
        items=[
            Item(
                sku="BACKPACK-TRAVEL-45L",
                quantity=1,
                unit_price=Decimal("119.99"),
                category="Travel",
            ),
            Item(
                sku="PACKING-CUBES-SET6",
                quantity=1,
                unit_price=Decimal("29.99"),
                category="Travel",
            ),
            Item(
                sku="TRAVEL-ADAPTER-UNIV",
                quantity=1,
                unit_price=Decimal("24.99"),
                category="Travel",
            ),
            Item(
                sku="NECK-PILLOW-MEMORY",
                quantity=2,
                unit_price=Decimal("19.99"),
                category="Travel",
            ),
        ],
    ),
    Order(
        order_id="ORD-0020",
        customer_id="CUST-8899",
        order_timestamp=datetime(2024, 6, 10, 13, 0, 0, tzinfo=timezone.utc),
        currency="USD",
        items=[
            Item(
                sku="SMART-SPEAKER-MINI",
                quantity=2,
                unit_price=Decimal("49.99"),
                category="Electronics",
            ),
            Item(
                sku="SMART-BULB-E27-4PK",
                quantity=3,
                unit_price=Decimal("34.99"),
                category="Electronics",
            ),
            Item(
                sku="SMART-PLUG-2PK",
                quantity=2,
                unit_price=Decimal("22.99"),
                category="Electronics",
            ),
        ],
    ),
]


class DemoRepository:
    """A demo repository that can be used in tests."""

    def get_all_orders(self) -> list[schemas.Order]:
        """Return all the orders stored in memory."""
        return _DEMO_ORDERS


def get_service_with_demo_repository() -> DemoRepository:
    """Return a demo repository."""
    return OrderService(repository=DemoRepository())


@pytest.fixture(name="demo_repository")
def _demo_repository_fixture() -> Generator[Any, None, None]:
    """Clear the repository cache before each test."""
    app.dependency_overrides[get_order_service] = get_service_with_demo_repository
    yield
    app.dependency_overrides.pop(get_order_service)
