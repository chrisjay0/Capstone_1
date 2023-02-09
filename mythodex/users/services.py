from users.models import User, User as UserModel
from users.domains import User as UserDomain
from users.forms import UserEditForm, UserAddForm
from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from database import db

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

#######################################
# domain based services

class UserService:
    
    @classmethod
    def create(cls,
               form: UserAddForm,
               ) -> UserDomain:
        
        password = form.password.data
        
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user_model = UserModel(
            username=form.username.data,
            email=form.email.data,
            password=hashed_pwd,
            image_url=form.image_url.data,
        )
        
        db.session.add(user_model)
        db.session.commit()
        
        return UserDomain.from_model(user_model)
    
    @classmethod
    def get_by_username(cls, username: str) -> 'UserDomain':
        user_model = UserModel.query.filter_by(username=username).first()
        return UserDomain.from_model(user_model)
    
    @classmethod
    def get_by_id(cls, user_id: int) -> 'UserDomain':
        user_model = UserModel.query.get_or_404(user_id)
        return UserDomain.from_model(user_model)
    
    @classmethod
    def update(cls, user_id: int,
                    form: UserEditForm,
                    ) -> UserDomain:

        user_model = UserModel.query.get_or_404(user_id)
        password = form.password.data
        is_authorized = bcrypt.check_password_hash(
            user_model.password, 
            password)

        if user_model and is_authorized:
            user_model.username = form.username.data
            user_model.email = form.email.data
            user_model.image_url = form.image_url.data
            user_model.bio = form.bio.data
            user_model.last_updated = datetime.utcnow()
            
            db.session.commit()
            
            return UserDomain.from_model(user_model)
        
        return False
    
    @classmethod
    def delete(cls,
               user_id: int,
               form: UserEditForm,
               ) -> bool:

        user_model = UserModel.query.get_or_404(user_id)
        
        password = form.password.data
        
        is_authorized = bcrypt.check_password_hash(
            user_model.password, 
            password)
        
        if is_authorized:
            db.session.delete(user_model)
            db.session.commit()
            return True