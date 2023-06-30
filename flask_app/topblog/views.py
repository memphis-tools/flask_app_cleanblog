from flask import Flask, flash, abort, request, url_for, redirect, render_template
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from flask_wtf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
from colorama import Fore, Style
from flask_app.topblog.models import db, User
from .forms import ContactForm, LoginForm, SigninForm


app = Flask(__name__)
app.config.from_pyfile('settings.py')

# Doc: https://python-adv-web-apps.readthedocs.io/en/latest/flask_forms.html
# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)
ckeditor = CKEditor(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# login_manager configuration
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
@app.route("/home/")
@app.route("/index/")
def index():
    return render_template("index.html", logged_in=current_user.is_authenticated)


@app.route("/post/")
@login_required
def posts():
    return render_template("posts.html", logged_in=current_user.is_authenticated)


@app.route("/contact/", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    today = datetime.today()
    if request.method == "POST":
        if form.validate_on_submit():
            print(f"{Fore.GREEN}[DEBUG - MAIL]\n \
                    Received from {form.name.data} \
                    on {today.strftime('%d-%m-%y %h%M')}:\n \
                    {form.message.data}{Style.RESET_ALL}")
            flash("Mail sent sir !")
            return redirect(url_for('index'))
        else:
            flash("Check input sir !")
    return render_template("contact.html", form=form, logged_in=current_user.is_authenticated)


@app.route("/about/")
def about():
    return render_template("about.html", logged_in=current_user.is_authenticated)


@app.route("/signin", methods=["GET", "POST"])
def signin():
    form = SigninForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                flash("User already exists with this email")
                return redirect(url_for("signin"))
            else:
                hashed_and_salted = generate_password_hash(form.password.data, "pbkdf2:sha256", salt_length=8)
                new_user = User(username=form.username.data, email=form.email.data, password=hashed_and_salted)

                flash("Informative message")
                db.session.add(new_user)
                db.session.commit()

    return render_template("signin.html", form=form, logged_in=current_user.is_authenticated)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            password = form.password.data
            if not user:
                flash("User does not exist")
                return render_template("login.html", form=form, logged_in=current_user.is_authenticated)
            elif not check_password_hash(user.password, password):
                flash("(Dummy message) Incorrect password")
                return render_template("login.html", form=form, logged_in=current_user.is_authenticated)
            else:
                login_user(user)
                flash("Welcome back sir !")
                return render_template("index.html",
                                       logged_in=current_user.is_authenticated,
                                       not_critical="not_critical")

    return render_template("login.html", form=form, logged_in=current_user.is_authenticated)


@app.route("/logout")
def logout():
    logout_user()
    return render_template("index.html", logged_in=current_user.is_authenticated)


if __name__ == "__main__":
    app.run(debug=True)
