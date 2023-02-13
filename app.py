import os

from flask import Flask, render_template, session, g, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
import random
from sqlalchemy.exc import IntegrityError
from flask_modals import Modal

from magic_items.routes import magic_routes
from users.routes import user_routes


from database import connect_db

from magic_items.services import MagicItemService

from users.forms import UserAddForm, LoginForm
from users.services import User, authenticate_user, UserService

app = Flask(__name__)
modal = Modal(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    'DATABASE_URL', 'postgresql:///mythodex')

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY','secret5231')
print('*************************************')
print('*************************************')
print('*************************************')
print(app.config["SECRET_KEY"])
print('*************************************')
print('*************************************')
print('*************************************')

app.register_blueprint(user_routes)
app.register_blueprint(magic_routes)

toolbar = DebugToolbarExtension(app)

connect_db(app)

CURR_USER_KEY = "curr user"


#########################################################################################################
#########################################################################################################
##
## Homepage and error pages


@app.route("/", methods=["GET", "POST"])
def show_homepage():
    return render_template(
        "home.html",
        item=MagicItemService.get(random.randrange(1, 363)),
    )


@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""

    return render_template("404.html"), 404


@app.errorhandler(403)
def page_not_autherized(e):
    """403 NOT auth page."""

    return render_template("403.html"), 403


@app.errorhandler(405)
def page_not_autherized(e):
    """405 method not allowed."""

    return render_template("405.html"), 405


#########################################################################################################
#########################################################################################################
##
## Login / Logout Routes


@app.before_request
def add_user_to_g():
    """If logged in, add current user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None


def do_login(user):
    session[CURR_USER_KEY] = user.id


def do_logout():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = authenticate_user(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", "danger")

    return render_template("users/login.html", form=form)


@app.route("/logout")
def logout():
    """Handle logout of user."""

    do_logout()
    return redirect("/")


@app.route("/signup", methods=["GET", "POST"])
def signup():

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = UserService.create(form)

            do_login(user)

            flash(f"Welcome to Mythodex {user.username}", "success")
            return redirect(f"/users/{user.id}")

        except IntegrityError:
            flash("Username already taken", "danger")
            return render_template("users/signup.html", form=form)

    return render_template("users/signup.html", form=form)
