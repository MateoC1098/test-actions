from src.commands.reset_database import ResetDatabaseCommand
from unittest.mock import patch

# Test para verificar el reseteo exitoso de la base de datos
def test_reset_database_success(app, mocker):
    try:
        with app.app_context():
            # Mockear el método 'delete' y 'commit' de la sesión de la base de datos
            mock_delete = mocker.patch('sqlalchemy.orm.query.Query.delete', autospec=True)
            mock_commit = mocker.patch('sqlalchemy.orm.scoping.scoped_session.commit', autospec=True)

            # Ejecutar el comando para resetear la base de datos
            command = ResetDatabaseCommand()
            response, status_code = command.execute()

            # Verificaciones
            mock_delete.assert_called_once()  # Verifica que se llamó al método delete
            mock_commit.assert_called_once()  # Verifica que se llamó al método commit
            assert status_code == 200  # Verifica que el código de estado sea 200 (OK)
            assert "Todos los datos fueron eliminados" in response.get_json()["msg"]  # Verifica el mensaje de éxito
    finally:
        # Asegura que todos los mocks se detengan después de la prueba
        with app.app_context():
            patch.stopall()        
