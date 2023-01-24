import os

from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension

from database.models import db, connect_db

import requests

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
    res = requests.get("https://www.dnd5eapi.co/api/magic-items/adamantine-armor/").json()
    
    
    
    return render_template('home.html',response=res)


@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""

    return render_template('404.html'), 404
