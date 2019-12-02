import os, requests

from flask import Flask, render_template, request, flash, redirect, session, url_for

from app.utl.user import User
from app.session import *
import urllib.request, json

app = Flask(__name__)

app.secret_key = os.urandom(64)

# makes session permanent
@app.before_request
def before_request():
    session.permanent = True

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title = "Home", current_user = current_user())


@app.route( '/recipe')
def recipe():
    return render_template('recipe.html', title = 'Recipe')

@app.route( '/recipe_search', methods=['GET', 'POST'])
def recipeSearch():
    data = None
    if (request.form):
        url = "http://www.recipepuppy.com/api/?q={}&p=1".format(request.form['query'])
        req = urllib.request.urlopen(url)
        response = req.read()
        data = json.loads(response)['results']
    return render_template( 'recipe_search.html', title = "Recipe Search", data = data)

@app.route( '/fooddata', methods=['GET', 'POST'])
def fooddata():
    data = None
    if ('food' in request.form):
        food = request.form['food']
        url = "https://api.nal.usda.gov/fdc/v1/search?api_key=eVfCzyFo4P5Aoie9Lt1kniHK7iUfafWXNMYYbwsl"
        data = '{"generalSearchInput":"%s", "includeDataTypes":{"Survey (FNDDS)":true,"Foundation":true,"Branded":false} }'  % food
        headers = {"Content-Type":"application/json"}
        r = requests.post(url, data = data, headers = headers)
        data = r.json() # dictionary of search results
        for result in data['foods']:
            result['link'] = "https://api.nal.usda.gov/fdc/v1/{}?api_key=eVfCzyFo4P5Aoie9Lt1kniHK7iUfafWXNMYYbwsl".format(
                                        result['fdcId'])
    return render_template('food_data.html', title = 'Food Data', data = data)

@app.route('/restaurant')
def restaurant():
    return render_template('restaurant.html', title = "Restaurant")

@app.route( '/food_diary')
def foodDiary():
    if current_user() == None:
      flash('You must log in to access this page', 'warning')
      return redirect( url_for( 'login'))
    return render_template( 'food_diary.html', title = "Food Diary")

@app.route( '/new_entry', methods=['GET', 'POST'])
def newEntry():
    print(request.form)
    return render_template( 'new_entry.html'
                            , user = current_user())


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

# food data central: eVfCzyFo4P5Aoie9Lt1kniHK7iUfafWXNMYYbwsl
