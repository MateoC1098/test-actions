# tests/conftest.py
import pytest
from src.main import create_app, db

@pytest.fixture(scope="session")
def app():
    """Fixture de aplicación Flask para pruebas."""
    app = create_app({
        "TESTING": True,
    })
    yield app