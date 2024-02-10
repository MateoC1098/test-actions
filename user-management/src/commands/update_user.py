from .base_command import BaseCommannd
from src.models.user import User, db
from flask import jsonify

class UpdateUserCommand(BaseCommannd):
    def __init__(self, user_id, data):
        self.user_id = user_id
        self.data = data

    def execute(self):
        # Verificar si al menos uno de los campos esperados está presente en la petición
        if not any(field in self.data for field in ["fullName", "phoneNumber", "dni", "status"]):
            return jsonify({"error": "Debe existir al menos un campo fullName, phoneNumber,dni, status"}), 400

        user = User.query.get(self.user_id)
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        # Actualizar los campos proporcionados
        for field in ["fullName", "phoneNumber", "dni", "status"]:
            if field in self.data:
                setattr(user, field, self.data[field])

        db.session.commit()
        return jsonify({"msg": "el usuario ha sido actualizado"}), 200
