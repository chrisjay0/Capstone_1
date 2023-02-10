import os
from parameterized import parameterized, parameterized_class
from unittest import TestCase
from sqlalchemy import exc



os.environ['DATABASE_URL'] = "postgresql:///mythodex-test"


from app import app

from database import db
from users.models import User as UserModel
from magic_items.domains import MagicItem as MagicItemDomain, Collection as CollectionDomain
from users.services import UserService
from magic_items.models import Collection as CollectionModel, MagicItem as MagicItemModel, ItemCollection as ItemCollectionModel

from params_test import paramslist
db.create_all()

@parameterized_class(
    ('p_uid','p_username','p_email','p_password','p_cname','p_cdesc','p_iname','p_itype','p_irarity','p_idesc','p_icreatedby','p_isource'),paramslist
)
class MagicItemsDomainsTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u = UserModel(
            username=self.p_username,
            email=self.p_email,
            password=self.p_password)
        u.id = self.p_uid
        db.session.add(u)
        db.session.commit()

        self.u = UserModel.query.get(self.p_uid)
        self.client = app.test_client()
        
        c = CollectionModel(
            name = self.p_cname,
            description = self.p_cdesc,
            user_id = self.p_uid,
            
        )

        db.session.add(c)
        db.session.commit()

        self.assertEqual(len(self.u.collections), 1)
        self.assertEqual(self.u.collections[0].name, self.p_cname)
        
        m = MagicItemModel(
            name = self.p_iname,
            item_type = self.p_itype,
            rarity=self.p_irarity,
            description= [f'{self.p_irarity}, {self.p_itype}',self.p_idesc],
            source="user",
            created_by=self.p_uid,
        )

        db.session.add(m)
        db.session.commit()

        self.assertEqual(len(self.u.created_items), 1)
        self.assertEqual(self.u.created_items[0].name, self.p_iname)
        
        ic = ItemCollectionModel(
            item_id = self.u.created_items[0].id,
            collection_id = self.u.collections[0].id,
        )

        db.session.add(ic)
        db.session.commit()

        self.assertEqual(len(self.u.collections[0].items), 1)
        self.assertEqual(self.u.collections[0].items[0].name, self.p_iname)

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    
    def test_collection_domain(self):
        
        c_model = CollectionModel.query.get(self.u.collections[0].id)
        
        c_domain = CollectionDomain.from_model(c_model)

        self.assertEqual(c_model.name, c_domain.name)
        
        