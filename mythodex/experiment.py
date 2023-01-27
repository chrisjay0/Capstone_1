from app import db
import time

from lists.models import ItemUserList, UserList
from users.models import User
from magic_items.models import MagicItem, ItemVariant

import requests

new_item_for_list = ItemUserList(
    item_id = 58,
    list_id = 1,
    times_on_list = 1,
)

db.session.add(new_item_for_list)
db.session.commit()