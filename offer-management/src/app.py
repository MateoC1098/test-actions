from flask import Flask, jsonify
from .blueprints.views import views
from .errors.errors import ApiError
import os 

from .models.offer import db
 
def create_app(test_config=None):
    app = Flask(__name__)
    
    if test_config is None:
        app.config.from_pyfile('config/config.py')
        db.init_app(app)
         
    else:
        app.config.update(test_config)
        
    app.register_blueprint(views)
    
    @app.errorhandler(ApiError)
    def handle_exception(err):
        response = {
            "mssg": err.description,
            "version": os.environ.get("VERSION", "1.0")
        }
        return jsonify(response), err.code
    
    return app


app = create_app()
with app.app_context():
    db.create_all()