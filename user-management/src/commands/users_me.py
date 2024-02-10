from flask import request, jsonify
from .base_command import BaseCommannd
from src.models.user import User, db
from datetime import datetime

class UsersMeCommand(BaseCommannd):
    def __init__(self):
        # No necesita argumentos para el constructor, obtendrá el token directamente de la solicitud
        pass

    def execute(self):
        # Extraer el token del encabezado de la solicitud dentro del comando
        authorization_header = request.headers.get('Authorization', '')
        if not authorization_header.startswith('Bearer '):
            return jsonify({"error": "El token no está en el encabezado de la solicitud"}), 403
        
        token = authorization_header.split(' ')[1]

        user = db.session.query(User).filter(User.token == token, User.expireAt > datetime.utcnow()).first()
        if not user:
            return jsonify({"error": "El token no es válido o está vencido."}), 401

        user_data = {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "fullName": user.fullName,
            "dni": user.dni,
            "phoneNumber": user.phoneNumber,
            "status": user.status.name if hasattr(user.status, 'name') else user.status # Si el estado es un string, no tiene el atributo name
        }

        # Devolver los datos del usuario en formato JSON
        return jsonify(user_data), 200
