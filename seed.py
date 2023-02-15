import time, requests
from app import create_app

app = create_app()
app.app_context().push()

from users.models import User
from magic_items.models import MagicItem, ItemVariant, ItemCollection, Collection
from database import db

db.drop_all()
db.create_all()

user = User(username="test", email="test@test.com", bio="test bio", password="pass")

db.session.add(user)
db.session.commit()

item = MagicItem(
    name="test item",
    item_type="Armor",
    rarity="Common",
    description="test desc",
    source="test",
)

db.session.add(item)
db.session.commit()

u_collection = Collection(
    name="test collection",
    user_id=1,
    description="test desc",
)

db.session.add(u_collection)
db.session.commit()

item_for_collection = ItemCollection(
    item_id=1,
    collection_id=1,
)

db.session.add(item_for_collection)
db.session.commit()

res = requests.get("https://www.dnd5eapi.co/api/magic-items/adamantine-armor/").json()

DND_API_URL = "https://www.dnd5eapi.co/api/magic-items/"

variant_indexing_collection = []

res = requests.get(DND_API_URL).json()


for result in res.get("results"):
    item_res = requests.get(DND_API_URL + result.get("index")).json()

    if len(item_res.get("variants")) == 0:
        variants = []
    else:
        for variant in item_res.get("variants"):
            new_variant_index = [item_res.get("name"), variant.get("name")]
            variant_indexing_collection.append(new_variant_index)

    item_description = []
    for description_line in item_res.get("desc"):
        item_description.append(description_line)

    item = MagicItem(
        name=item_res.get("name"),
        item_type=item_res.get("equipment_category").get("name"),
        rarity=item_res.get("rarity").get("name"),
        is_variant=item_res.get("variant"),
        description=item_description,
        source="dnd5eapi",
    )

    db.session.add(item)
    db.session.commit()
    time.sleep(0.5)


for variant_index in variant_indexing_collection:

    original_id = int(MagicItem.query.filter_by(name=variant_index[0]).first().id)
    variant_id = int(MagicItem.query.filter_by(name=variant_index[1]).first().id)

    variant_map = ItemVariant(
        original_item_id=original_id,
        variant_item_id=variant_id,
    )

    db.session.add(variant_map)
    db.session.commit()
