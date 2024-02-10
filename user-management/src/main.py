from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from .blueprints.operations import operations_blueprint
from .errors.errors import ApiError
from src.models.user import db
import os

def create_app(test_config=None):
    app = Flask(__name__)
    
    if test_config is None:
        # Carga la configuración de la instancia si no se está ejecutando en un contexto de prueba
        app.config.from_object('src.instance.config')
        db.init_app(app)
    else:
        # Carga la configuración de prueba si se ha pasado
        app.config.update(test_config)
    
    app.register_blueprint(operations_blueprint)

    @app.errorhandler(ApiError)
    def handle_exception(err):
        response = {
            "mssg": err.description,
            "version": os.environ.get("VERSION", "1.0")
        }
        return jsonify(response), err.code

    return app