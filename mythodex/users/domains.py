from typing import List
from dataclasses import dataclass
from datetime import datetime
from magic_items.domains import Collection, MagicItem
from users.models import User as UserModel


@dataclass
class User:
    id: int
    username: str
    email: str
    image_url: str
    bio: str
    password: str
    collections: List[Collection]
    created_items: List[MagicItem]
    date_created: datetime
    last_updated: datetime

    @classmethod
    def from_model(cls, model_instance: UserModel) -> "User":
        return cls(
            id=model_instance.id,
            username=model_instance.username,
            email=model_instance.email,
            image_url=model_instance.image_url,
            bio=model_instance.bio,
            password=model_instance.password,
            collections=model_instance.collections,
            created_items=model_instance.created_items,
            date_created=model_instance.date_created,
            last_updated=model_instance.last_updated,
        )

    @classmethod
    def udate(cls) -> bool:
        try:
            cls.last_updated = datetime.utcnow()
            return True
        except:
            return False
