from .base import BaseTest
from browser_calls_flask.models import SupportTicket


class SupportTicketViewsTests(BaseTest):

    def test_save_valid_ticket(self):
        self.post_ticket(name='Neo', phone_number='+15551239483', description='Issue while destroying the Matrix')
        new_ticket = SupportTicket.query.filter_by(name='Neo').first()
        self.assertNotEquals(None, new_ticket)

    def test_checks_for_invalid_phone_numbers_before_saving(self):
        response = self.post_ticket(name='James', phone_number='92',
                                    description="I don't know how to use...")

        self.assertIn("Invalid phone number", str(response.data))
        new_ticket = SupportTicket.query.filter_by(name='James').first()
        self.assertEquals(None, new_ticket)

    def test_dashboard_shows_tickets(self):
        ticket1 = SupportTicket(name="John", phone_number="+15551239483",
                                description="Got an issue while...")
        self.db.session.add(ticket1)
        self.db.session.commit()
        response = self.client.get('/dashboard')
        self.assertIn("15551239483", str(response.data))

    def post_ticket(self, name, phone_number, description):
        data = dict(name=name, phone_number=phone_number, description=description)
        return self.client.post('/tickets', data=data, follow_redirects=True)
