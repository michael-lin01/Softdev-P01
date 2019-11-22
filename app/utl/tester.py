# Project MYplatE by Team willCodeForFood
# SoftDev1 pd01
# P01 -- ArRESTful Development
# 2019-11-20

import sqlite3
import random
import sys
from utl.db_builder import exec

#==========================diary functions===========================

#helper function for addEntry
def addEntryHelper( user_id, title, data):
    rand = random.randrange( limit)
    while ( rand in data):
        #if the id is already in use
        rand = random.randrange( limit)
    #print(rand)
    #print(command)
    command = "INSERT INTO blog_tbl VALUES(%s, %s, '%s')" % ( rand, user_id, title)
    #print(command)
    exec( command)
    return rand

#takes in user_id/title, generates blog_id, adds them to blog_tbl, returns blog_id
def addEntry( user_id, title):
    title = title.strip()
    user_id = int( user_id)
    cmd = "SELECT * FROM blog_tbl WHERE user_id = %d AND title = '%s'" % (user_id, title)
    data = exec( cmd).fetchone()
    if (data is not None):
        return None
    cmd = "SELECT blog_id FROM blog_tbl WHERE user_id = %d;" % user_id
    data = exec( cmd).fetchall()
    return addEntryHelper( user_id, title, data)

