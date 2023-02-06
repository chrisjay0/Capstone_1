import os

from flask import Flask, render_template, session, g, flash, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from flask_modals import Modal
import random
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from database.models import db, connect_db

import requests

from magic_items.models import MagicItem 
from magic_items.services import Collection, ItemCollection, add_collection, get_user_collections, get_collection, update_collection, get_magic_item, add_magic_item_to_list
from magic_items.forms import CollectionAddForm, ItemAddForm
from users.forms import UserAddForm, UserEditForm, LoginForm, ListAddForm
from users.services import signup_user, User, authenticate_user, UserServices

app = Flask(__name__)
modal = Modal(app)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///mythodex'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = 'SECRET'
toolbar = DebugToolbarExtension(app)

connect_db(app)

CURR_USER_KEY = "curr_user"


##############################################################################
# Homepage and error pages

@app.route('/', methods=["GET", "POST"])
def show_homepage():
    return render_template('home.html',
                           item = get_magic_item(random.randrange(1,363)),
                           )


@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""

    return render_template('404.html'), 404

##############################################################################
# Signup / Login / Logout Routes


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
        



@app.route('/signup', methods=["GET", "POST"])
def signup():

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = signup_user(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = authenticate_user(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""
    
    do_logout()
    return redirect('/')


##############################################################################
# User Routes

@app.route('/user/<int:user_id>')
def show_user(user_id):
    user = UserServices.get_by_id(user_id)
    return render_template('users/user.html',user=user)

@app.route('/user/edit', methods=["GET","POST"])
def edit_user():
    user_id = int(request.args['user_id'])

    if not g.user:
        flash("Please login to edit a profile.", "danger")
        return redirect("/login")
    
    if g.user.id != user_id:
        flash(f"{g.user.id} is not {user_id} Unauthorized to edit that profile.", "danger")
        return redirect(f"/user/{g.user.id}")
    
    user = UserServices.get_by_id(user_id)
    form = UserEditForm(obj=user)
    
    if not form.validate_on_submit():
        return render_template(f'/users/edit.html',form=form)
    
    try:
        user = UserServices.update(user.id, form)
        flash(f'Succesfully updated profile','success')
        return redirect(f"/user/{g.user.id}")
    except:
        flash(f'Unable to update profile','error')
        return render_template(f'/users/edit.html',form=form)

##############################################################################
# List Routes

@app.route('/collections/<int:collection_id>', methods=["GET"])
def show_collection(collection_id):
    
    item_collection = Collection.query.get_or_404(collection_id)
    return render_template('magic_items/collection.html',collection=item_collection)

@app.route('/collections/<int:collection_id>/edit', methods=["GET","POST"])
def edit_collection(collection_id):

    if not g.user:
        flash("Please login to manage collections.", "danger")
        return redirect("/login")
    
    collection_to_edit = get_collection(collection_id)

    if g.user.id != collection_to_edit.user_id:
        flash("Unauthorized to edit that collection", "danger")
        return redirect(f"/user/{g.user.id}/collections")
    
    form = CollectionAddForm(obj=collection_to_edit)
    
    if not form.validate_on_submit():
        return render_template("/magic_items/edit_collection.html",collection=collection_to_edit,form=form)
    
    if not update_collection(collection_to_edit.id, form):
        flash('Unable to update {collection_to_edit.name}','danger')
        return render_template("/magic_items/edit_collection.html",collection=collection_to_edit,form=form)

    flash(f'Succesfully updated {collection_to_edit.name}!','success')
    return redirect(f'/collections/{collection_to_edit.id}')
    
@app.route('/my-collections/add-collection', methods=["GET", "POST"])
def add_new_collection():

    if not g.user:
        flash("Please login to create a new collection", "danger")
        return redirect("/login")
    
    form = CollectionAddForm()
    
    if form.validate_on_submit():
        try:
            new_collection = Collection(
                name=form.name.data,
                description=form.description.data,
                user_id=g.user.id,
            )
            
            db.session.add(new_collection)
            db.session.commit()
            
            flash('new collection '+ new_collection.name +' added','success')
            return redirect('/')
        except:
            flash('error','danger')
            return render_template('magic_items/new_collection.html',form=form)
        
    return render_template('magic_items/new_collection.html',form=form)


@app.route('/my-collections/<int:collection_id>/add-item/<int:item_id>', methods=["POST"])
def add_new_collection_with_item(collection_id, item_id):

    if not g.user:
        flash("Please login to create a new collection", "danger")
        return redirect("/login")
    
    magic_item = get_magic_item(item_id)
    collection = get_collection(collection_id)
    
    if not add_magic_item_to_list(magic_item,collection):
        
        flash('Error prevented adding item to collection','danger')
        return redirect('/')
    
    flash('Item added to collection!','success')
    return redirect(f'/collections/{collection_id}')


@app.route('/user/<int:user_id>/collections', methods=["GET"])
def show_user_collections(user_id):
    
    collections = get_user_collections(user_id)
        
    return render_template('magic_items/collections.html',collections=collections)


@app.route('/user/<int:user_id>/collections/<int:collection_id>/delete', methods=["POST"])
def delete_collection(user_id,collection_id):

    if not g.user:
        flash("Please login to manage collections.", "danger")
        return redirect("/login")

    if g.user.id != user_id:
        flash("Please login to manage collections.", "danger")
        return redirect(f"/user/{g.user.id}/collections")

    user_collection = Collection.query.get(collection_id)
    db.session.delete(user_collection)
    db.session.commit()

    return redirect(f"/user/{g.user.id}/collections")


##############################################################################
# Magic Item Routes

@app.route('/magic-items/<int:item_id>', methods=["GET"])
def show_item(item_id):
    
    item = MagicItem.query.get_or_404(item_id)
    return render_template('magic_items/magic_item.html',item=item)
    






