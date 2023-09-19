
from magic_items.models import (
    Collection as CollectionModel,
    ItemCollection as ItemCollectionModel,
    MagicItem as MagicItemModel,
)
from datetime import datetime
from database import db
from typing import List, Optional, Dict

import random

from sqlalchemy import func

UNAUTH_MSG = "User not authorized"

ITEMS_PER_PAGE = 12

ITEM_RARITY = [
    ("Common","Common"),
    ("Uncommon","Uncommon"),
    ("Rare","Rare"),
    ("Very Rare","Very Rare"),
    ("Legendary","Legendary"),
]

ITEM_TYPES = [
    ("Scroll","Scroll"),
    ("Rod","Rod"),
    ("Armor","Armor"),
    ("Ammunition","Ammunition"),
    ("Ring","Ring"),
    ("Potion","Potion"),
    ("Staff","Staff"),
    ("Wondrous Item","Wondrous Item"),
    ("Wand","Wand"),
    ("Weapon","Weapon"),
]

ITEM_SOURCE = [
    ("","Source"),
    ("dnd5eapi","Official Resources"),
    ("user","User Created"),
]

from magic_items.forms import CollectionAddForm, ItemForm, ItemFilterForm

from magic_items.domains import (
    Collection as CollectionDomain,
    ItemCollection as ItemCollectionDomain,
    MagicItemDomain as MagicItemDomain,
    StandardCollectionFilters,
    StandardMagicItemFilters,
)


#######################
## New services using domain classes


class MagicItemFlashMessage:
    unauth = {
        "message": "Not authorized to make changes to that magic item",
        "category": "danger",
    }
    login_to_manage = {
        "message": "Please login or signup to manage magic items and collections",
        "category": "warning",
    }
    
    @classmethod
    def create_success(cls, item_name:str,) -> dict:
        return {
        "message": f"New item {item_name} added!",
        "category": "success",
    }

class MagicItemService:
    @classmethod
    def create(cls, user_id: int, form: ItemForm) -> MagicItemDomain:

        data = {
            k: v
            for k, v in form.data.items()
            if k != "csrf_token" and k != "description"
        }

        item_model = MagicItemModel(
            **data,
            description=[
                f"{form.rarity.data}, {form.item_type.data}",
                form.description.data,
            ],
            source="user",
            created_by=user_id,
        )

        db.session.add(item_model)
        db.session.commit()

        return MagicItemDomain.from_model(item_model)

    @classmethod
    def get(
        cls,
        item_id: int,
    ) -> MagicItemDomain:
        item_model = MagicItemModel.query.get(item_id)
        return MagicItemDomain.from_model(item_model)

    @classmethod
    def get_filtered(
        cls,
        **filters: dict,
    ) -> List[MagicItemDomain]:
        
        
        invalid_filter = StandardMagicItemFilters.check(**filters)
        if invalid_filter is not True:
            print(f"Invalid filter: {invalid_filter}")
            raise Exception('Magic Item filter not allowed')


        edited_filter = {}

        for filter in filters:
            if filters[filter] != "" and filter != "p":
                edited_filter.update({filter: filters[filter]})

        model_magic_items = MagicItemModel.query.filter_by(**edited_filter).all()
        domain_magic_items = []

        for magic_item_model in model_magic_items:
            magic_item_domain = MagicItemDomain.from_model(magic_item_model)
            domain_magic_items.append(magic_item_domain)

        return domain_magic_items

    @classmethod
    def get_filtered_paginated(
        cls,
        **filters: dict,
    ) -> List[List[MagicItemDomain]]:
        
        
        if StandardMagicItemFilters.check(**filters) is not True:
            raise Exception('Magic Item filter not allowed')

        edited_filter = {}

        for filter in filters:
            if filters[filter] != "" and filter != "p":
                edited_filter.update({filter: filters[filter]})

        model_magic_items = MagicItemModel.query.filter_by(**edited_filter).all()
        
        model_pagination = db.paginate(model_magic_items, per_page=ITEMS_PER_PAGE)
        
        domain_pagination = []
        
        i = 1
        
        while i <= model_pagination.pages:
            domain_page = MagicItemDomain.from_models_list(model_pagination.items)
            domain_pagination.append(domain_page)
            model_pagination = model_pagination.next()
            i += 1

        return domain_pagination

    @classmethod
    def update(cls, user_id: int, magic_item_id: int, form: ItemForm):

        item_model = MagicItemModel.query.get_or_404(magic_item_id)

        for k, v in form.data.items():
            if k != "csrf_token" and k != "description":
                setattr(item_model, k, v)

        item_model.description = (
            f"{form.rarity.data}, {form.item_type.data}",
            form.description.data,
        )
        item_model.last_updated = datetime.utcnow()

        db.session.commit()

        return MagicItemDomain.from_model(item_model)

    @classmethod
    def delete(cls, user_id: int, magic_item_id: int) -> bool:

        item_model = MagicItemModel.query.get_or_404(magic_item_id)

        if item_model.created_by is not user_id:
            raise Exception(UNAUTH_MSG)

        db.session.delete(item_model)
        db.session.commit()

    @classmethod
    def random(
        cls,
    ) -> MagicItemDomain:

        item_model = MagicItemModel.query.order_by(func.random()).first()

        return MagicItemDomain.from_model(item_model)


