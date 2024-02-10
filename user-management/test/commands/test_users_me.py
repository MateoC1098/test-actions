import pytest
from unittest.mock import patch
from flask import Flask, jsonify
from src.commands.users_me import UsersMeCommand
from src.models.user import User, db
from datetime import datetime, timedelta

# Mock para el usuario retornado por la consulta de la base de datos
@pytest.fixture
def mock_user():
    user = User(
        username="testuser",
        email="test@example.com",
        fullName="Test User",
        dni="12345678",
        phoneNumber="1234567890",
        status="VERIFICADO",
        token="valid_token",
        expireAt=datetime.utcnow() + timedelta(hours=2),  # Asegura que el token no ha expirado
        password="testpass",
        salt="salt"
    )

# Prueba: Falta token en el encabezado de la solicitud
def test_users_me_no_token_provided(app):
    with app.test_request_context(headers={'Authorization': ''}):
        command = UsersMeCommand()
        response, status_code = command.execute()
        assert status_code == 403
        assert "El token no está en el encabezado de la solicitud" in response.get_json()["error"]


