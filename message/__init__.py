
from datetime import date
from connection import mysql_connection

class Message:
    __id = None
    from_usr = None
    to_usr = None
    text = None
    __date = None


    def __init__(self):
        self.__id = -1
        self.from_usr = None
        self.to_usr = None
        self.text = ""
        self.__date = None

    @property
    def id(self):
        return self.__id

    @property
    def date(self):
        return self.__date

    def set_date(self):
        self.__date = date.today()

    def save_to_db(self, cursor):
        if self.__id == -1:
            sql = """INSERT INTO Messages(from_usr, to_usr, text, creation_date) 
               VALUES(%s, %s, %s, %s)
               """
            values = (self.from_usr, self.to_usr, self.text, self.date)
            cursor.execute(sql, values)
            self.__id = cursor.lastrowid
            return True

    @staticmethod
    def load_msg_by_id(cursor, id):
        sql = "SELECT id, from_usr, to_usr, text, creation_date FROM Messages WHERE id=%s"
        result = cursor.execute(sql, (id,))
        data = cursor.fetchone()
        # print(data)
        if data is not None:
            loaded_msg = Message()
            loaded_msg.__id = data[0]
            loaded_msg.from_usr = data[1]
            loaded_msg.to_usr = data[2]
            loaded_msg.text = data[3]
            loaded_msg.__date = data[4]
            return loaded_msg
        else:
            return None

    @staticmethod
    def load_all_msg(cursor):
        sql = "SELECT id, from_usr, to_usr, text, creation_date FROM Messages"
        ret = []
        result = cursor.execute(sql)
        data = cursor.fetchall()
        # print(data)

        for row in data:
            loaded_msg = Message()
            loaded_msg.__id = row[0]
            loaded_msg.from_usr = row[1]
            loaded_msg.to_usr = row[2]
            loaded_msg.text = row[3]
            loaded_msg.__date = row[4]
            ret.append(loaded_msg)
        return ret

    @staticmethod
    def load_all_msg_for_user(cursor, usr_id):
        sql = "SELECT id, from_usr, to_usr, text, creation_date FROM Messages WHERE to_usr=%s ORDER BY creation_date"
        ret = []
        result = cursor.execute(sql, (usr_id,))
        data = cursor.fetchall()
        # print(data)

        for row in data:
            loaded_msg = Message()
            loaded_msg.__id = row[0]
            loaded_msg.from_usr = row[1]
            loaded_msg.to_usr = row[2]
            loaded_msg.text = row[3]
            loaded_msg.__date = row[4]
            ret.append(loaded_msg)
        return ret
