import pytest
from unittest.mock import patch
from src.commands.verOfertas import ViewOffersCommand
from src.models.offer import Offer, db
from src.errors.errors import InvalidFormat
import uuid

# Fixture para datos de oferta para pruebas
@pytest.fixture
def offer_data():
    """Datos de oferta para pruebas."""
    return {
        "id": str(uuid.uuid4()),
        "postId": str(uuid.uuid4()),
        "description": "Test Offer",
        "size": "LARGE",
        "fragile": False,
        "offer": 50.0
    }
            
def test_view_offers_invalid_format(app, offer_data, setup_db, mocker, mock_request):
    try:
        with app.app_context():
            # Crea el comando para consultar las ofertas con un formato inválido
            command = ViewOffersCommand(post_id=12345)  # Suponiendo que un número entero es un formato inválido

            # Ejecuta el comando dentro del contexto de la aplicación
            with patch('src.commands.verOfertas.request', mock_request):
                # Verifica que la consulta de las ofertas con un formato inválido lance la excepción InvalidFormat
                with pytest.raises(InvalidFormat):
                    command.execute()
                
    finally:
        with app.app_context():
            patch.stopall()
