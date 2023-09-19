import os
from parameterized import parameterized_class
from unittest import TestCase


os.environ["DATABASE_URL"] = "postgresql:///mythodex-test"


from app import app

from database import db
from users.models import User as UserModel
from magic_items.services import (
    MagicItemService,
    CollectionService,
    ItemCollectionService,
)
from magic_items.models import (
    Collection as CollectionModel,
    MagicItem as MagicItemModel,
    ItemCollection as ItemCollectionModel,
)
from magic_items.domains import (
    MagicItemDomain as MagicItemDomain,
    Collection as CollectionDomain,
)

from params_test import paramslist

db.create_all()


@parameterized_class(
    (
        "p_uid",
        "p_username",
        "p_email",
        "p_password",
        "p_cname",
        "p_cdesc",
        "p_iname",
        "p_itype",
        "p_irarity",
        "p_idesc",
        "p_icreatedby",
        "p_isource",
    ),
    paramslist,
)
class ItemServiceTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u = UserModel(
            username=self.p_username, email=self.p_email, password=self.p_password
        )
        u.id = self.p_uid
        db.session.add(u)
        db.session.commit()

        self.u = UserModel.query.get(self.p_uid)
        self.client = app.test_client()

        c = CollectionModel(
            name=self.p_cname,
            description=self.p_cdesc,
            user_id=self.p_uid,
        )

        db.session.add(c)
        db.session.commit()

        self.assertEqual(len(self.u.collections), 1)
        self.assertEqual(self.u.collections[0].name, self.p_cname)

        m = MagicItemModel(
            name=self.p_iname,
            item_type=self.p_itype,
            rarity=self.p_irarity,
            description=[f"{self.p_irarity}, {self.p_itype}", self.p_idesc],
            source="user",
            created_by=self.p_uid,
        )

        db.session.add(m)
        db.session.commit()

        self.assertEqual(len(self.u.created_items), 1)
        self.assertEqual(self.u.created_items[0].name, self.p_iname)

        ic = ItemCollectionModel(
            item_id=self.u.created_items[0].id,
            collection_id=self.u.collections[0].id,
        )

        db.session.add(ic)
        db.session.commit()

        self.assertEqual(len(self.u.collections[0].items), 1)
        self.assertEqual(self.u.collections[0].items[0].name, self.p_iname)

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_item_service_get(self):
        m_domain = MagicItemService.get(self.u.created_items[0].id)
        self.assertEqual(m_domain.name, self.u.created_items[0].name)

    def test_item_service_get_filtered_type(self):
        filter_dict = {
            "item_type": self.p_itype,
        }
        m_domains = MagicItemService.get_filtered(**filter_dict)
        self.assertEqual(m_domains[0].name, self.u.created_items[0].name)

    def test_item_service_get_filtered_name_rarity(self):
        filter_dict = {
            "name": self.p_iname,
            "rarity": self.p_irarity,
        }
        m_domains = MagicItemService.get_filtered(**filter_dict)
        self.assertEqual(m_domains[0].name, self.u.created_items[0].name)

    def test_item_service_get_filtered_wrong(self):
        filter_dict = {
            "name": "wrong name",
        }
        m_domains = MagicItemService.get_filtered(**filter_dict)
        self.assertEqual(len(m_domains), 0)

    def test_collection_service_add_item(self):
        CollectionService.add_magic_item(
            self.u.created_items[0].id, self.u.collections[0].id
        )
        inventory = (
            ItemCollectionModel.query.filter_by(
                item_id=self.u.created_items[0].id,
            )
            .first()
            .inventory
        )
        self.assertEqual(inventory, 2)

    def test_collection_service_add_more(self):
        CollectionService.add_magic_item(
            self.u.created_items[0].id, self.u.collections[0].id
        )
        CollectionService.add_magic_item(
            self.u.created_items[0].id, self.u.collections[0].id
        )
        inventory = (
            ItemCollectionModel.query.filter_by(
                item_id=self.u.created_items[0].id,
            )
            .first()
            .inventory
        )
        self.assertEqual(inventory, 3)

    def test_collection_service_reduce_item(self):
        CollectionService.reduce_magic_item(
            self.u.created_items[0].id, self.u.collections[0].id
        )
        inventory = (
            ItemCollectionModel.query.filter_by(
                item_id=self.u.created_items[0].id,
            )
            .first()
            .inventory
        )
        self.assertEqual(inventory, 1)

    def test_collection_service_remove_item(self):
        CollectionService.remove_magic_item(
            self.u.created_items[0].id, self.u.collections[0].id
        )
        inventory = ItemCollectionModel.query.filter_by(
            item_id=self.u.created_items[0].id,
        ).first()
        self.assertEqual(inventory, None)

    def test_collection_service_get(self):
        c_domain = CollectionService.get(self.u.collections[0].id)
        self.assertEqual(c_domain.name, self.u.collections[0].name)

    def test_collection_service_get_filtered_user(self):
        filter_dict = {
            "user_id": self.p_uid,
        }
        c_domains = CollectionService.get_filtered(**filter_dict)
        self.assertEqual(c_domains[0].name, self.u.collections[0].name)

    def test_collection_service_get_filtered_user_and_collection_name(self):
        filter_dict = {
            "user_id": self.p_uid,
            "name": self.p_cname,
        }
        c_domains = CollectionService.get_filtered(**filter_dict)
        self.assertEqual(c_domains[0].name, self.u.collections[0].name)

    def test_collection_service_get_filtered_description(self):
        filter_dict = {
            "description": self.p_cdesc,
        }
        c_domains = CollectionService.get_filtered(**filter_dict)
        self.assertEqual(c_domains[0].name, self.u.collections[0].name)

    def test_collection_service_get_filtered_wrong(self):
        filter_dict = {
            "description": "wrong desc",
        }
        c_domains = CollectionService.get_filtered(**filter_dict)
        self.assertEqual(len(c_domains), 0)

    def test_collection_service_delete(self):
        CollectionService.delete(self.u.collections[0].id, self.u.id)
        self.assertEqual(len(self.u.collections), 0)
