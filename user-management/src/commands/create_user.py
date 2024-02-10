from .base_command import BaseCommannd
from src.models.user import User,db
from flask import request, jsonify


#Este método crea un nuevo usuario
class CreateUserCommand(BaseCommannd):
  
    def __init__(self, data):
        self.data = data

    def execute(self):
        username = self.data.get("username")
        password = self.data.get("password")
        email = self.data.get("email")
        dni = self.data.get("dni")
        fullName = self.data.get("fullName")
        phoneNumber = self.data.get("phoneNumber")


        if not username or not password or not email:
            return jsonify({"error": "Username, password, and email son campos requeridos"}), 400

        # Chequea si el usuario o el email ya existen
        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()

        if existing_user or existing_email:
            return jsonify({"error": "Username or email ya existen"}), 412

        # Crea un nuevo usuario
        new_user = User(
            username=username,
            password=password,
            email=email,
            dni=dni,
            fullName=fullName,
            phoneNumber=phoneNumber,
            status="POR_VERIFICAR",  # Init status
            salt="salt"  # Salt
        )

        db.session.add(new_user)
        db.session.commit()

        # Construir respuesta con ID y fecha de creación en formato ISO
        response_data = {
            "id": str(new_user.id),  
            "createdAt": new_user.createdAt.isoformat()  
        }
        return jsonify(response_data), 201
