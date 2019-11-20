from app.utl import execute

class User:

    def __init__(self, id):
        data = execute('SELECT * FROM user WHERE id=%d' % id).fetchall()
        self.id = int(data[0][0])
        self.username = str(data[0][1])
        self.password = str(data[0][2])

    #checks if username exists
    @staticmethod
    def username_avaliable(username):
        command = 'SELECT id FROM user WHERE username = "{}"'.format(username)
        data = execute(command).fetchall()
        #data = execute('SELECT id FROM user WHERE username = "%s"' % username).fetchall()
        return len(data) == 0

    # add user into database
    @staticmethod
    def new_user(username, password):
        command = 'INSERT INTO user (username, password) VALUES ("{}", "{}")'.format(username, password)
        execute(command)
        #execute('INSERT INTO user (username, password) VALUES ("%s", "%s")' % (username, password)) 
    
    # get user object by username
    @staticmethod
    def get_user(username):
        command = 'SELECT id from user WHERE username = "{}"'.format(username)
        data = execute(command).fetchall()
        #data = execute('SELECT id from user WHERE username = "%s"' % username).fetchall()
        if len(data) == 0: # if no user exists with the username then return None
            return None
        else:
            return User(data[0][0]) #returns user oobject