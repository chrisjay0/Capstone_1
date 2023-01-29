import os

from flask import Flask, render_template, session, g, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from flask_modals import Modal, render_template_modal
import random
from sqlalchemy.exc import IntegrityError

from database.models import db, connect_db

import requests

from magic_items.models import MagicItem 
from magic_items.services import shorten_description 
from lists.services import UserList, ItemUserList, add_list
from lists.forms import ListAddForm
from users.forms import UserAddForm, LoginForm, ListAddForm
from users.services import signup_user, User, authenticate_user

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
    form=ListAddForm()
    
    if form.validate_on_submit():
        try:
            new_list = add_list(
                name=form.name.data,
                description=form.description.data,
            )
            db.session.add(new_list)
            db.session.commit()

            
            flash('new list '+ new_list.name +' added','success')
            return render_template('home.html',response=rand_magic,desc=short_m_desc,list=test_list,form=form)
        except:
            flash('error','danger')
            return render_template('home.html',response=rand_magic,desc=short_m_desc,list=test_list,form=form)
            
    
    
    rand_magic_id = random.randrange(1,363)
    rand_magic = MagicItem.query.get(rand_magic_id)
    
    test_list = UserList.query.get(1)
    
    short_m_desc = shorten_description(rand_magic)
    
    
    
    return render_template_modal('home.html',response=rand_magic,desc=short_m_desc,list=test_list,form=form)


@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""

    return render_template('404.html'), 404


##############################################################################
# Signup / Login / Logout Routes


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

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
# List Routes


@app.route('/my-lists/add-list', methods=["GET", "POST"])
def add_new_list():

    if not g.user:
        flash("Please login to create a new list", "danger")
        return redirect("/login")
    
    form = ListAddForm()
    
    if form.validate_on_submit():
        try:
            new_list = UserList(
                name=form.name.data,
                desc=form.description.data,
                user_id=g.user.id,
            )
            
            db.session.add(new_list)
            db.session.commit()
            
            flash('new list '+ new_list.name +' added','success')
            return redirect('/')
        except:
            flash('error','danger')
            return render_template('lists/new_list.html',form=form)
        
    return render_template('lists/new_list.html',form=form)


@app.route('/my-lists/<int:list_id>/add-item/<int:item_id>', methods=["GET", "POST"])
def add_new_list_with_item(list_id, item_id):

    if not g.user:
        flash("Please login to create a new list", "danger")
        return redirect("/login")
    
    item_list_map = ItemUserList(
        item_id=item_id,
        list_id=list_id,
        times_on_list=1,
    )
    
    try:
        db.session.add(item_list_map)
        db.session.commit()
        flash('Item added to list!','success')
        return redirect('/')
        
    except:
        flash('Error prevented adding item to list','danger')
        return redirect('/')


@app.route('/my-lists', methods=["GET", "POST"])
def show_user_lists():

    if not g.user:
        flash("Please login to create a new list", "danger")
        return redirect("/login")
    
    
        
    return render_template('lists/user_lists.html',lists=lists)
    






