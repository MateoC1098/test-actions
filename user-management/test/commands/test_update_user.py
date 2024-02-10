import pytest
from unittest.mock import patch, MagicMock
from src.commands.update_user import UpdateUserCommand
from src.models.user import User, db

@pytest.fixture
def setup_db(mocker):
    # Configura el mock para db.session.add y db.session.commit
    mocker.patch.object(db.session, "commit", autospec=True)

@pytest.fixture
def user_data():
    return {
        "fullName": "Updated Test User",
        "phoneNumber": "9876543210",
        "dni": "87654321",
        "status": "VERIFICADO"
    }

def test_update_user_missing_required_fields(app, setup_db):
    with app.app_context():
        command = UpdateUserCommand(user_id="non-existing", data={})
        response, status_code = command.execute()

        assert status_code == 400
        assert "Debe existir al menos un campo fullName, phoneNumber,dni, status" in response.get_json()["error"]
        

def test_update_user_not_found(app, setup_db, user_data):
    with app.app_context():
        with patch('src.models.user.User.query') as mock_query:
            mock_query.get.return_value = None  # Simula que no se encuentra el usuario

            command = UpdateUserCommand(user_id="non-existing", data=user_data)
            response, status_code = command.execute()

            assert status_code == 404
            assert "Usuario no encontrado" in response.get_json()["error"]

def test_update_user_success(app, setup_db, user_data):
    with app.app_context():
        user = User(
            username="testuser",
            email="test@example.com",
            password="testpass",
            salt="salt",
            status="NO_VERIFICADO"
        )

        with patch('src.models.user.User.query') as mock_query:
            mock_query.get.return_value = user  # Simula que se encuentra el usuario

            command = UpdateUserCommand(user_id=user.id, data=user_data)
            response, status_code = command.execute()

            assert status_code == 200
            assert "el usuario ha sido actualizado" in response.get_json()["msg"]
            for key, value in user_data.items():
                assert getattr(user, key) == value  # Asegura que los campos se actualicen correctamente
