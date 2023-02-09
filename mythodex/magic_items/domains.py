from typing import List
from dataclasses import dataclass
from datetime import datetime
from magic_items.models import MagicItem as MagicItemModel, Collection as CollectionModel, ItemCollection as ItemCollectionModel

@dataclass
class ItemVariant:
    original_item_id: int
    variant_item_id: int

@dataclass
class MagicItem:
    id: int
    name: str
    item_type: str
    rarity: str
    is_variant: bool
    description: List[str]
    created_by: int
    source: str
    date_created: datetime
    last_updated: datetime
    
    @property
    def shorten_description(self):
        desc = self.description[1]
        if len(desc) <= 55:
            return desc
        return desc[0:55] + '...'
    
    @property
    def shorten_heading(self):
        desc = self.description[0]
        if len(desc) <= 20:
            return desc
        return desc[0:20] + '...'
    
    @property
    def shorten_title(self):
        name = self.name
        if len(name) <= 18:
            return name
        return name[0:18] + '...'
    
    @classmethod
    def from_model(cls, model_instance: MagicItemModel) -> 'MagicItem':
        return cls(
            id=model_instance.id,
            name=model_instance.name,
            item_type=model_instance.item_type,
            rarity=model_instance.rarity,
            is_variant=model_instance.is_variant,
            description=model_instance.description,
            created_by=model_instance.created_by,
            source=model_instance.source,
            date_created=model_instance.date_created,
            last_updated=model_instance.last_updated,
    )
    
@dataclass
class ItemCollection:
    item_id: int
    collection_id: int
    times_on_collection: int
    
    @classmethod
    def from_model(cls, model_instance: ItemCollectionModel) -> 'ItemCollection':
        return cls(
            item_id=model_instance.item_id,
            collection_id=model_instance.collection_id,
            times_on_collection=model_instance.times_on_collection,
    )

@dataclass
class Collection:
    id: int
    name: str
    description: str
    user_id: int
    items: List[MagicItem]
    date_created: datetime
    last_updated: datetime
    
    @property
    def shorten_description(self):
        desc = self.description
        if len(desc) <= 55:
            return desc
        return desc[0:55] + '...'
    
    @property
    def shorten_title(self):
        name = self.name
        if len(name) <= 18:
            return name
        return name[0:18] + '...'
    
    @classmethod
    def from_model(cls, model_instance: CollectionModel) -> 'Collection':
        return cls(
            id=model_instance.id,
            name=model_instance.name,
            description=model_instance.description,
            user_id=model_instance.user_id,
            items=model_instance.items,
            date_created=model_instance.date_created,
            last_updated=model_instance.last_updated,
    )