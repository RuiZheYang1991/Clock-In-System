from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash
from ..mysql.models.user import User  # 替換成你的 User 模型的實際導入路徑
from ..form.admin.login_form import LoginForm

#
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'
auth = Blueprint('auth', __name__)




@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin.index'))

    return render_template('login.html', form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.index'))


@auth.route("/register", methods=["GET", "POST"])
def register():
    from .. import db
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if User.query.filter_by(email=email).first():
            flash("Email already exists")
            return redirect(url_for("register"))

        new_user = User(email=email, password_hash=generate_password_hash(password, method="sha256"))
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for("index"))

    return render_template("register.html")
