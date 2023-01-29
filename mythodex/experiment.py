from app import db
import time

from lists.models import ItemUserList, UserList
from users.models import User
from magic_items.models import MagicItem, ItemVariant

import requests

new_list = UserList(
    name='test',
    desc='nin',
    user_id=1,
)

db.session.add(new_list)
db.session.commit()