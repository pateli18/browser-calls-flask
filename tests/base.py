import unittest
from browser_calls_flask.models import SupportTicket


class BaseTest(unittest.TestCase):

    def setUp(self):
        from browser_calls_flask import app, db
        self.app = app
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.db = db
        self.client = app.test_client()

    def tearDown(self):
        SupportTicket.query.delete()
        self.db.session.commit()
