from flask_testing import TestCase

from api.app import create_app
from api.db import db
from api.settings import TestConfiguration


class BaseTestCase(TestCase):

    def create_app(self):
        return create_app(TestConfiguration)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.drop_all()
