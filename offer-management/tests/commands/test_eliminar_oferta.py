import pytest
from unittest.mock import patch
from src.commands.eliminarOferta import DeleteOfferCommand
from src.models.offer import Offer, db
from flask import Response
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

def test_delete_offer_success(app, offer_data, setup_db, mocker, mock_request):
    try:
        with app.app_context():
            # Simula que la oferta existe en la base de datos
            mock_offer_query = mocker.patch('src.models.offer.Offer.query')
            mock_filter_by = mock_offer_query.filter_by
            mock_first = mock_filter_by.return_value.first
            mock_first.return_value = None

            # Crea el comando para eliminar la oferta
            command = DeleteOfferCommand(offer_data['id'])

            # Ejecuta el comando dentro del contexto de la aplicación
            with patch('src.commands.eliminarOferta.request', mock_request):
                # Verifica que la eliminación de la oferta sea exitosa
                response = command.execute()
                
                assert isinstance(response, tuple)
                assert isinstance(response[0], Response)
                assert response[0].json == {"msg": "la oferta fue eliminada"}
                assert response[1] == 200
                
                # Verifica que la oferta ya no exista en la base de datos
                assert not Offer.query.get(offer_data['id']) is None
    finally:
        with app.app_context():
            patch.stopall()