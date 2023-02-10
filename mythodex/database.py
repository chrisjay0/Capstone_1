from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect this database to Flask app."""
    db.app = app
    db.init_app(app)
