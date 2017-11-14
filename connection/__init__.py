from connect_to_db import connect_to_db
from mysql.connector import connect, ProgrammingError

def mysql_connection(func, *args, **kwargs):
    conn, cur = None, None
    try:
        conn = connect_to_db("workshop2_db")
        cur = conn.cursor()
        return func(cur, *args, **kwargs)
    except ProgrammingError as e:
        print(e)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()