from flask import Flask, flash, abort, request, url_for, redirect, render_template
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from flask_wtf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
from colorama import Fore, Style
from sqlalchemy import desc

from . import settings
from flask_app.topblog.models import db, UserModel, PostModel
from .forms import LoginForm, SigninForm, PostAddForm, PostDeleteForm, PostUpdateForm, \
    ContactForm
from .exceptions import UsersDoesNotExist


app = Flask(__name__)
app.config.from_pyfile('settings.py')

POST_PAGINATOR_MAX = settings.POST_PAGINATOR_MAX

# Doc: https://python-adv-web-apps.readthedocs.io/en/latest/flask_forms.html
# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)
ckeditor = CKEditor()
ckeditor.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(user_id)


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
    posts = PostModel.query.order_by(desc(PostModel.id)).limit(POST_PAGINATOR_MAX).all()
    try:
        users = UserModel.query.all()
    except UsersDoesNotExist:
        users = []

    return render_template("index.html",
                           posts=posts,
                           users=users,
                           POST_PAGINATOR_MAX=POST_PAGINATOR_MAX,
                           logged_in=current_user.is_authenticated)


@app.route("/post/<int:post_id>/")
@login_required
def post(post_id):
    requested_post = PostModel.query.get(post_id)
    post_author = UserModel.query.get(requested_post.author_id)
    return render_template("post.html",
                           post=requested_post,
                           post_author=post_author,
                           logged_in=current_user.is_authenticated)


@app.route("/post/add/", methods=["GET", "POST"])
@login_required
def post_add():
    if current_user.id == 1:
        flash("You can not add any post as the admin Sir")
        return redirect(url_for("index",
                                POST_PAGINATOR_MAX=POST_PAGINATOR_MAX,
                                logged_in=current_user.is_authenticated))
    form = PostAddForm()
    today = datetime.today()
    if request.method == "POST":
        if form.validate_on_submit():
            new_post = PostModel(
                title=form.title.data,
                subtitle=form.subtitle.data,
                description=form.description.data,
                author_id=current_user.id,
                img_url=form.img_url.data,
                created_time=today.strftime("%B %d, %Y"),
                updated_time=today.strftime("%B %d, %Y")
            )
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for("index",
                                    POST_PAGINATOR_MAX=POST_PAGINATOR_MAX,
                                    logged_in=current_user.is_authenticated))

    return render_template("post_add.html", form=form, logged_in=current_user.is_authenticated)


@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def post_update(post_id):
    post_to_update = PostModel.query.get(post_id)
    form = PostUpdateForm(
        title=post_to_update.title,
        subtitle=post_to_update.subtitle,
        description=post_to_update.description,
        author_id=current_user.id,
        img_url=post_to_update.img_url,
    )
    today = datetime.today()
    if request.method == "POST":
        if form.validate_on_submit():
            post_to_update.title = form.title.data
            post_to_update.subtitle = form.subtitle.data
            post_to_update.img_url = form.img_url.data
            post_to_update.description = form.description.data
            post_to_update.updated_time = today.strftime("%B %d, %Y")
            db.session.commit()
            return redirect(url_for("index",
                                    POST_PAGINATOR_MAX=POST_PAGINATOR_MAX,
                                    logged_in=current_user.is_authenticated))
    return render_template("post_update.html", form=form, logged_in=current_user.is_authenticated)


@app.route("/post/<int:post_id>/delete", methods=["GET", "POST"])
@login_required
@admin_only
def post_delete(post_id):
    form = PostDeleteForm()
    if request.method == "POST":
        if form.decision.data:
            post_to_delete = PostModel.query.get(post_id)
            db.session.delete(post_to_delete)
            db.session.commit()

        return redirect(url_for("index",
                                POST_PAGINATOR_MAX=POST_PAGINATOR_MAX,
                                logged_in=current_user.is_authenticated))
    return render_template("post_delete.html", form=form, logged_in=current_user.is_authenticated)


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
            return redirect(url_for("index",
                                    POST_PAGINATOR_MAX=POST_PAGINATOR_MAX,
                                    logged_in=current_user.is_authenticated))
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
            user = UserModel.query.filter_by(email=form.email.data).first()
            if user:
                flash("User already exists with this email")
                return redirect(url_for("signin"))
            else:
                hashed_and_salted = generate_password_hash(form.password.data, "pbkdf2:sha256", salt_length=8)
                new_user = UserModel(username=form.username.data, email=form.email.data, password=hashed_and_salted)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login'))

    return render_template("signin.html", form=form, logged_in=current_user.is_authenticated)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = UserModel.query.filter_by(email=form.email.data).first()
            password = form.password.data
            if not user:
                flash("User does not exist")
                return render_template("login.html", form=form, logged_in=current_user.is_authenticated)
            elif not check_password_hash(user.password, password):
                flash("(Dummy message) Incorrect password")
                return render_template("login.html", form=form, logged_in=current_user.is_authenticated)
            else:
                login_user(user)
                return redirect(url_for("index",
                                        POST_PAGINATOR_MAX=POST_PAGINATOR_MAX,
                                        logged_in=current_user.is_authenticated))

    return render_template("login.html", form=form, logged_in=current_user.is_authenticated)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index",
                            POST_PAGINATOR_MAX=POST_PAGINATOR_MAX,
                            logged_in=current_user.is_authenticated))


if __name__ == "__main__":
    app.run(debug=True)
