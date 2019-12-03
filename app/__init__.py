import os, requests

from flask import Flask, render_template, request, flash, redirect, session, url_for

from app.utl.user import User
from app.utl.blog import Blog
from app.session import *
import urllib.request, json

app = Flask(__name__)

app.secret_key = os.urandom(64)

f = open("keys.json","r")
data = f.read()
keys = json.loads(data)
zomato_key = keys['zomato']
fooddata_key = keys['fooddata']

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
    return render_template('recipe.html', title = 'Recipe',current_user = current_user())

@app.route( '/recipe_search', methods=['GET', 'POST'])
def recipeSearch():
    data = None
    if (request.form):
        url = "http://www.recipepuppy.com/api/?q={}&p=1".format(request.form['query'])
        req = urllib.request.urlopen(url)
        response = req.read()
        data = json.loads(response)['results']
    return render_template( 'recipe_search.html', title = "Recipe Search", data = data,current_user = current_user())

@app.route( '/fooddata', methods=['GET', 'POST'])
def fooddata():
    data = None
    if (fooddata_key == "YOUR_API_KEY_HERE"):
        flash("FoodData API key not in the right place! Please look at README.md", "danger")
    elif ( 'food' in request.form):     # checks that food key is in post
        food = request.form[ 'food']   # gets the key value
        url = "https://api.nal.usda.gov/fdc/v1/search?api_key={}".format(fooddata_key)
        data = '{"generalSearchInput":"%s", "includeDataTypes":{"Survey (FNDDS)":true,"Foundation":true,"Branded":false} }' % food
             # hardcoding post keyval pairs sending to server, returns some data
        headers = { "Content-Type":"application/json"}     # context # json = ***************
        r = requests.post( url, data = data, headers = headers)
        data = r.json() # dictionary of search results
        for result in data['foods']:
            result['link'] = "https://api.nal.usda.gov/fdc/v1/{}?api_key={}".format(
                                        result['fdcId'], fooddata_key)
    elif('link' in request.form):
        req = urllib.request.urlopen(request.form['link'])
        response = req.read()
        data = json.loads(response)
    return render_template('food_data.html', title = 'Food Data', data = data, current_user = current_user())

@app.route('/restaurant')
def restaurant():
    return render_template('restaurant.html', title = "Restaurant", current_user = current_user())

# William Cao from Dojo helped me
@app.route( '/restaurant_search', methods=[ 'GET', 'POST'])
def restaurantSearch():
    # return render_template('restaurant_search.html', title = "Restaurant")
    data = None
    if (zomato_key == "YOUR_API_KEY_HERE"):
        flash("Zomato API key not in the right place! Please look at README.md", "danger")
    elif ( request.form):
        restaurant = request.form[ 'query']
        url = "https://developers.zomato.com/api/v2.1/search?q={}&count=10".format( restaurant)
        headers = { "Content-Type": "application/json", "user-key": zomato_key}
        r = requests.get( url, headers=headers)
        data = r.json()
        print( data)
        for result in data[ 'restaurants']:
            print( result[ 'restaurant'][ 'name'])
    return render_template( 'restaurant_search.html', title = "Restaurant Search", data = data, current_user = current_user())

@app.route( '/food_diary')
def foodDiary():
    if current_user() == None:
      flash('You must log in to access this page', 'warning')
      return redirect( url_for( 'login'))
    blog = Blog(current_user().id)
    return render_template( 'food_diary.html', title = "Food Diary", blog = blog, current_user = current_user())

@app.route( '/new_entry', methods=['GET', 'POST'])
def newEntry():
    # print(request.form)
    if current_user() == None: # have to be logged in to make an entry
      flash('You must log in to access this page', 'warning')
      return redirect( url_for( 'login'))
    if (request.form):
        entry = request.form
        date = "%s-%s-%s" % (entry['datepicker'][-4:],entry['datepicker'][:2],entry['datepicker'][3:5]) # convert string from date picker into sqlite date format
        if (Blog.check_date_taken(current_user().id,date)): # flash message to user if they put in a date that is already taken
            flash("Already an entry made for this date", "warning")
        else:
            Blog.add_entry(current_user().id, entry['breakfast'], entry['lunch'], entry['dinner'], entry['snacks'], entry['restaurant'], date)
            flash("Entry added successfully", 'success')
    return render_template('new_entry.html',title = "New Entry", current_user = current_user())


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
