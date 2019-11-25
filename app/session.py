from flask import session, redirect, flash, request

from app.utl.user import User


# get current logged in user
def current_user():
    if 'user_id' in session:
        return User(session['user_id'])
    return None


# login a user
# usr is a User object
def login_user(usr):
    session['user_id'] = usr.id

# clear session
def logout_user():
    session.clear()
