from .base import BaseTest


class SupportTicketFormTests(BaseTest):

    def test_root(self):
        response = self.client.get('/')
        self.assertIn('Welcome', response.data)
