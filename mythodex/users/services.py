from users.models import User
from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from database.models import db

bcrypt = Bcrypt()

def authenticate_user(username, password):

        user = User.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False
    
        
def signup_user(username, email, password, image_url):

    hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

    user = User(
        username=username,
        email=email,
        password=hashed_pwd,
        image_url=image_url,
    )

    db.session.add(user)
    return user


def edit_user(username, email, image_url, header_image_url, bio, password):

    hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

    user = User(
        username=username,
        email=email,
        image_url=image_url,
        header_image_url=header_image_url,
        bio=bio,
        password=hashed_pwd,
        date_last_updated=datetime.utcnow(),
    )
    
    return user