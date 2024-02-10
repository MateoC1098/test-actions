from .base_command import BaseCommannd
from src.models.user import User, db
from flask import jsonify

class CreateTokenCommand(BaseCommannd):
    def __init__(self, data):
        self.data = data

    def execute(self):

        # Verificar que ambos campos, username y password, estén presentes en la petición
        if 'username' not in self.data or 'password' not in self.data:
            return jsonify({"error": "Username and password son requeridos"}), 400


        #Se busca el usuario en la base de datos
        username = self.data.get("username")
        password = self.data.get("password")
        user = db.session.query(User).filter(User.username == username, User.password == password).first()

        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        # Genera el token
        user.generate_token()
        db.session.commit() # Guarda el token en la base de datos

        # Construir respuesta con ID, token y fecha de creación en formato ISO
        response_data = {
            "id": str(user.id),  
            "token": user.token,
            "expireAt": user.expireAt.isoformat()  
        }
        
        return jsonify(response_data), 200