from unittest import TestCase

from browser_calls_flask import app, db


class BaseTest(TestCase):

    def setUp(self):
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
