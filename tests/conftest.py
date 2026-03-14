import pytest
from fastapi.testclient import TestClient

from order_api.main import app
from order_api.dependencies import get_repository


@pytest.fixture(name="client")
def _test_client_fixture() -> TestClient:
    return TestClient(app=app)


@pytest.fixture(name="repository")
def _repository_fixture() -> None:
    """Clear the repository cache before each test."""
    return get_repository.cache_clear()
