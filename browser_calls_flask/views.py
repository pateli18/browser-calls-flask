from . import app, db
from flask import render_template, redirect
from .forms import SupportTicketForm
from .models import SupportTicket


@app.route('/')
def root():
    form = SupportTicketForm()
    return render_template('ticket_form.html', form=form)


@app.route('/tickets', methods=['GET', 'POST'])
def new_ticket():
    form = SupportTicketForm()
    if form.validate_on_submit():
        ticket = SupportTicket(**form.data)
        db.session.add(ticket)
        db.session.commit()
        return redirect('/')
    return render_template('ticket_form.html', form=form)


@app.route('/dashboard')
def dashboard():
    support_tickets = SupportTicket.query.all()
    return render_template('support_dashboard.html', support_tickets=support_tickets)
