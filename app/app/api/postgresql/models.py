from .. import db

class PostgreSQLModel(db.Model):
    __tablename__ = 'postgresql_model'

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(64))