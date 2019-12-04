from app.utl import execute
from app.utl.user import User
import sqlite3

class Blog:
    def __init__(self, id, date=None):
        if (date):
            command = 'SELECT * FROM blog WHERE user_id={} AND entry_date="{}"'.format(id,date)
        else: 
            command = 'SELECT * FROM blog WHERE user_id={} ORDER BY entry_date'.format(id)
        data = execute(command).fetchall()
        self.id = id
        self.data = data
        self.user = User(id)

    @staticmethod
    def add_entry(user_id, breakfast, lunch, dinner, snacks, restaurant, entry_date):
        command = 'INSERT INTO blog (user_id, breakfast, lunch, dinner, snacks, restaurant, entry_date) \
            VALUES ({}, "{}", "{}", "{}", "{}", "{}", "{}")'.format(user_id, breakfast, lunch, dinner, snacks, restaurant, entry_date)
        execute(command)
    
    @staticmethod
    def edit_entry(user_id, breakfast, lunch, dinner, snacks, restaurant, entry_date):
        command = 'UPDATE blog \
                    SET breakfast =  "{}", lunch = "{}", dinner = "{}", snacks = "{}", restaurant = "{}" \
                    WHERE user_id = {} AND entry_date = "{}"'.format(breakfast,lunch,dinner,snacks,restaurant,user_id,entry_date)
        execute(command)
    @staticmethod
    def check_date_taken(user_id, entry_date):
        command = 'SELECT * FROM blog WHERE user_id=%s AND entry_date="%s"' % (user_id, entry_date)
        data = execute(command).fetchall()
        return len(data) > 0