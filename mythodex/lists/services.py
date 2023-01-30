from lists.models import UserList, ItemUserList
from datetime import datetime
from database.models import db

def add_list(name, description):

    new_list = UserList(
        name=name,
        description=description,
    )
    return new_list

def get_user_lists(user_id:int):
    user_lists = UserList.query.filter_by(user_id=user_id).all()
    return user_lists

def get_list(list_id:int):
    requested_list = UserList.query.get_or_404(list_id)
    return requested_list

def update_list(list_id:int, form):
    
    udate_list = UserList.query.get_or_404(list_id)
    
    try:
        udate_list.name = form.name.data
        udate_list.description = form.description.data
        udate_list.date_last_updated = datetime.utcnow()
        
        db.session.commit()
        return True
        
    except:
        
        return False
        
    
    

