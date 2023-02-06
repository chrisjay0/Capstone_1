from typing import List
from dataclasses import dataclass
from datetime import datetime
from magic_items.models import MagicItem as MagicItemModel, Collection as CollectionModel

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
    created_user_id: int
    source: str
    date_created: datetime
    last_updated: datetime
    
    @property
    def shorten_description(self):
        desc = self.description[1]
        if len(desc) <= 55:
            return desc
        return desc[0:55] + '...'
    
    @classmethod
    def from_model(cls, model_instance: MagicItemModel) -> 'MagicItem':
        return cls(
            id=model_instance.id,
            name=model_instance.name,
            item_type=model_instance.item_type,
            rarity=model_instance.rarity,
            is_variant=model_instance.is_variant,
            description=model_instance.description,
            created_user_id=model_instance.created_user_id,
            source=model_instance.source,
            date_created=model_instance.date_created,
            last_updated=model_instance.last_updated,
    )
    
@dataclass
class ItemCollection:
    item_id: int
    collection_id: int
    times_on_collection: int

@dataclass
class Collection:
    id: int
    name: str
    description: str
    user_id: int
    items: List[MagicItem]
    date_created: datetime
    last_updated: datetime
    
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