# Project MYPlatE by Team willCodeForFood
# SoftDev1 pd01
# P01 -- ArRESTful Development
# 2019-11-19


import sqlite3   #enable control of an sqlite database

#opens or creates database file
DB_FILE="food.db"

#commits the changes after a command
def exec(cmd):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    output = c.execute(cmd)
    db.commit()
    return output

#==========================================================
#creates tables if they do not exist with necessary columns
def build_db():
    command = "CREATE TABLE IF NOT EXISTS user_tbl (id INT, username TEXT, password BLOB)"
    exec(command)    # run SQL statement

    command = "CREATE TABLE IF NOT EXISTS blog_tbl (user_id INT, entryContent TEXT, entryDate TEXT)"
    exec(command)    # run SQL statement

    command = "CREATE TABLE IF NOT EXISTS blog_tbl (query INT, response TEXTT)"
    exec(command)    # run SQL statement

    
