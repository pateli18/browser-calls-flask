from . import app, db
from flask import render_template, redirect, flash
from .forms import SupportTicketForm
from .models import SupportTicket
from .validators import is_valid_number


@app.route('/')
def root():
    form = SupportTicketForm()
    return render_template('ticket_form.html', form=form)


@app.route('/tickets', methods=['GET', 'POST'])
def new_ticket():
    form = SupportTicketForm()
    if form.validate_on_submit():
        if not is_valid_number(form.data['phone_number']):
            flash("Invalid phone number!")
            return render_template('ticket_form.html', form=form)
        ticket = SupportTicket(**form.data)
        db.session.add(ticket)
        db.session.commit()
        return redirect('/')
    return render_template('ticket_form.html', form=form)


@app.route('/dashboard')
def dashboard():
    support_tickets = SupportTicket.query.all()
    return render_template('support_dashboard.html', support_tickets=support_tickets)
