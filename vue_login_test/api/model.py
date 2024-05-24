# Check login credentials
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
import random
import database

db = database.SQLDatabase()
db.database_setup()


def check_credentials(username):
    # m = hashlib.md5()
    # m.update(password.encode('utf-8'))
    # encrypted = m.hexdigest()
    result = db.check_credentials(username)
    # yes: [{id: 1}]
    # no: []
    if len(result) == 0:
        return -1
    return result


def register(username, password, pk):
    m = hashlib.md5()
    salt = str(random.randint(0, 999999))
    m.update((password + salt).encode('utf-8'))
    encrypted = m.hexdigest()

    # if username == 'user1':
    #     friend = 'user2'
    # elif username == 'user2':
    #     friend = 'user1'

    # True or False
    print(password, encrypted, salt)
    return db.add_user(username, encrypted, salt, pk)


def get_friend(username):
    friends = db.get_friends(username)
    print("model get friend", friends)
    return friends


def get_publicKey(username):
    publicKey = db.get_publicKey(username)
    print("model get friend's public key", publicKey)
    return publicKey


def get_chat(username, friendname):
    chat = db.get_chat(username, friendname)
    print("model get chat", chat)
    return chat


def add_chat(username, friendname, message):
    return db.add_chat(username, friendname, message)


def add_friend(username, friendname):
    return db.add_friend(username, friendname)


def add_question(title, description, provider, private):
    if_private = 0
    if private:
        if_private = 1
    result = db.add_question(title, description, if_private, provider)
    if len(result) != 1:
        return False
    else:
        return result[0].get('max(id)')


def get_question():
    question = db.get_question()
    print("model get question", question)
    return question


def add_comment(qid, answer, user):
    result = db.add_comment(qid, answer, user)
    if len(result) != 1:
        return False
    else:
        return result[0].get('max(id)')


def get_comment(qid):
    comment = db.get_comment(qid)
    print("model get comment", comment)
    return comment


def add_file(filename, title, url, username, format):
    result = db.add_file(filename, title, url, username, format)
    return result


def get_file():
    file = db.get_file()
    print("model get file", file)
    return file


def get_user():
    user = db.get_user()
    return user
