# Project MYPlatE by Team willCodeForFood
# SoftDev1 pd01
# P01 -- ArRESTful Development
# 2019-11-19


import sqlite3   #enable control of an sqlite database

#opens or creates database file
DB_FILE="food.db"

#commits the changes after a command
def execute( cmd):
    db = sqlite3.connect( DB_FILE)
    c = db.cursor()
    output = c.execute( cmd)
    db.commit()
    return output

#==========================================================
#creates tables if they do not exist with necessary columns
def build_db():
    # execute('DROP TABLE IF EXISTS user')
    # execute('DROP TABLE IF EXISTS blog')

    command = "CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, username TEXT, password BLOB)"
    execute(command)    # run SQL statement

    command = "CREATE TABLE IF NOT EXISTS blog (user_id INT, breakfast TEXT, lunch TEXT, dinner TEXT, snacks TEXT, restaurant TEXT, entry_date DATE)"
    execute(command)    # run SQL statement
    