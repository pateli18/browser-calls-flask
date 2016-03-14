from .base import BaseTest
from browser_calls_flask.models import SupportTicket


class SupportTicketViewsTests(BaseTest):

    def test_root(self):
        response = self.client.get('/')
        assert "Welcome" in str(response.data)

    def test_save_ticket(self):
        self.post_ticket(name='Neo', phone_number='42', description='Issue while destroying the Matrix')
        new_ticket = SupportTicket.query.filter_by(name='Neo').first()
        self.assertNotEquals(None, new_ticket)

    def post_ticket(self, name, phone_number, description):
        data = dict(name=name, phone_number=phone_number, description=description)
        return self.client.post('/tickets', data=data, follow_redirects=True)
