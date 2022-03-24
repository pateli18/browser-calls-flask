from typing import Tuple
from flask import render_template, flash, jsonify, request, redirect
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant

from . import app, db
from .forms import SupportTicketForm
from .models import SupportTicket

from twilio.twiml.voice_response import VoiceResponse, Dial


@app.route('/')
def root():
    form = SupportTicketForm()
    return render_template('home.html', form=form)


@app.route('/tickets', methods=['GET', 'POST'])
def new_ticket():
    success_message = "Your ticket was submitted! An agent will call you soon."
    form = SupportTicketForm()

    if form.validate_on_submit():
        ticket = SupportTicket(**form.data)
        db.session.add(ticket)
        db.session.commit()
        flash(success_message)
        return redirect('/')

    return render_template('home.html', form=form)


@app.route('/dashboard', methods=['GET'])
def dashboard():
    support_tickets = SupportTicket.query.all()
    return render_template('support_dashboard.html', support_tickets=support_tickets)


@app.route('/support/token', methods=['GET'])
def get_token():
    """Returns a Twilio Client token"""
    identity = (
        'support_agent' if request.args.get('forPage') == '/dashboard' else 'customer'
    )

    # Create access token with credentials
    access_token = AccessToken(
        app.config['TWILIO_ACCOUNT_SID'],
        app.config['TWILIO_API_KEY'],
        app.config['TWILIO_API_SECRET'],
        identity=identity,
    )

    # Create a Voice grant and add to token
    voice_grant = VoiceGrant(
        outgoing_application_sid=app.config['TWIML_APPLICATION_SID'],
        incoming_allow=True,  # Optional: add to allow incoming calls
    )
    access_token.add_grant(voice_grant)

    token = access_token.to_jwt()

    return jsonify({'token': token.decode()})


@app.route('/support/call', methods=['POST'])
def call():
    """Returns TwiML instructions to Twilio's POST requests"""
    response = VoiceResponse()

    dial = Dial(callerId=app.config['TWILIO_NUMBER'], record="record-from-answer-dual")
    dial.number(request.form['phoneNumber']) #

    return str(response.append(dial))


@app.route('/transcribe/{call_sid}', methods=['GET'])
def transcribe(call_sid: str):
    # TODO: add logic here
    print(call_sid)