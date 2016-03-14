import unittest


class BaseTest(unittest.TestCase):

    def setUp(self):
        from browser_calls_flask import app, db
        self.app = app
        self.db = db
        self.client = app.test_client()
