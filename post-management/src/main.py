from flask import Flask
from .blueprints.views import views

from .models.publicacion import db

app = Flask(__name__)

try:
    app.config.from_pyfile('config/config.py')
except:
    pass

app.register_blueprint(views)

app_context = app.app_context()
app_context.push()

try:
    db.init_app(app)
    db.create_all()
    print("Conexión a la base de datos establecida correctamente.")
except:
    print("Error al conectar a la base de datos.")


