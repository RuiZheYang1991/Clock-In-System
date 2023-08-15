from flask import Blueprint
from flask_restful import Resource

from .models import PostgreSQLModel

postgresql_bp = Blueprint('postgresql', __name__)

class PostgreSQLAPI(Resource):
    def get(self):
        return {item.id: item.data for item in PostgreSQLModel.query.all()}