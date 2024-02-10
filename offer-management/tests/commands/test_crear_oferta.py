import pytest
from unittest.mock import patch
from src.commands.crearOferta import CreateOfferCommand
from src.models.offer import Offer, db
from src.errors.errors import FieldsMissing, InvalidValues, TokenMissing
from unittest.mock import MagicMock
import uuid

# Fixture para datos de oferta para pruebas
@pytest.fixture
def offer_data():
    """Datos de entrada para crear una oferta."""
    return {
        "postId": str(uuid.uuid4()),
        "description": "Test Offer",
        "size": "LARGE",
        "fragile": False,
        "offer": 50.0
    }

def test_create_offer_success(app, offer_data, setup_db, mocker, mock_request):
    try:
        with app.app_context():
            mock_offer_query = mocker.patch('src.models.offer.Offer.query')
            mock_filter_by = mock_offer_query.filter_by
            mock_first = mock_filter_by.return_value.first
            mock_first.side_effect = [None, None]  
            
            command = CreateOfferCommand(offer_data)
            with patch('src.commands.crearOferta.request', mock_request):
                response, status_code = command.execute()  
                
            response_json = response.get_json()

            # Verificaciones
            assert "id" in response_json  
            assert status_code == 201
    finally:
        with app.app_context():
            patch.stopall()
            
def test_create_offer_with_missing_fields(app, setup_db, mocker, mock_request):
    try:
        with app.app_context():
            mock_offer_query = mocker.patch('src.models.offer.Offer.query')
            mock_filter_by = mock_offer_query.filter_by
            mock_first = mock_filter_by.return_value.first
            mock_first.side_effect = [None, None]

            offer_data_with_missing_fields = {
                "postId": str(uuid.uuid4()), 
                "description": "Test Offer",
                # size, fragile, y offer están faltando
            }

            # Crear comando con datos de oferta con campos faltantes
            command_missing_fields = CreateOfferCommand(offer_data_with_missing_fields)
            command_missing_fields = CreateOfferCommand(offer_data_with_missing_fields)
            with patch('src.commands.crearOferta.request', mock_request):
                # Verificar que se lance la excepción FieldsMissing al ejecutar el comando
                with pytest.raises(FieldsMissing):
                    response_missing_fields, status_code_missing_fields = command_missing_fields.execute()
            # Verificar que se retorne un 400 Bad Request
                    assert status_code_missing_fields == 400
            
    finally:
        with app.app_context():
            patch.stopall()

def test_create_offer_with_invalid_values(app, setup_db, mocker, mock_request):
    try:
        with app.app_context():
            mock_offer_query = mocker.patch('src.models.offer.Offer.query')
            mock_filter_by = mock_offer_query.filter_by
            mock_first = mock_filter_by.return_value.first
            mock_first.side_effect = [None, None]  # Simula que no hay ofertas existentes

            # Datos de la oferta con valores inválidos
            offer_data_with_invalid_values = {
                "postId": str(uuid.uuid4()), 
                "description": "Test Offer",
                "size": "INVALID_SIZE",  # Tamaño de paquete no válido
                "fragile": False,
                "offer": -50.0  # Oferta negativa
            }

            # Crear comando con datos de oferta con valores inválidos
            command_invalid_values = CreateOfferCommand(offer_data_with_invalid_values)
            with patch('src.commands.crearOferta.request', mock_request):
                # Verificar que se lance la excepción InvalidValues al ejecutar el comando
                with pytest.raises(InvalidValues):
                    command_invalid_values.execute()
    finally:
        # Asegura que todos los mocks se detengan después de la prueba
        with app.app_context():
            patch.stopall()

def test_create_offer_without_token(app, offer_data, setup_db, mock_request):
    try:
        with app.app_context():
            mock_offer_query = MagicMock()
            mock_offer_query.filter_by.return_value.first.side_effect = [None, None]

            # Modificar la creación del comando para no incluir el argumento token
            command = CreateOfferCommand(offer_data)

            # Simular que no hay un token presente en la solicitud HTTP
            with patch('src.commands.crearOferta.request', mock_request):
                mock_request.headers = {"Authorization": None}  # Simular que no hay un token presente
                # Verificar que se lance la excepción TokenMissing al ejecutar el comando sin token
                with pytest.raises(TokenMissing):
                    response, status_code = command.execute()

    finally:
        # Asegura que todos los mocks se detengan después de la prueba
        with app.app_context():
            patch.stopall()