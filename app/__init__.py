import os

from flask import Flask, render_template, request, flash, redirect, session

from app.utl.user import User
from app.session import *

app = Flask(__name__)

app.secret_key = os.urandom(64)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", current_user = current_user())

@app.route('/login', methods=['GET', 'POST'])
def login():
    # check if form was submitted
    if 'username' in request.form.keys() and \
            'password' in request.form.keys():
        # read the data from the form
        # we can use [] now since we know the key exists
        username = request.form['username']
        password = request.form['password']

        # make sure that the form data is valid
        valid = True

        to_login = User.get_user(username) # gets user object using username

        auth_valid = True

        if to_login is None: # if a user with that username doesn't exist
            flash('That username does not belong to a registered account!','red')
            auth_valid = False
        elif to_login.password != password: # if they typed in the wrong password
            flash('Incorrect password!','red')
            auth_valid = False

        if not valid or not auth_valid:
            flash('Please fix the above error(s) before submitting the form again!', 'red')
        else:
            login_user(to_login) # from session.py
            message = 'Successfully logged in'
            flash(message, 'green')
            return redirect('/')
    return render_template("login.html", title = "Log In")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'username' in request.form.keys() and \
            'password' in request.form.keys() and \
            'password_repeat' in request.form.keys():

        # read the data from the form
        username = request.form['username']
        password = request.form['password']
        password_repeat = request.form['password_repeat']

        # make sure that the form data is valid
        valid = True

        if not password == password_repeat: # if they typed in a different password in repeat
            flash('Passwords do not match!', 'red')
            valid = False

        if not User.username_avaliable(username): # checks database if username already exists
            flash('Username already taken!', 'red')
            valid = False

        if not valid:
            flash('Please fix the above error(s) before submitting the form again!', 'red')
        else:
            User.new_user(username, password)
            return redirect('login')
    return render_template('signup.html', title = 'Sign Up')

# logout user
@app.route('/logout')
def logout():
    logout_user()
    flash('Successfully logged out!', 'green')
    return redirect('/')