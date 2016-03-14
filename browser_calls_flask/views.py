from . import app, db
from flask import render_template, redirect
from .forms import SupportTicketForm
from .models import SupportTicket


@app.route('/')
def root():
    return render_template('home.html')


@app.route('/tickets', methods=['GET', 'POST'])
def new_ticket():
    form = SupportTicketForm()
    if form.validate_on_submit():
        ticket = SupportTicket(**form.data)
        db.session.add(ticket)
        db.session.commit()
        return redirect('/')
    return render_template('ticket_form.html', form=form)
