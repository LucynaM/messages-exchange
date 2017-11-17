from clcrypto import *



class User:
    __id = None
    username = None
    __hashed_password = None
    __email = None

    def __init__(self):
        self.__id = -1
        self.username = ""
        self.__hashed_password = ""
        self.__email = ""


    @property
    def id(self):
        return self.__id

    @property
    def email(self):
        return self.__email

    def set_email(self):
        if self.username:
            self.__email = self.username + "@test.pl"

    @property
    def hashed_password(self):
        return self.__hashed_password

    def set_password(self, password, salt):
        self.__hashed_password = password_hash(password, salt)


    def save_to_db(self, cursor):
        if self.__id == -1:
            sql = """INSERT INTO Users(username, email, hashed_password) 
            VALUES(%s, %s, %s)
            """
            values = (self.username, self.email, self.hashed_password)
            cursor.execute(sql, values)
            self.__id = cursor.lastrowid
            return True
        else:
            sql = "UPDATE Users SET username=%s, email=%s, hashed_password=%s WHERE id={}".format(self.id)
            values = (self.username, self.email, self.hashed_password)
            # print("sql", sql)
            cursor.execute(sql, values)
            return True


    @staticmethod
    def load_user_by_login(cursor,	login):
        sql = "SELECT id, username, email, hashed_password FROM Users WHERE username=%s"
        result = cursor.execute(sql, (login, ))
        data = cursor.fetchone()
        #print(data)
        if data is not None:
            loaded_user = User()
            loaded_user.__id = data[0]
            loaded_user.username = data[1]
            loaded_user.__email = data[2]
            loaded_user.__hashed_password = data[3]
            return loaded_user
        else:
            return None

    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT id, username, email, hashed_password FROM Users"
        ret = []
        result = cursor.execute(sql)
        data = cursor.fetchall()
        #print(data)

        for row in data:
            loaded_user = User()
            loaded_user.__id = row[0]
            loaded_user.username = row[1]
            loaded_user.__email = row[2]
            loaded_user.__hashed_password = row[3]
            ret.append(loaded_user)
        return ret

    def delete(self, cursor):
        sql = "DELETE FROM Users WHERE id=%s"
        cursor.execute(sql, (self.__id, ))
        self.__id = -1
        return True



