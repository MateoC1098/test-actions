from flask import Flask
from .models.publicacion import db
from .blueprints.views import views

def create_app(config_filename):
    app = Flask(__name__)
    try:
        app.config.from_pyfile(config_filename)
    except:
        pass
    return app

def set_views(app, views=views):
    app.register_blueprint(views)

def set_app_context(app):
    app_context = app.app_context()
    app_context.push()

def set_db(app):
    db.init_app(app)
    db.create_all()
    print("Conexión a la base de datos establecida correctamente.")