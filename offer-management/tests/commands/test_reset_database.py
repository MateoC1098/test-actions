from src.commands.resetDatabase import ResetDatabaseCommand
from unittest.mock import patch

# Test para verificar el reseteo exitoso de la base de datos
def test_reset_database_success(mocker):
    try:
        
        mock_drop_all = mocker.patch('src.models.offer.db.drop_all', autospec=True)
        mock_create_all = mocker.patch('src.models.offer.db.create_all', autospec=True)

        
        command = ResetDatabaseCommand()
        result = command.execute()

        # Verificaciones
        mock_drop_all.assert_called_once()  # Verifica que se llamó al método drop_all
        mock_create_all.assert_called_once()  # Verifica que se llamó al método create_all
        assert result == {"msg": "Todos los datos fueron eliminados"}  # Verifica el mensaje de éxito
    finally:
        # Asegura que todos los mocks se detengan después de la prueba
        patch.stopall()