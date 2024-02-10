from .baseCommand import BaseCommand
from ..models.offer import db

class ResetDatabaseCommand(BaseCommand):
    def execute(self):
        db.drop_all()
        db.create_all()
        return {"msg": "Todos los datos fueron eliminados"}