import pytest
from unittest.mock import patch
from src.commands.verOfertas import ViewOffersCommand
from src.commands.verOferta import ViewOfferCommand
from src.models.offer import Offer, db
from src.errors.errors import InvalidFormat, OfferNotFound
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

def test_view_offer_by_id_success(app, offer_data, setup_db, mocker, mock_request):
    try:
        with app.app_context():
            # Simula que la oferta existe en la base de datos
            mock_offer_query = mocker.patch('src.models.offer.Offer.query')
            mock_filter_by = mock_offer_query.filter_by
            mock_first = mock_filter_by.return_value.first
            mock_first.return_value = Offer(**offer_data)

            # Crea el comando para consultar la oferta por su ID
            command = ViewOfferCommand(offer_data['id'])

            # Ejecuta el comando dentro del contexto de la aplicación
            with patch('src.commands.verOferta.request', mock_request):
                # Verifica que la consulta de la oferta por su ID sea exitosa
                response = command.execute()
                assert response.status_code == 200
                
                # Verifica que los datos de la oferta sean correctos en la respuesta
                assert response.json['id'] == offer_data['id']
                assert response.json['description'] == offer_data['description']
                assert response.json['size'] == offer_data['size']
                assert response.json['fragile'] == offer_data['fragile']
                assert response.json['offer'] == offer_data['offer']
    finally:
        with app.app_context():
            patch.stopall()
            
def test_view_offer_by_invalid_id_format(app, offer_data, setup_db, mocker, mock_request):
    try:
        with app.app_context():
            
            invalid_offer_id = "id_no_valido"

            
            mock_offer_query = mocker.patch('src.models.offer.Offer.query')
            mock_filter_by = mock_offer_query.filter_by
            mock_first = mock_filter_by.return_value.first
            mock_first.return_value = None

            
            command = ViewOfferCommand(invalid_offer_id)

            # Ejecuta el comando dentro del contexto de la aplicación
            with patch('src.commands.verOferta.request', mock_request):
                # Verifica que la consulta de la oferta con un ID no válido lance la excepción InvalidFormat
                with pytest.raises(InvalidFormat):
                    command.execute()
                
    finally:
        with app.app_context():
            patch.stopall()