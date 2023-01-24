from app import db
import time

from lists.models import ItemUserList, UserList
from users.models import User, ItemLikes
from magic_items.models import MagicItem, ItemVariant

import requests

db.drop_all()
db.create_all()

user = User(username='test',
            email='test@test.com',
            bio='test bio',
            password='pass')

db.session.add(user)
db.session.commit()

res = requests.get("https://www.dnd5eapi.co/api/magic-items/adamantine-armor/").json()

DND_API_URL = 'https://www.dnd5eapi.co/api/magic-items/'

res = requests.get(DND_API_URL).json()

for result in res.get('results'):
    item_res = requests.get(DND_API_URL + result.get('index')).json()
    item = MagicItem(
        name = item_res.get('name'),
        item_type = item_res.get('equipment_category').get('name'),
        rarity = item_res.get('rarity').get('name'),
        description = item_res.get('desc')[1],
        source='dnd5eapi',
        )
    db.session.add(item)
    db.session.commit()
    time.sleep(.5)
    
    
    
    

# item = MagicItem(
#     name = res.get('name'),
#     item_type = res.get('equipment_category').get('name'),
#     rarity = res.get('rarity').get('name'),
#     description = res.get('desc')[1],
#     source='dnd5eapi',
#     )

# db.session.add(item)