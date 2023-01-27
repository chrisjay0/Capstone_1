from app import db
import time

from lists.models import ItemUserList, UserList
from users.models import User
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

item = MagicItem(
        name = 'test item',
        item_type = 'armor',
        rarity = 'common',
        description = 'test desc',
        source='test',)

db.session.add(item)
db.session.commit()

u_list = UserList(
        name = 'test list',
        user_id = 1,
        desc = 'test desc',)

db.session.add(u_list)
db.session.commit()

item_for_list = ItemUserList(
        item_id=1,
        list_id=1,
        times_on_list=1,)

db.session.add(item_for_list)
db.session.commit()

res = requests.get("https://www.dnd5eapi.co/api/magic-items/adamantine-armor/").json()

DND_API_URL = 'https://www.dnd5eapi.co/api/magic-items/'

res = requests.get(DND_API_URL).json()

for result in res.get('results'):
    item_res = requests.get(DND_API_URL + result.get('index')).json()
    
    if len(item_res.get('variants')) == 0:
        has_variants = False
    else:
        has_variants = True
        for variant in item_res.get('variants'):
            new_variant = ItemVariant(
                original_item_name = item_res.get('name'),
                variant_item_name = variant.get('name'),
            )
            db.session.add(new_variant)
            db.session.commit()
            
    
    item = MagicItem(
        name = item_res.get('name'),
        item_type = item_res.get('equipment_category').get('name'),
        rarity = item_res.get('rarity').get('name'),
        has_variants = has_variants,
        is_variant = item_res.get('variant'),
        description = item_res.get('desc')[1],
        source='dnd5eapi',
        )
    
    db.session.add(item)
    db.session.commit()
    time.sleep(.5)