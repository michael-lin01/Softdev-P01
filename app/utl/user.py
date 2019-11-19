from app.database import exececute

class User:

    def __init__(self, id):
        data = execute('SELECT * FROM `user` WHERE `user`.id=%d' % id).fetchall()
        self.id = int(data[0][0])
        self.username = data[0][1]
        self.password = data[0][2]
