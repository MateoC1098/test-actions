# Importaciones necesarias
import pytest
from unittest.mock import patch
from src.commands.create_user import CreateUserCommand
from src.models.user import User, db
from unittest.mock import MagicMock

# Test para verificar el manejo de un username o email existente
@pytest.fixture
def existing_user_data():
    """Datos de un usuario existente."""
    return User(
        username="testuser",
        email="test@example.com",
        password="testpass",
        salt="salt",
        status="active",
        dni="12345678",
        fullName="Test User",
        phoneNumber="1234567890"
    )


# Usamos pytest.fixture para inicializar nuestra base de datos de prueba y otras configuraciones necesarias
@pytest.fixture
def user_data():
    """Datos de entrada para crear un usuario."""
    return {
        "username": "testuser",
        "password": "testpass",
        "email": "test@example.com",
        "dni": "12345678",
        "fullName": "Test User",
        "phoneNumber": "1234567890"
    }

@pytest.fixture
def setup_db(mocker):
    """Configura el mock de la base de datos."""
    mocker.patch.object(db.session, "add", autospec=True)
    mocker.patch.object(db.session, "commit", autospec=True)

# Test para verificar la creación exitosa de un usuario
def test_create_user_success(app, user_data, setup_db, mocker):
    try:
        with app.app_context():
            # Mockear el método filter_by directamente puede ser complicado debido a cómo Flask-SQLAlchemy maneja las queries
            # Una solución es mockear la query completa
            mock_query = mocker.patch('src.models.user.User.query')
            mock_filter_by = mock_query.filter_by
            mock_first = mock_filter_by.return_value.first
            mock_first.side_effect = [None, None]  # Simula que no hay usuarios existentes

            command = CreateUserCommand(user_data)
            response, status_code = command.execute()  # Desempaquetar la tupla

            # Ahora puedes acceder al contenido JSON de la respuesta y al código de estado
            response_json = response.get_json()  # Obtiene el contenido JSON de la respuesta
            #print(response_json)  # Imprimir el contenido JSON para depuración

            # Verificaciones
            assert "id" in response_json  # Verificar que el contenido JSON incluya el ID
            assert status_code == 201  # Verificar que el código de estado sea 201
    finally:
        # Asegura que todos los mocks se detengan después de la prueba
        with app.app_context():
            patch.stopall()


# Test para verificar el manejo de un username o email existente
def test_create_user_existing_username_or_email(app, user_data, setup_db, mocker, existing_user_data):
    try:
        with app.app_context():
            # Configuramos el mock para simular que ya existe un usuario con ese username o email
            mock_query = mocker.patch('src.models.user.User.query')
            mock_filter_by_username = mock_query.filter_by.return_value.filter_by
            mock_filter_by_email = mock_query.filter_by.return_value.filter_by
            # Simulamos que la primera llamada a filter_by (para username) retorna None (usuario no encontrado por username)
            # y la segunda llamada (para email) retorna un usuario existente
            mock_filter_by_username.return_value.first.side_effect = [None, existing_user_data]
            mock_filter_by_email.return_value.first.side_effect = [existing_user_data, None]

            command = CreateUserCommand(user_data)
            response, status_code = command.execute()

            #print(response)

            # Verificaciones
            assert status_code == 412  # Verifica que el código de estado sea 412 (Precondition Failed)
            assert "error" in response.get_json()  # Verifica que la respuesta contiene un mensaje de error
            assert "Username or email ya existen" in response.get_json()["error"]  # Mensaje de error esperado
    finally:
        # Asegura que todos los mocks se detengan después de la prueba
        with app.app_context():
            patch.stopall()

# Test para verificar que se devuelve un error cuando falta username, password o email
@pytest.mark.parametrize("missing_field", [
    {"password": "testpass", "email": "test@example.com"},  # Falta username
    {"username": "testuser", "email": "test@example.com"},  # Falta password
    {"username": "testuser", "password": "testpass"},       # Falta email
])
def test_create_user_missing_required_fields(app, setup_db, mocker, missing_field):
    with app.app_context():
        command = CreateUserCommand(missing_field)
        response, status_code = command.execute()

        # Verificaciones
        assert status_code == 400  # Verifica que el código de estado sea 400 (Bad Request)
        assert "error" in response.get_json()  # Verifica que la respuesta contiene un mensaje de error
        assert "Username, password, and email son campos requeridos" in response.get_json()["error"]  # Mensaje de error esperado
            
