# Project MYplatE by Team willCodeForFood
# SoftDev1 pd01
# P01 -- ArRESTful Development
# 2019-11-20

import sqlite3
import random
import sys
from utl.db_builder import exec

#==========================user get methods===========================

#takes in username, returns user_id from user_tbl
def getUserID(username):
    q = "SELECT user_id FROM user_tbl WHERE username = '%s';" % username
    data = exec(q).fetchone()
    return data


#str instead of tuple output of getUserID
def getUserIDStr(username):
    user_id = getUserID(username)
    return str(user_id[0])


#takes in user_id, returns username from user_tbl
def getUserInfo(user_id):
    q = "SELECT username FROM user_tbl WHERE user_id = '%s';" % user_id
    data = exec(q).fetchone()
    return data

#returns a tuple of all blogs in blog_tbl
def getAllUsers():
    q = "SELECT username, user_id FROM user_tbl"
    data = exec(q).fetchall()
    return data

#==========================diary functions===========================


#helper function for addEntry
def addEntryHelper( user_id, title, data):
    rand = random.randrange( limit)
    while ( rand in data):
        #if the id is already in use
        rand = random.randrange( limit)
    #print(rand)
    #print(command)
    command = "INSERT INTO diary_tbl VALUES(%s, %s, '%s')" % ( rand, user_id, title)
    #print(command)
    exec( command)
    return rand

#takes in user_id/title, generates blog_id, adds them to blog_tbl, returns blog_id
def addEntry( user_id, title):
    title = title.strip()
    user_id = int( user_id)
    cmd = "SELECT * FROM blog_tbl WHERE user_id = %d AND title = '%s'" % ( user_id, title)
    data = exec( cmd).fetchone()
    if ( data is not None):
        return None
    cmd = "SELECT blog_id FROM blog_tbl WHERE user_id = %d;" % user_id
    data = exec( cmd).fetchall()
    return addEntryHelper( user_id, title, data)

