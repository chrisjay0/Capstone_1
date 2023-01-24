

import sys
sys.path.insert(0, '/the/folder/path/name-package/')


from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def connect_db(app):
    """Connect this database to Flask app."""

    db.app = app
    db.init_app(app)