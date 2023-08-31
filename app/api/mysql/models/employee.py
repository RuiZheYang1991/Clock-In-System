from api.database import db
from datetime import datetime


class Employee(db.Model):
    __tablename__ = 'employee'

    # Existing fields
    employee_number = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=True)
    position = db.Column(db.String(50), nullable=True)
    create_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=True)
    phone_number = db.Column(db.String(15),unique=True, nullable=True)  # Phone number
    gender = db.Column(db.String(10), nullable=True)  # Gender
    department = db.Column(db.String(50), nullable=True)  # Department
    birth_date = db.Column(db.Date, nullable=True)
    address = db.Column(db.String(200), nullable=True)  # Address
    salary = db.Column(db.Integer, nullable=True)  # Salary
    nationality = db.Column(db.String(50), nullable=True)  # Nationality

class ClockRecord(db.Model):
    __tablename__ = 'clock_record'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_number = db.Column(db.Integer, db.ForeignKey('employee.employee_number'), nullable=False)
    clock_in = db.Column(db.DateTime, nullable=True)
    clock_out = db.Column(db.DateTime, nullable=True)
    update_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)