from browser_calls_flask import db
from datetime import datetime


class SupportTicket(db.Model):
    """ Represents a support ticket """
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime)

    def __init__(self, name, phone_number, description):
        self.name = name
        self.phone_number = phone_number
        self.description = description
        self.timestamp = datetime.utcnow()

    def __repr__(self):
        return '<SupportTicket %s - %s>' % (self.id, self.name)
