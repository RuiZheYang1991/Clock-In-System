import os

class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY','mysecret')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'rootpassword')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', '3.89.118.117')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'myapp')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
    POSTGRES_USER = os.environ.get('POSTGRES_USER', 'user')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'password')
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
    POSTGRES_DB = os.environ.get('POSTGRES_DB', 'myapp')
    SQLALCHEMY_BINDS = {
        'postgresql': f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}'
    }