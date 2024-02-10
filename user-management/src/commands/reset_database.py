from .base_command import BaseCommannd
from src.models.user import User, db
from flask import jsonify

class ResetDatabaseCommand(BaseCommannd):
    def execute(self):
        try:
            # Eliminar todos los registros de la tabla de usuarios
            num_rows_deleted = db.session.query(User).delete()
            db.session.commit()
            return jsonify({"msg": "Todos los datos fueron eliminados"}), 200
        except Exception as e:
            db.session.rollback()
            # Considera registrar el error e
            return jsonify({"error": "Error al restablecer la base de datos"}), 500
