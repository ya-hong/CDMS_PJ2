# 多个接口共通的功能函数

from bookstore.model.db_handler import *
import psycopg2
import time


class Utils:
    def __init__(self):
        self.db_handler = DB_handler()

    def get_conn(self):
        conn = self.db_handler.db_connect()
        return conn

    # 检查user_id是否存在
    # 存在返回True, 不存在返回False
    def uid_check(self, user_id):
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            command = "SELECT * FROM users WHERE UID = %s"
            cur.execute(command, (user_id,))
            cnt = cur.rowcount
            cur.close()
            conn.close()
            if cnt:
                return True
            else:
                return False
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    # token检测, 判断token是否失效
    # token不存在, 已超时, 均会判断为失效, 返回False
    # token存在, 返回True
    def token_check(self, user_id):
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            command = "SELECT token from users WHERE UID = %s"
            cur.execute(command, (user_id, ))
            token = cur.fetchone()[0]
            cur.close()
            conn.close()
            if token is None:
                return False
            else:
                current_time = time.time()
                if int(token) - int(current_time) > 3600:
                    return False
                else:
                    return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)