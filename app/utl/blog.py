from app.utl import execute
from app.utl.user import User
import sqlite3

class Blog:
    def __init__(self, id):
        command = 'SELECT * FROM blog WHERE user_id={}'.format(id)
        data = execute(command).fetchall()
        self.id = id
        self.data = data
        self.user = User(id)

    @staticmethod
    def add_entry(user_id, breakfast, lunch, dinner, snacks, restaurant, entry_date):
        command = 'INSERT INTO blog (user_id, breakfast, lunch, dinner, snacks, restaurant, entry_date) \
                    VALUES ({}, "{}", "{}", "{}", "{}", "{}", "{}")'.format(user_id, breakfast, lunch, dinner, snacks, restaurant, entry_date)
        execute(command)
