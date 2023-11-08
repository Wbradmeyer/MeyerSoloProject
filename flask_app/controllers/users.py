from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user

# Create Users Controller
@app.route('/users/create', methods=['POST'])
def create_user():
    user_id = user.User.create_new_user(request.form)
    if user_id:
        return redirect('/home')      
    return redirect('/')


# Read Users Controller
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users/login', methods=['POST'])
def login_user():
    if user.User.login_user(request.form):
        return redirect('/home')
    return redirect('/')

@app.route('/users/logout')
def logout_user():
    session.clear()
    return redirect('/')

