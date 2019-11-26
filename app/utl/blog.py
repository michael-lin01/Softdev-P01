from app.utl import execute
from app.utl import User

class Blog:
    def __init__(self, id):
        command = 'SELECT * FROM blog WHERE user_id={}'.format(id)
        data = execute(command).fetchall()
        self.id = int(data[0][0])
        self.user = User(id)

    @staticmethod
    def add_entry(user_id, content, entryDate):
        command = 'INSERT INTO blog (user_id, content, entryDate) \
                    VALUES ({}, "{}", "{}")'.format(user_id, content, entryDate)
        execute(command)
