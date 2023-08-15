from flask import Flask
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from .utils.request_hooks import before_request, after_request
from .database import db, migrate
from api.mysql.controllers.controller import mysql_bp
from .postgresql.views import postgresql_bp
from .mysql.routes import register_routes as mysql_routes
from api.views import views_bp
app = Flask(__name__)
app.config.from_object('config.Config')
api = Api(app)
db.init_app(app)
migrate.init_app(app, db)

# app.before_request(before_request)
# app.after_request(after_request)
app.register_blueprint(views_bp)
app.register_blueprint(mysql_bp)
app.register_blueprint(postgresql_bp)
mysql_routes(api)
# swagger API文檔~~
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be served in this directory
    '/static/swagger.json',
    config={  # Swagger UI config overrides
        'app_name': "Clock-in System"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)