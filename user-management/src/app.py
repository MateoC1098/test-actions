# Una aplicación para unirorn
from src.models.user import db
from src.main import create_app

#Crea la aplicación
app = create_app()
with app.app_context():
    db.create_all()