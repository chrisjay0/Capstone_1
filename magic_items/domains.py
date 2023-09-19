from typing import List
from dataclasses import dataclass
from datetime import datetime
from magic_items.models import (
    MagicItem as MagicItemModel,
    Collection as CollectionModel,
    ItemCollection as ItemCollectionModel,
)

COLLECTION_FILTERS = [
    'name',
    'description',
    'user_id',
    'date_created',
    'last_updated',
    'p',
]

MAGIC_ITEM_FILTERS = [
    'name',
    'description',
    'created_by',
    'date_created',
    'last_updated',
    'item_type',
    'rarity',
    'source',
    'p',
]

MAX_CHAR_SHORTEN = {
    "description":55,
    "heading":20,
    "title":18,
}

def shorten_strings(strings:dict) -> dict:
    for (name, string) in strings.items():
        if len(string) > MAX_CHAR_SHORTEN.get(name):
            strings[name] = string[0:MAX_CHAR_SHORTEN.get(name)] + '...'
    return strings
    


@dataclass
class ItemVariant:
    original_item_id: int
    variant_item_id: int


@dataclass
class MagicItemDomain:
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
    def short_strings(self) -> dict:
        
        strings = {
            'title':self.name,
            'heading':self.description[0],
            'description':self.description[1],
        }
                
        return shorten_strings(strings)
    
    def attributes(self):
        [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self, a))]

    @classmethod
    def from_model(cls, model_instance: MagicItemModel) -> "MagicItemDomain":
        
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

    @classmethod
    def from_models_list(cls, model_list: List[MagicItemModel] ) -> List["MagicItemDomain"]:
        
        domain_list = []
        
        for model_instance in model_list:
            
            domain_instance = cls(
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
            
            domain_list.append(domain_instance)
            
        return domain_list


@dataclass
class ItemCollection:
    item_id: int
    collection_id: int
    times_on_collection: int

    @classmethod
    def from_model(cls, model_instance: ItemCollectionModel) -> "ItemCollection":
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
    items: List[MagicItemDomain]
    date_created: datetime
    last_updated: datetime
    
    @property
    def short_strings(self) -> dict:
        
        strings = {
            'title':self.name,
            'description':self.description,
        }
                
        return shorten_strings(strings)

    @classmethod
    def from_model(cls, model_instance: CollectionModel) -> "Collection":
        return cls(
            id=model_instance.id,
            name=model_instance.name,
            description=model_instance.description,
            user_id=model_instance.user_id,
            items=MagicItemDomain.from_models_list(model_instance.items),
            date_created=model_instance.date_created,
            last_updated=model_instance.last_updated,
        )
        
@dataclass
class StandardCollectionFilters:
    
    @classmethod
    def check(cls, **filters: dict,) -> bool:
        for key in filters.keys():
            if key not in COLLECTION_FILTERS:
                return key
        return True
        
@dataclass
class StandardMagicItemFilters:
    
    @classmethod
    def check(cls, **filters: dict,) -> bool:
        for key in filters.keys():
            if key not in MAGIC_ITEM_FILTERS:
                return key
        return True