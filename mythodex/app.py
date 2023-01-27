import os

from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
import random

from database.models import db, connect_db

import requests

from magic_items.models import MagicItem 
from lists.models import UserList, ItemUserList 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///mythodex'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = 'SECRET'
toolbar = DebugToolbarExtension(app)

connect_db(app)


##############################################################################
# Homepage and error pages


@app.route('/')
def show_homepage():
    
    
    rand_magic_id = random.randrange(1,363)
    rand_magic = MagicItem.query.get(rand_magic_id)
    
    test_list = UserList.query.get(1)
    
    
    
    
    
    res = requests.get("https://www.dnd5eapi.co/api/magic-items/adamantine-armor/").json()
    
    
    
    return render_template('home.html',response=rand_magic,list=test_list)


@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""

    return render_template('404.html'), 404
