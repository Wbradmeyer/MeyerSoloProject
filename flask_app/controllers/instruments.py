from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import instrument
import calendar

# Create Instruments Controller
@app.route('/instruments/new', methods=['POST', 'GET'])
def create_instrument():
    if 'user_id' not in session: return redirect('/')
    if request.method == 'POST':
        instrument_id = instrument.Instrument.create_new_instrument(request.form)
        if instrument_id:
            return redirect('/dashboard')
    return render_template('create_instrument.html', data = request.form)


# Read Instruments Controller
@app.route('/dashboard')
def show_instruments():
    if 'user_id' not in session: return redirect('/')
    all_instruments = instrument.Instrument.get_all_instruments_with_users()
    return render_template('dashboard.html', instruments = all_instruments)

@app.route('/instruments/<int:id>')
def instrument_card(id):
    if 'user_id' not in session: return redirect('/')
    this_instrument = instrument.Instrument.get_instrument_by_id(id)
    month = calendar.month_name[this_instrument.date_seen.month]
    return render_template('one_instrument.html', instrument = this_instrument, month = month)


# Update Instruments Controller
@app.route('/instruments/edit/<int:id>', methods=['POST', 'GET'])
def edit_instrument(id):
    if 'user_id' not in session: return redirect('/')
    if request.method == 'POST':
        updated = instrument.Instrument.update_instrument(request.form)
        if updated:
            return redirect('/dashboard')
    instrument_to_update = instrument.Instrument.get_instrument_by_id(id)
    if instrument_to_update.user_id == session['user_id']:
        return render_template('edit_instrument.html', instrument = instrument_to_update)
    else:
        return redirect('/users/logout')


# Delete Instruments Controller
@app.route('/instruments/delete/<int:id>')
def delete_instrument(id):
    if 'user_id' not in session: return redirect('/')
    if instrument.Instrument.delete_instrument_by_id(id):
        return redirect('/dashboard')
    else:
        return redirect('/users/logout')