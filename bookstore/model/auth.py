from bookstore.error import *
from bookstore.model.db_handler import *
import psycopg2
import time


class User:
    def __init__(self):
        self.db_handler = DB_handler()
        self.utils = Utils()

    def get_conn(self):
        conn = self.db_handler.db_connect()
        return conn

    # 用户注册，成功注册则返回true，注册失败则返回false
    def register(self, user_id, password):
        if self.utils.uid_check(user_id):
            return False
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            command = "INSERT INTO users (uid, pwd, balance) VALUES (%s, %s, %s)"
            cur.execute(command, (user_id, password, 0.0))
            conn.commit()
            cur.close()
            conn.close()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    # 用户注销，成功注销返回true，注销失败返回false
    def unregister(self, user_id, password):
        if not self.utils.uid_check(user_id):
            return False
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            command = "DELETE FROM users WHERE uid = %s AND pwd = %s"
            cur.execute(command, (user_id, password))
            flag = cur.rowcount
            conn.commit()
            cur.close()
            conn.close()
            if flag:
                return True
            else:
                return False
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    # 用户登录，成功登录返回token，失败返回None
    def login(self, user_id, password, terminal):
        if not self.utils.uid_check(user_id):
            return None
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            command = "UPDATE users SET terminal = %s WHERE uid = %s AND pwd = %s"
            cur.execute(command, (terminal, user_id, password))
            flag = cur.rowcount
            conn.commit()
            cur.close()
            if flag:
                # 生成token，存入数据库
                start_time = time.time()
                token = str(int(start_time))
                cur = conn.cursor()
                command = "UPDATE users SET token = %s WHERE uid = %s"
                cur.execute(command, (token, user_id))
                conn.commit()
                cur.close()
                conn.close()
                # 如何判断token是否已经失效
                return token
            else:
                return None
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    # 更改密码
    def password(self, user_id, old_password, new_password):
        if not self.utils.uid_check(user_id):
            return False
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            command = "UPDATE users SET pwd = %s WHERE uid = %s AND pwd = %s"
            cur.execute(command, (new_password, user_id, old_password))
            flag = cur.rowcount
            conn.commit()
            cur.close()
            conn.close()
            if flag:
                return True
            else:
                return False
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    # 用户登出
    def logout(self, user_id):
        if not self.utils.uid_check(user_id):
            return False
        if not self.utils.token_check(user_id):
            return False
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            command = "UPDATE users SET token=null, terminal=null WHERE UID = %s"
            cur.execute(command, (user_id, ))
            conn.commit()
            cur.close()
            conn.close()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

# if __name__ == "__main__":
#     user = User()
#     user_id = "test"
#     password = "test"
#     user.unregister("test", "test")
