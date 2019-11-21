import os

from flask import Flask, render_template, request, flash, redirect, session, url_for

from app.utl.user import User
from app.session import *
import urllib.request, json

app = Flask(__name__)

app.secret_key = os.urandom(64)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title = "Home", current_user = current_user())


@app.route( '/recipe')
def recipe():
    return render_template('recipe.html')

@app.route( '/recipe_search', methods=['GET', 'POST'])
def recipeSearch():
    data = None
    if (request.form):
        r = "http://www.recipepuppy.com/api/?q={}&p=1".format(request.form['query'])
        u = urllib.request.urlopen(r)
        response = u.read()
        data = json.loads(response)['results']
    return render_template( 'recipe_search.html', data = data)

@app.route('/restaurant')
def restaurant():
    return render_template('restaurant.html')

@app.route( '/query', methods = [ 'POST'])
def query():
    query = request.form[ 'keyword']
    # display results on search page
    return redirect(
        url_for(
            'search', query = query
            )
        )

@app.route( '/food_diary')
def foodDiary():
    if current_user() == None:
      flash('You must log in to access this page', 'warning')
      return redirect( url_for( 'login'))
    return render_template( 'food_diary.html')

@app.route( '/new_entry')
def newEntry():
    username = tester.getUserInfo( session[ 'userid'])[ 0]
    return render_template( 'new_entry.html',
                            username = username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # check if form was submitted
    form = request.form.keys()
    if 'username' in form and 'password' in form:
        # read the data from the form
        # we can use [] now since we know the key exists
        username = request.form['username']
        password = request.form['password']

        # make sure that the form data is valid
        valid = True

        to_login = User.get_user(username) # gets user object using username

        auth_valid = True

        if to_login is None: # if a user with that username doesn't exist
            flash('That username does not belong to a registered account!','danger')
            auth_valid = False
        elif to_login.password != password: # if they typed in the wrong password
            flash('Incorrect password!','danger')
            auth_valid = False

        if valid and auth_valid:
            login_user(to_login) # from session.py
            message = 'Successfully logged in'
            flash(message, 'success')
            return redirect(url_for('foodDiary'))
    return render_template("login.html", title = "Log In", current_user = current_user())

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # check if form was submitted
    form = request.form.keys()
    if 'username' in form and 'password' in form and 'password_repeat' in form:

        # read the data from the form
        username = request.form['username']
        password = request.form['password']
        password_repeat = request.form['password_repeat']

        # make sure that the form data is valid
        valid = True

        if not password == password_repeat: # if they typed in a different password in repeat
            flash('Passwords do not match!', 'danger')
            valid = False

        if not User.username_avaliable(username): # checks database if username already exists
            flash('Username already taken!', 'danger')
            valid = False

        if valid:
            User.new_user(username, password)
            return redirect('login')
    return render_template('signup.html', title = 'Sign Up', current_user = current_user())

# logout user
@app.route('/logout')
def logout():
    logout_user()
    flash('Successfully logged out!', 'success')
    return redirect('/')

#==========================user tests===========================

#addUser( "Michael","pls")
#addUser("Emily", "actually")
#addUser("Yaru","work")

#==========================diary functions===========================
