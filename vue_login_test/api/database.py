import datetime
import sqlite3


# This class is a simple handler for all of our SQL database actions
# Practicing a good separation of concerns, we should only ever call
# These functions from our models

# If you notice anything out of place here, consider it to your advantage and don't spoil the surprise


class SQLDatabase():

    # Get the database running
    def __init__(self, database_arg="test_db.db"):
        self.conn = sqlite3.connect(database_arg, check_same_thread=False)
        self.cur = self.conn.cursor()

    def execute(self, sql_string, params=tuple()):
        out = None
        for string in sql_string.split(";"):
            try:
                out = self.cur.execute(string, params)
            except Exception as e:
                print(e, "\nwhen executing:\n", sql_string)
        return out

    def fetchall(self, sqltext, params=tuple()):
        result = []
        try:
            self.cur.execute(sqltext, params)
        except sqlite3.Warning as e:
            print("sqlite3.Warning:", e, "Nice try!")
        if (self.cur.description != None):
            cols = [a[0] for a in self.cur.description]
        returnres = self.cur.fetchall()
        for row in returnres:
            result.append({a: b for a, b in zip(cols, row)})
        return result

    def fetchone(self, sqltext, params=tuple()):
        result = []
        try:
            self.cur.execute(sqltext, params)
        except sqlite3.Warning as e:
            print("sqlite3.Warning:", e, "Nice try!")
        if (self.cur.description != None):
            cols = [a[0] for a in self.cur.description]
        returnres = self.cur.fetchone()
        if (returnres != None):
            result.append({a: b for a, b in zip(cols, returnres)})
        return result

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.cur.close()
        self.conn.close()

    # -----------------------------------------------------------------------------
    # Sets up the database
    def database_setup(self):
        # Clear the database if needed

        # Create the users tables
        # Users table contains the id, username and password

        # self.execute("DROP TABLE IF EXISTS Users")
        # self.commit()
        self.execute("""
        CREATE TABLE IF NOT EXISTS Users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT NOT NULL,
            salt INTEGER NOT NULL,
            pk TEXT,
            friend TEXT,
            if_admin INTEGER NOT NULL,
            if_mute INTEGER NOT NULL
            
        );
        """)

        self.commit()
        # self.execute("INSERT INTO Users VALUES (0, 'admin', '9b95b770e87c7fdb74746ceb37b12e99', '720991', NULL, NULL, 1, 0)")
        # self.commit()

        # Chat
        self.execute("DROP TABLE IF EXISTS Chat")
        self.commit()
        self.execute("""
                CREATE TABLE IF NOT EXISTS Chat(
                    from_username TEXT NOT NULL,
                    to_username TEXT NOT NULL,
                    message TEXT NOT NULL
                );
                """)
        self.commit()
        # 默认历史记录
        # sql_cmd = "INSERT INTO Chat VALUES (?, ?, ?)"
        # self.execute(sql_cmd, ('user1', 'user2', 'hi',))
        # self.commit()
        # sql_cmd = "INSERT INTO Chat VALUES (?, ?, ?)"
        # self.execute(sql_cmd, ('user2', 'user1', 'Hi',))
        # self.commit()
        # sql_cmd = "INSERT INTO Chat VALUES (?, ?, ?)"
        # self.execute(sql_cmd, ('user2', 'user1', 'How are you?',))
        # self.commit()

        # Question
        self.execute("DROP TABLE IF EXISTS Question")
        self.commit()
        self.execute("""
                CREATE TABLE IF NOT EXISTS Question(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    if_private INTEGER NOT NULL,
                    provider TEXT NOT NULL
                );
                """)
        self.commit()

        # Comment
        self.execute("DROP TABLE IF EXISTS Comment")
        self.commit()
        self.execute("""
                        CREATE TABLE IF NOT EXISTS Comment(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            qid INTEGER NOT NULL REFERENCES Question(id),
                            answer TEXT NOT NULL,
                            user TEXT NOT NULL REFERENCES User(username)
                        );
                        """)
        self.commit()

        self.add_question('Testing', 'I am currently testing the forum function', 0, 'admin')

        # File
        self.execute("DROP TABLE IF EXISTS File")
        self.commit()
        self.execute("""
                                CREATE TABLE IF NOT EXISTS File(
                                    name TEXT NOT NULL,
                                    title TEXT NOT NULL,
                                    url TEXT NOT NULL,
                                    user TEXT NOT NULL,
                                    format TEXT NOT NULL
                                );
                                """)
        self.commit()

    # Add a user to the database
    def add_user(self, username, password, salt, pk):
        sql_cmd = "INSERT INTO Users VALUES (NULL, ?, ?, ?, ?, ?, 0, 0)"
        out = self.execute(sql_cmd, (username, password, salt, pk, ''))
        self.commit()
        if out is not None:
            return True
        else:
            return False

    # Check login credentials
    def check_credentials(self, username):
        sql_query = """
                SELECT id, password, salt, if_mute
                FROM Users
                WHERE username = ?
            """
        result = self.fetchone(sql_query, (username,))
        self.commit()
        return result
        # if result:
        #     id = result[0]["id"]
        #     admin = result[0]["admin"]
        #     if admin == 1:
        #         return id, True
        #     return id, False
        # else:
        #     return None, False

    def get_publicKey(self, username):
        sql_query = """
                                SELECT pk
                                FROM Users
                                WHERE username = ?
                            """
        pk = self.fetchone(sql_query, (username,))
        self.commit()

        if len(pk) != 0:
            pk = pk[0].get('pk')
            return pk
        else:
            return None

    def get_friends(self, username):
        sql_query = """
                        SELECT friend
                        FROM Users
                        WHERE username = ?
                    """
        ls = self.fetchone(sql_query, (username,))
        self.commit()
        if len(ls) != 0:
            friend = ls[0].get('friend')
        else:
            return None

        result = {
            'friend': friend
        }
        return result

    def get_chat(self, username, friendname):

        sql_query = """
                        SELECT from_username, to_username, message
                        FROM Chat
                        WHERE (from_username = ? 
                        AND to_username = ?)
                        OR (from_username = ? 
                        AND to_username = ?)
                    """
        chat = self.fetchall(sql_query, (username, friendname, friendname, username,))
        self.commit()

        return chat

    def add_chat(self, from_username, to_username, message):
        sql_cmd = "INSERT INTO Chat VALUES (?, ?, ?)"
        self.execute(sql_cmd, (from_username, to_username, message,))
        self.commit()

        return

    def add_friend(self, username, friendname):
        sql_query = """
                                SELECT username
                                FROM Users
                                WHERE username = ?
                            """
        ls = self.fetchone(sql_query, (friendname,))
        self.commit()
        if len(ls) != 0:
            # 给自己添加新好友
            friend = ls[0].get('username')
            sql_query = """
                                            SELECT friend
                                            FROM Users
                                            WHERE username = ?
                                        """
            friends_ls = self.fetchone(sql_query, (username,))
            friends_ls = friends_ls[0].get('friend')

            sql_cmd = "UPDATE Users SET friend = ? WHERE username = ?"
            if friends_ls != '':
                friends_ls += ';' + friend
            else:
                friends_ls += friend
            self.execute(sql_cmd, (friends_ls, username))
            self.commit()

            # 给好友添加自己
            sql_query = """
                        SELECT friend
                        FROM Users
                        WHERE username = ?
                        """
            _friends_ls = self.fetchone(sql_query, (friend,))
            _friends_ls = _friends_ls[0].get('friend')

            sql_cmd = "UPDATE Users SET friend = ? WHERE username = ?"
            if _friends_ls != '':
                _friends_ls += ';' + username
            else:
                _friends_ls += username
            self.execute(sql_cmd, (_friends_ls, friendname))
            self.commit()
            return True
        else:
            return False

    def add_question(self, title, description, private, provider):
        sql_cmd = "INSERT INTO Question VALUES (NULL, ?, ?, ?, ?)"
        self.execute(sql_cmd, (title, description, private, provider,))
        self.commit()
        return self.fetchone('select max(id) from Question')

    def get_question(self):
        sql_query = """
                        SELECT *
                        FROM Question
                    """
        question = self.fetchall(sql_query, )
        self.commit()

        return question

    def add_comment(self, qid, answer, user):
        sql_cmd = "INSERT INTO Comment VALUES (NULL, ?, ?, ?)"
        self.execute(sql_cmd, (qid, answer, user,))
        self.commit()
        return self.fetchone('select max(id) from Comment')

    def get_comment(self, qid):
        sql_query = """
                        SELECT *
                        FROM Comment
                        where qid = ?
                    """
        comment = self.fetchall(sql_query, (qid,))
        self.commit()
        print(comment)

        return comment

    def add_file(self, filename, title, url, username, format):
        sql_cmd = "INSERT INTO File VALUES (?, ?, ?, ?, ?)"
        self.execute(sql_cmd, (filename, title, url, username, format,))
        self.commit()
        return True

    def get_file(self):
        sql_query = """
                        SELECT *
                        FROM File
                    """
        file = self.fetchall(sql_query, )
        self.commit()

        return file

    def get_user(self):
        sql_query = """
                        SELECT id, username, if_mute
                        FROM Users
                        WHERE if_admin = 0
                    """
        user = self.fetchall(sql_query, )
        self.commit()

        return user
