from flask import Flask
from .blueprints.views import views

from .models.offer import db

app = Flask(__name__)

try:
    app.config.from_pyfile('config/config.py')
except:
    pass

app.register_blueprint(views)


#app.register_blueprint(views, name="my_views")

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()