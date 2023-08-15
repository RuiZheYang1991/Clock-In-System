from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
#set FLASK_APP=run.py
# flask --app run.py db init
# flask --app run.py db migrate -m "Initial migration"
#flask --app run.py db upgrade