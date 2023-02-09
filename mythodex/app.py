import os

from flask import Flask, render_template, session, g, flash, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from flask_modals import Modal
import random
from sqlalchemy.exc import IntegrityError

from database import connect_db

from magic_items.services import (
    CollectionService,
    MagicItemService,
    ItemCollectionService,
)

from magic_items.forms import CollectionAddForm, ItemForm, ItemFilterForm
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
toolbar = DebugToolbarExtension(app)

connect_db(app)

CURR_USER_KEY = "curr_user"


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


##############################################################################
# User Routes


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


@app.route("/users/<int:user_id>")
def show_user(user_id):
    user = UserService.get_by_id(user_id)
    return render_template("users/user.html", user=user)


@app.route("/users/edit", methods=["GET", "POST"])
def edit_user():
    user_id = int(request.args["user_id"])

    if not g.user:
        flash("Please login to edit a profile.", "danger")
        return redirect("/login")

    if g.user.id != user_id:
        flash(
            f"{g.user.id} is not {user_id} Unauthorized to edit that profile.", "danger"
        )
        return redirect(f"/users/{g.user.id}")

    user = UserService.get_by_id(user_id)
    form = UserEditForm(obj=user)

    if not form.validate_on_submit():
        return render_template(f"/users/edit.html", user=user, form=form)

    try:
        user = UserService.update(user.id, form)
        flash(f"Succesfully updated profile", "success")
        return redirect(f"/users/{g.user.id}")
    except:
        flash(f"Unable to update profile", "error")
        return render_template(f"/users/edit.html", user=user, form=form)


@app.route("/users/delete", methods=["POST"])
def delete_user():

    if not g.user:
        flash("Please login to edit a profile.", "danger")
        return redirect("/login")

    user_id = int(request.args["user_id"])
    form = UserEditForm()

    if g.user.id != user_id:
        flash(
            f"{g.user.id} is not {user_id} Unauthorized to edit that profile.", "danger"
        )
        return redirect(f"/users/{g.user.id}")

    if not form.validate_on_submit():
        return redirect(f"/users/edit?user_id={g.user.id}")

    try:
        UserService.delete(user_id, form)
        flash(f"Your profile has been removed", "success")
        return redirect("/")
    except:
        flash(f"Unable to update profile", "error")
        return render_template(f"/users/edit.html", form=form)


##############################################################################
# Collection Routes


@app.route("/collections/new", methods=["GET", "POST"])
def add_new_collection():

    if not g.user:
        flash("Please login to create a new collection", "danger")
        return redirect("/login")

    form = CollectionAddForm()

    if form.validate_on_submit():
        if not request.args:
            try:
                collection = CollectionService.create(g.user.id, form)
                flash("new collection " + collection.name + " added", "success")
                return redirect(f"/collections/{collection.id}")

            except:
                flash("error", "danger")
                return render_template("magic_items/new_collection.html", form=form)
        else:
            try:
                magic_item_id = int(request.args["magic_item_id"])
                collection = CollectionService.create(g.user.id, form)
                CollectionService.add_magic_item(magic_item_id, collection.id)
                flash(f"new collection {collection.name} created", "success")
                return redirect(f"/collections/{collection.id}")

            except:
                flash("error", "danger")
                return render_template("magic_items/new_collection.html", form=form)

    return render_template("magic_items/new_collection.html", form=form)


@app.route("/collections", methods=["GET"])
def show_collections():

    if request.args and request.args["user_id"] == "":
        flash("Please login or signup to manage your collections", "danger")
        return redirect("/login")

    collections = CollectionService.get_filtered(**request.args)
    return render_template(
        "magic_items/collections.html",
        collections=collections,
    )


@app.route("/collections/<int:collection_id>", methods=["GET"])
def show_single_collection(collection_id):
    collection = CollectionService.get(collection_id)
    inventory = ItemCollectionService.get_inventory_numbers(collection.id)
    return render_template(
        "magic_items/collection.html", collection=collection, inventory=inventory
    )


@app.route("/collections/edit", methods=["GET", "POST"])
def edit_collection():

    if not g.user:
        flash("Please login to manage collections.", "danger")
        return redirect("/login")

    collection_id = int(request.args["collection_id"])
    collection = CollectionService.get(collection_id)
    form = CollectionAddForm(obj=collection)

    if g.user.id != collection.user_id:
        flash("Unauthorized to edit that collection", "danger")
        return redirect(f"/collections?user_id={g.user.id}")

    if not form.validate_on_submit():
        return render_template(
            "/magic_items/edit_collection.html", collection=collection, form=form
        )

    try:
        collection = CollectionService.update(g.user.id,collection_id, form)
        flash(f"Succesfully updated {collection.name}!", "success")
        return redirect(f"/collections/{collection.id}")

    except:
        flash("Unable to update {collection.name}", "danger")
        return render_template(
            "/magic_items/edit_collection.html", collection=collection, form=form
        )


