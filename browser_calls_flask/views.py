from flask import render_template, redirect, flash, jsonify, request

from . import app, db
from .forms import SupportTicketForm
from .models import SupportTicket
from .validators import is_valid_number

from twilio.util import TwilioCapability


@app.route('/')
def root():
    form = SupportTicketForm()
    return render_template('ticket_form.html', form=form)


@app.route('/tickets', methods=['GET', 'POST'])
def new_ticket():
    success_message = "Your ticket was submitted! An agent will call you soon."
    form = SupportTicketForm()

    if form.validate_on_submit():
        if not is_valid_number(form.data['phone_number']):
            flash("Invalid phone number!")
            return render_template('ticket_form.html', form=form)
        ticket = SupportTicket(**form.data)
        db.session.add(ticket)
        db.session.commit()
        flash(success_message)
        return redirect('/')
    return render_template('ticket_form.html', form=form)


@app.route('/dashboard')
def dashboard():
    support_tickets = SupportTicket.query.all()
    return render_template('support_dashboard.html', support_tickets=support_tickets)


@app.route('/support/token')
def get_token():
    """Returns a Twilio Client token"""
    # Create a TwilioCapability object with our Twilio API credentials
    capability = TwilioCapability(
        app.config['TWILIO_ACCOUNT_SID'],
        app.config['TWILIO_AUTH_TOKEN'])

    # Allow our users to make outgoing calls with Twilio Client
    capability.allow_client_outgoing(app.config['TWIML_APPLICATION_SID'])

    # If the user is on the support dashboard page, we allow them to accept
    # incoming calls to "support_agent"
    # (in a real app we would also require the user to be authenticated)
    if request.args.get('forPage') == '/dashboard':
        capability.allow_client_incoming('support_agent')
    else:
        # Otherwise we give them a name of "customer"
        capability.allow_client_incoming('customer')

    # Generate the capability token
    token = capability.generate()

    return jsonify({'token': token})
