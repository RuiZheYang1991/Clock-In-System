from flask import Flask
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from .database import db, migrate
from .mysql.views import mysql_bp
from .mysql.controllers import register_routes as mysql_routes
app = Flask(__name__)
app.config.from_object('config.Config')
api = Api(app)
db.init_app(app)
migrate.init_app(app, db)
app.register_blueprint(mysql_bp)
mysql_routes(api)
# swagger API文檔~~
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  
    '/static/swagger.json',
    config={  
        'app_name': "Clock-in System"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)