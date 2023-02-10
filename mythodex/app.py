import os

from flask import Flask, render_template, session, g, flash, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from flask_modals import Modal
import random
from sqlalchemy.exc import IntegrityError

from magic_items.routes import magic_routes
from users.routes import user_routes


from database import connect_db

from magic_items.services import (
    CollectionService,
    MagicItemService,
    ItemCollectionService,
)

from magic_items.forms import CollectionAddForm, ItemFilterForm
from users.forms import UserAddForm, UserEditForm, LoginForm, ListAddForm
from users.services import signup_user, User, authenticate_user, UserService

app = Flask(__name__)
modal = Modal(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///mythodex"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["SECRET_KEY"] = "SECRET"

app.register_blueprint(user_routes)
app.register_blueprint(magic_routes)

toolbar = DebugToolbarExtension(app)

connect_db(app)

CURR_USER_KEY = 'curr user'




##############################################################################
# Homepage and error pages


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


##############################################################################
# Login / Logout Routes


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


# ##############################################################################
# # User Routes


# @app.route("/signup", methods=["GET", "POST"])
# def signup():

#     form = UserAddForm()

#     if form.validate_on_submit():
#         try:
#             user = UserService.create(form)

#             do_login(user)

#             flash(f"Welcome to Mythodex {user.username}", "success")
#             return redirect(f"/users/{user.id}")

#         except IntegrityError:
#             flash("Username already taken", "danger")
#             return render_template("users/signup.html", form=form)

#     return render_template("users/signup.html", form=form)


# @app.route("/users/<int:user_id>")
# def show_user(user_id):
#     user = UserService.get_by_id(user_id)
#     return render_template("users/user.html", user=user)


# @app.route("/users/edit", methods=["GET", "POST"])
# def edit_user():
#     user_id = int(request.args["user_id"])

#     if not g.user:
#         flash("Please login to edit a profile.", "danger")
#         return redirect("/login")

#     if g.user.id != user_id:
#         flash(
#             f"{g.user.id} is not {user_id} Unauthorized to edit that profile.", "danger"
#         )
#         return redirect(f"/users/{g.user.id}")

#     user = UserService.get_by_id(user_id)
#     form = UserEditForm(obj=user)

#     if not form.validate_on_submit():
#         return render_template(f"/users/edit.html", user=user, form=form)

#     try:
#         user = UserService.update(user.id, form)
#         flash(f"Succesfully updated profile", "success")
#         return redirect(f"/users/{g.user.id}")
#     except:
#         flash(f"Unable to update profile", "error")
#         return render_template(f"/users/edit.html", user=user, form=form)


# @app.route("/users/delete", methods=["POST"])
# def delete_user():

#     if not g.user:
#         flash("Please login to edit a profile.", "danger")
#         return redirect("/login")

#     user_id = int(request.args["user_id"])
#     form = UserEditForm()

#     if g.user.id != user_id:
#         flash(
#             f"{g.user.id} is not {user_id} Unauthorized to edit that profile.", "danger"
#         )
#         return redirect(f"/users/{g.user.id}")

#     if not form.validate_on_submit():
#         return redirect(f"/users/edit?user_id={g.user.id}")

#     try:
#         UserService.delete(user_id, form)
#         flash(f"Your profile has been removed", "success")
#         return redirect("/")
#     except:
#         flash(f"Unable to update profile", "error")
#         return render_template(f"/users/edit.html", form=form)