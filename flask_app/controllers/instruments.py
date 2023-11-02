import os
from flask_app import app
from flask import render_template, redirect, request, session, url_for
from werkzeug.utils import secure_filename
from flask_app.models import instrument

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Create Instruments Controller
@app.route('/instruments/new', methods=['POST', 'GET'])
def create_instrument():
    # if 'user_id' not in session: return redirect('/')
    if request.method == 'POST':
        # if image file is present and allowed, save it to the upload folder
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # now create a new instrument passing in the image filename
        instrument_id = instrument.Instrument.create_new_instrument(request.form, filename)
        if instrument_id:
            return redirect('/home')
    return render_template('create_instrument.html', data = request.form)


# Read Instruments Controller
@app.route('/home')
def show_user_instruments():
    # if 'user_id' not in session: return redirect('/')
    all_instruments = instrument.Instrument.get_all_instruments_with_users()
    # REPLACE THIS WITH A QUERY!!!!
    owned_instruments = [inst for inst in all_instruments if inst.seller_id == session['user_id']]
    # print('*****************************************', session['first_name'])
    sold_instruments = instrument.Instrument.get_all_instruments_with_sellers()
    purchased = [inst for inst in sold_instruments if inst.user_id == session['user_id']]
    return render_template('home.html', owned_instruments = owned_instruments, purchased = purchased)

@app.route('/instruments/all')
def show_all_instruments():
    # if 'user_id' not in session: return redirect('/')
    all_instruments = instrument.Instrument.get_all_instruments_with_users()
    # REPLACE THIS WITH A QUERY!!!
    instruments_for_sale = [inst for inst in all_instruments if inst.sold == False]
    return render_template('display_all.html', instruments = instruments_for_sale)

@app.route('/instruments/<int:id>')
def instrument_card(id):
    # if 'user_id' not in session: return redirect('/')
    this_instrument = instrument.Instrument.get_instrument_by_id(id)
    return render_template('one_instrument.html', instrument = this_instrument)


# Update Instruments Controller
@app.route('/instruments/edit/<int:id>', methods=['POST', 'GET'])
def edit_instrument(id):
    # if 'user_id' not in session: return redirect('/')
    if request.method == 'POST':
        updated = instrument.Instrument.update_instrument(request.form)
        if updated:
            return redirect('/home')
    instrument_to_update = instrument.Instrument.get_instrument_by_id(id)
    if instrument_to_update.user_id == session['user_id']:
        inst_select = instrument.Instrument.get_instrument_select()
        quality_select = instrument.Instrument.get_quality_select()
        return render_template('edit_instrument.html', instrument = instrument_to_update, 
                            inst_select = inst_select, quality_select = quality_select)
    else:
        return redirect('/users/logout')
    
@app.route('/instruments/purchase/<int:id>', methods=['POST'])
def purchase_instrument(id):
    # if 'user_id' not in session: return redirect('/')
    instrument.Instrument.change_owner(id)
    return redirect('/home')


# Delete Instruments Controller
@app.route('/instruments/delete/<int:id>')
def delete_instrument(id):
    # if 'user_id' not in session: return redirect('/')
    if instrument.Instrument.delete_instrument_by_id(id):
        return redirect('/home')
    else:
        return redirect('/users/logout')