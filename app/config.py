import os

class Config:

    SECRET_KEY = 'mysecret'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'rootpassword')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', '3.89.118.117')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'myapp')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'

