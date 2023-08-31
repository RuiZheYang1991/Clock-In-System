import os

from flask_swagger_ui import get_swaggerui_blueprint


class Config:
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY','mysecret')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'rootpassword')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', '3.92.139.233')

    # MYSQL_HOST = os.environ.get('MYSQL_HOST', '192.168.0.106')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'myapp')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
    SECURITY_PASSWORD_SALT = os.environ.get('SALT','some_random_salt')
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SECURITY_LOGIN_USER_TEMPLATE = 'security/login.html'
    SECURITY_REGISTERABLE = True
    # POSTGRES_USER = os.environ.get('POSTGRES_USER', 'user')
    # POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'password')
    # POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
    # POSTGRES_DB = os.environ.get('POSTGRES_DB', 'myapp')
    # SQLALCHEMY_BINDS = {
    #     'postgresql': f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}'
    # }



class DevelopmentConfig(Config):
    DEBUG = True
    # ... 其他開發環境特定的配置

class TestingConfig(Config):
    TESTING = True
    # ... 其他測試環境特定的配置

class ProductionConfig(Config):
    # ... 生產環境特定的配置
    DEBUG = False
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'rootpassword')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', '127.0.0.1')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'myapp')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'


def create_swagger_ui():
    SWAGGER_URL = '/api/docs'
    return get_swaggerui_blueprint(
        SWAGGER_URL,
        '/static/swagger.json',
        config={
            'app_name': "Clock-in System"
        }
    ),SWAGGER_URL