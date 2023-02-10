import os
from parameterized import parameterized_class
from unittest import TestCase


os.environ["DATABASE_URL"] = "postgresql:///mythodex-test"


from app import app

from database import db
from users.models import User as UserModel
from users.services import UserService

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
class UserServiceTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        db.drop_all()
        db.create_all()

        u = UserModel(
            username=self.p_username,
            email=self.p_email,
            password=self.p_password,
        )
        u.id = self.p_uid
        db.session.add(u)
        db.session.commit()

        self.u = UserModel.query.get(self.p_uid)
        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_service(self):
        self.assertEqual(UserService.get_by_id(self.p_uid).username, self.p_username)
        self.assertEqual(
            UserService.get_by_username(self.p_username).id, int(self.p_uid)
        )

    def test_userservice_form_new(self):

        with app.test_client() as client:
            resp = client.post(
                "/signup",
                data={
                    "username": "tuser55",
                    "email": "t55@t.co",
                    "password": "agoodone",
                },
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Sign me up", html)
