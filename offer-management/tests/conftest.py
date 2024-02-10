import pytest
from src.app import app as _app, db
from unittest.mock import MagicMock
import uuid

@pytest.fixture(scope="module")
def app():
    app = _app
    app.config["TESTING"] = True
    with app.app_context():
        yield app

@pytest.fixture
def setup_db(mocker):
    """Configura el mock de la base de datos."""
    mocker.patch.object(db.session, "add", autospec=True)
    mocker.patch.object(db.session, "commit", autospec=True)

@pytest.fixture
def mock_request():
    """Simula la solicitud HTTP."""
    mock = MagicMock()
    mock.headers = {"Authorization": f"Bearer {uuid.uuid4()}"}
    return mock