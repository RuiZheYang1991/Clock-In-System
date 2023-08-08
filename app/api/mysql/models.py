from .. import db
from datetime import datetime
class MySQLModel(db.Model):
    __tablename__ = 'mysql_model'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.String(64))

class Employee(db.Model):
    __tablename__ = 'employee'
    employeeNumber = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    position = db.Column(db.String(50))
    create_time = db.Column(db.DateTime, default=datetime.utcnow)

class ClockRecord(db.Model):
    __tablename__ = 'clock_record'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employeeNumber = db.Column(db.Integer, db.ForeignKey('employee.employeeNumber'), nullable=False)
    clockIn = db.Column(db.DateTime, nullable=True)
    clockOut = db.Column(db.DateTime, nullable=True)
    update_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)