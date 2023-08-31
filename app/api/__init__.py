from flask import Flask, render_template, request, redirect, url_for, flash
from flask_restful import Api
from werkzeug.security import generate_password_hash
from api.mysql.models.user import User, Role
from config import DevelopmentConfig, TestingConfig, ProductionConfig
from .admin.auth import auth
from .utils.request_hooks import before_request, after_request
from .database import db, migrate
from api.mysql.controllers.controller import mysql_bp
from .mysql.routes import register_routes as mysql_routes
from flask_admin import Admin, AdminIndexView
from api.admin.admin_view import EmployeeModelView, MyAdminIndexView, EmployeeRecordView, EarlyClockView
from api.mysql.models.employee import Employee
from flask_babelex import Babel
from flask_security import Security, SQLAlchemyUserDatastore
from flask_login import LoginManager, login_user, logout_user
from .form.admin.login_form import LoginForm
from config import create_swagger_ui

config = {
    'dev': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    api = Api(app)
    db.init_app(app)
    migrate.init_app(app, db)

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    # security = Security(app, user_datastore)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    #
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.before_first_request
    def create_user():
        admin_name = 'admin'
        admin_mail = 'admin@example.com'
        hash = generate_password_hash(admin_name)
        db.create_all()
        if not Role.query.filter_by(name=admin_name).first():
            user_datastore.create_role(name=admin_name)
        if not User.query.filter_by(email=admin_mail).first():
            user_datastore.create_user(email=admin_mail, password=hash)
        db.session.commit()
        admin_role = Role.query.filter_by(name=admin_name).first()
        admin_user = User.query.filter_by(email=admin_mail).first()
        user_datastore.add_role_to_user(admin_user, admin_role)
        db.session.commit()

    app.register_blueprint(mysql_bp)
    app.register_blueprint(auth)

    # admin
    admin = Admin(app, name='員工管理系統', template_mode='bootstrap3', index_view=MyAdminIndexView())
    admin.add_view(EmployeeModelView(Employee, db.session,name='員工資料'))
    admin.add_view(EmployeeRecordView(name='打卡紀錄', endpoint='employee_record'))
    admin.add_view(EarlyClockView(name='今日早鳥', endpoint='early_clock'))
    # 介面中文化
    babel = Babel(app)
    @babel.localeselector
    def get_locale():
        return 'zh_Hant_TW'  # 繁體中文

    #註冊mysql API
    mysql_routes(api)
    #註冊swagger路由
    swaggerui_blueprint,SWAGGER_URL = create_swagger_ui()
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app