@app.route("/collections/add-item", methods=["POST"])
def add_item_to_collection():

    if not g.user:
        flash("Please login to manage your collections", "danger")
        return redirect("/login")

    magic_item_id = int(request.args["magic_item_id"])
    collection_id = int(request.args["collection_id"])

    CollectionService.add_magic_item(magic_item_id, collection_id)

    return redirect(f"/collections/{collection_id}")


@app.route("/collections/reduce-item", methods=["POST"])
def reduce_item_in_collection():

    if not g.user:
        flash("Please login to manage your collections", "danger")
        return redirect("/login")

    magic_item_id = int(request.args["magic_item_id"])
    collection_id = int(request.args["collection_id"])

    CollectionService.reduce_magic_item(magic_item_id, collection_id)

    return redirect(f"/collections/{collection_id}")


@app.route("/collections/remove-item", methods=["POST"])
def remove_item_in_collection():

    if not g.user:
        flash("Please login to manage your collections", "danger")
        return redirect("/login")

    magic_item_id = int(request.args["magic_item_id"])
    collection_id = int(request.args["collection_id"])

    CollectionService.remove_magic_item(magic_item_id, collection_id)

    return redirect(f"/collections/{collection_id}")


@app.route("/collections/delete", methods=["POST"])
def delete_collection():

    if not g.user:
        flash("Please login to manage your collections", "danger")
        return redirect("/login")

    collection_id = int(request.args["collection_id"])
    collection = CollectionService.get(collection_id)

    if g.user.id is not collection.user_id:
        flash("Not authorized to make changes to that collection", "danger")
        return redirect(f"/collections?user_id={g.user.id}")

    CollectionService.delete(collection_id, g.user.id)
    return redirect(f"/collections?user_id={g.user.id}")


@app.route("/collections/random", methods=["GET"])
def random_collection():

    collection = CollectionService.random()
    inventory = ItemCollectionService.get_inventory_numbers(collection.id)
    return render_template(
        "magic_items/collection.html", collection=collection, inventory=inventory
    )


@app.route("/collections/random-item", methods=["GET"])
def random_item_in_collection():
    
    collection_id = int(request.args['collection_id'])
    
    item = CollectionService.random_item(collection_id)

    return render_template("magic_items/magic_item.html",item=item)


##############################################################################
# Magic Item Routes


@app.route("/magic-items/new", methods=["GET", "POST"])
def add_item():

    if not g.user:
        flash("Please login to create a new magic item", "danger")
        return redirect("/login")

    form = ItemForm()

    if form.validate_on_submit():
        try:
            item = MagicItemService.create(g.user.id, form)
            flash("new item " + item.name + " added", "success")
            return redirect(f"/magic-items/{item.id}")

        except:
            flash("error", "danger")
            return render_template("magic_items/new_magic_item.html", form=form)

    return render_template("magic_items/new_magic_item.html", form=form)


@app.route("/magic-items/<int:item_id>", methods=["GET"])
def show_item(item_id):
    item = MagicItemService.get(item_id)
    if item.created_by:
        user = UserService.get_by_id(item.created_by)
        return render_template("magic_items/magic_item.html", item=item, user=user,)
    return render_template("magic_items/magic_item.html", item=item,)


@app.route("/magic-items", methods=["GET"])
def show_items():
    form = ItemFilterForm(object=request.args)

    if 'created_by' in request.args and request.args['created_by'] == '':
        flash("Please login or signup to your magic items", "danger")
        return redirect("/login")
    
    
    items = MagicItemService.get_filtered(**request.args)
        

    return render_template(
        "magic_items/magic_items.html",
        items=items,
        form=form,
    )


@app.route("/magic-items/edit", methods=["GET", "POST"])
def edit_item():

    if not g.user:
        flash("Please login to create a new magic item", "danger")
        return redirect("/login")

    magic_item_id = int(request.args["magic_item_id"])
    item = MagicItemService.get(magic_item_id)
    item.description = item.description[1]
    form = ItemForm(obj=item)

    if form.validate_on_submit():
        try:
            edited_item = MagicItemService.update(g.user.id,magic_item_id,form)
            flash("new item " + edited_item.name + " edited", "success")
            return redirect(f"/magic-items/{edited_item.id}")

        except:
            flash("error", "danger")
            return render_template("magic_items/edit_magic_item.html", form=form, item=item)

    return render_template("magic_items/edit_magic_item.html", form=form, item=item)


@app.route("/magic-items/delete", methods=["POST"])
def delete_item():

    if not g.user:
        flash("Please login to manage magic items", "danger")
        return redirect("/login")

    magic_item_id = int(request.args["magic_item_id"])
    item = MagicItemService.get(magic_item_id)

    if g.user.id is not item.created_by:
        flash("Not authorized to make changes to that magic item", "danger")
        return redirect(f"/magic-items?created_by={g.user.id}")

    MagicItemService.delete(g.user.id, magic_item_id)
    flash(f'{item.name} has been deleted','success')
    return redirect(f"/magic-items?created_by={g.user.id}")

@app.route("/magic-items/random", methods=["GET"])
def random_item():
    item = MagicItemService.random()
    return render_template("magic_items/magic_item.html", item=item)
