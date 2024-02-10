import pytest
from unittest.mock import patch, MagicMock
from src.commands.create_token import CreateTokenCommand
from src.models.user import User, db
from datetime import datetime, timedelta



# Fixture para configurar un usuario de prueba
@pytest.fixture
def user():
    return User(
        username="valid_user",
        email="user@example.com",
        password="valid_password",
        salt="salt",  # 
        status="VERIFICADO",
        token="existing_token",  # Token existente para simular un usuario que ya tiene un token
        expireAt=datetime.utcnow() + timedelta(hours=1)  # Token no expirado
    )


# Prueba: Falta de campos requeridos
@pytest.mark.parametrize("data", [
    {"username": "valid_user"},  # Falta password
    {"password": "valid_password"},  # Falta username
    {}  # Falta ambos
])
def test_create_token_missing_fields(app, data):
    with app.app_context():
        command = CreateTokenCommand(data)
        response, status_code = command.execute()

        assert status_code == 400
        assert "error" in response.get_json()