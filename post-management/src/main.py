from src import create_app, set_views, set_app_context, set_db
from .blueprints.views import views

app = create_app('config/config.py')


set_views(app,views)
set_app_context(app)
set_db(app)