class CollectionService:
    @classmethod
    def create(
        cls,
        user_id: int,
        form: CollectionAddForm,
    ) -> CollectionDomain:

        data = {k: v for k, v in form.data.items() if k != "csrf_token"}

        collection_model = CollectionModel(
            **data,
            user_id=user_id,
        )

        db.session.add(collection_model)
        db.session.commit()

        return CollectionDomain.from_model(collection_model)

    @classmethod
    def update(
        cls,
        user_id: int,
        collection_id: int,
        form: CollectionAddForm,
    ) -> CollectionDomain:

        collection_model = CollectionModel.query.get_or_404(collection_id)

        if collection_model.user_id is not user_id:
            raise Exception(UNAUTH_MSG)

        for k, v in form.data.items():
            if k != "csrf_token":
                setattr(collection_model, k, v)

        collection_model.last_updated = datetime.utcnow()

        db.session.commit()

        return CollectionDomain.from_model(collection_model)

    @classmethod
    def delete(cls, collection_id: int, user_id: int):

        collection_model = CollectionModel.query.get(collection_id)

        if collection_model.user_id is not user_id:
            raise Exception(UNAUTH_MSG)

        db.session.delete(collection_model)
        db.session.commit()

    @classmethod
    def get(
        cls,
        collection_id: int,
    ) -> CollectionDomain:
        collection_model = CollectionModel.query.get(collection_id)
        return CollectionDomain.from_model(collection_model)

    @classmethod
    def get_filtered(
        cls,
        **filters: dict,
    ) -> List[CollectionDomain]:
        
        if StandardCollectionFilters.check(**filters) is not True:
            raise Exception('Collection filter not allowed')

        model_collections = CollectionModel.query.filter_by(**filters).all()
        
        domain_collections = []

        for collection_model in model_collections:
            collection_domain = CollectionDomain.from_model(collection_model)
            domain_collections.append(collection_domain)

        return domain_collections

    @classmethod
    def get_filtered_paginated(
        cls,
        **filters: dict,
    ) -> List[CollectionDomain]:
        
        if StandardCollectionFilters.check(**filters) is not True:
            raise Exception('Collection filter not allowed')

        model_collections = CollectionModel.query.filter_by(**filters).all()
        
        model_page = db.paginate(model_collections)
        
        domain_collections = []

        for collection_model in model_collections:
            collection_domain = CollectionDomain.from_model(collection_model)
            domain_collections.append(collection_domain)

        return domain_collections

    @classmethod
    def add_magic_item(
        cls,
        magic_item_id: int,
        collection_id: int,
    ) -> bool:

        item_collection_model = ItemCollectionModel.query.filter_by(
            item_id=magic_item_id,
            collection_id=collection_id,
        ).first()

        if not item_collection_model:
            new_item_collection_model = ItemCollectionModel(
                item_id=magic_item_id,
                collection_id=collection_id,
            )
            db.session.add(new_item_collection_model)
            db.session.commit()
            return True

        else:
            item_collection_model.inventory += 1
            db.session.commit()
            return True

    @classmethod
    def reduce_magic_item(
        cls,
        magic_item_id: int,
        collection_id: int,
    ) -> bool:

        item_collection_model = ItemCollectionModel.query.filter_by(
            item_id=magic_item_id,
            collection_id=collection_id,
        ).first()

        if item_collection_model and item_collection_model.inventory > 1:
            item_collection_model.inventory -= 1
            db.session.commit()
            return True

        return False

    @classmethod
    def remove_magic_item(
        cls,
        magic_item_id: int,
        collection_id: int,
    ) -> bool:

        item_collection_model = ItemCollectionModel.query.filter_by(
            item_id=magic_item_id,
            collection_id=collection_id,
        ).first()

        if not item_collection_model:
            return False

        db.session.delete(item_collection_model)
        db.session.commit()
        return True

    @classmethod
    def random(
        cls,
    ) -> CollectionDomain:

        collection_model = CollectionModel.query.order_by(func.random()).first()

        return CollectionDomain.from_model(collection_model)

    @classmethod
    def random_item(
        cls,
        collection_id: int,
    ) -> MagicItemDomain:

        
        item_collection_models = ItemCollectionModel.query.filter_by(
            collection_id=collection_id
        ).all()

        rand_inventory = []

        for item in item_collection_models:
            i = item.inventory
            while i > 0:
                rand_inventory.append(item)
                i -= i

        item_id = random.choice(rand_inventory).item_id

        item_model = MagicItemModel.query.get(item_id)
        
        return MagicItemDomain.from_model(item_model)


class ItemCollectionService:
    @classmethod
    def get_inventory_numbers(
        cls,
        collection_id: int,
    ) -> dict:

        item_collection_models = ItemCollectionModel.query.filter_by(
            collection_id=collection_id
        ).all()

        inventory = {}

        for item in item_collection_models:
            inventory[item.item_id] = item.inventory

        return inventory
