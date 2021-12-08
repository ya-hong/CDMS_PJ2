from be.model.db_handler import *
import psycopg2


class User:
    def __init__(self):
        self.db_handler = DB_handler()

    def get_conn(self):
        conn = self.db_handler.db_connect()
        return conn

    def check_uid(self, user_id):
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            command = "SELECT * FROM users WHERE user_id = %s"
            cur.execute(command, (user_id,))
            row_num = cur.rowcount

            if row_num != 0:
                return True
            else:
                return False

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    # def register(self, user_id, password):

