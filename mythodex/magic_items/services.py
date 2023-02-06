from magic_items.models import Collection, ItemCollection , MagicItem
from datetime import datetime
from database.models import db

import magic_items.domains as domain
import magic_items.models as model


ITEM_RARITY  = ['Common','Uncommon','Rare','Very Rare']
ITEM_TYPES = ['Scroll','Rod','Armor','Ammunition','Ring','Potion','Staff','Wondrous Items','Wand','Weapon',]

def add_collection(name, description):

    new_collection = Collection(
        name=name,
        description=description,
    )
    return new_collection

def get_user_collections(user_id:int):
    user_collections = Collection.query.filter_by(user_id=user_id).all()
    return user_collections

# def get_collection(collection_id:int):
#     requested_collection = Collection.query.get_or_404(collection_id)
#     return requested_collection

def update_collection(collection_id:int, form):
    
    udate_collection = Collection.query.get_or_404(collection_id)
    
    try:
        udate_collection.name = form.name.data
        udate_collection.description = form.description.data
        udate_collection.date_last_updated = datetime.utcnow()
        
        db.session.commit()
        return True
        
    except:
        
        return False


#######################
## New services using domain classes

def get_magic_item(magic_item_id: int) -> domain.MagicItem:
    """Accepts an integer as a magic item ID and returns a magic item domain object.

    Args:
        magic_item_id (int): an ID of a magic item in the database

    Returns:
        dmMagicItem: a domain object representing the magic item
    """
    
    model_magic_item = model.MagicItem.query.get_or_404(magic_item_id)
    
    return domain.MagicItem.from_model(model_magic_item)

def get_collection(collection_item_id: int) -> domain.Collection:
    """Accepts an integer as a magic item ID and returns a magic item domain object.

    Args:
        magic_item_id (int): an ID of a magic item in the database

    Returns:
        dmMagicItem: a domain object representing the magic item
    """
    
    model_collection = model.Collection.query.get_or_404(collection_item_id)
    
    return domain.Collection.from_model(model_collection)

def add_magic_item_to_list(magic_item: domain.MagicItem, collection: domain.Collection) -> bool:
    """Accepts a domain magic item and domain collection,
    then it adds the magic item to the database model collection,
    and returns a new domain collection representing the updated collection.

    Args:
        magic_item (domain.MagicItem): a domain object representing the magic item
        collection (domain.Collection): a domain object representing the collection

    Returns:
        domain.Collection: a domain object representing the collection
    """
    try:
        model_item_collection = model.ItemCollection(
            item_id = magic_item.id,
            collection_id = collection.id,
        )
        
        db.session.add(model_item_collection)
        db.session.commit()
        return True
    except:
        return False