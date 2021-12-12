from bookstore.model.db_handler import DB_handler
from bookstore.error import *
import psycopg2


class foo_exception(Exception):
    def __init__(self, msg):
        self.args = msg

    def __str__(self):
        return self.args


class Seller:
    def __init__(self):
        self.conn = None

    def create_store(self, uid, shop_id):
        self.conn = DB_handler().db_connect()
        cur = self.conn.cursor()
        code = ErrorCode.OK
        try:
            check_code = check_uid_existence(cur, uid)
            if check_code == ErrorCode.USER_NOT_EXIST:
                raise foo_exception(check_code)
            check_code = check_shop_id_existence(cur, shop_id)
            if check_code == ErrorCode.SHOP_HAS_EXISTED:
                raise foo_exception(check_code)
            cur.execute("begin;")
            cur.execute("LOCK TABLE shops IN ACCESS EXCLUSIVE MODE;")
            cur.execute("INSERT INTO shops(shop_id, uid) VALUES(?, ?);", (shop_id, uid));
            cur.execute("END;")
        except psycopg2.DatabaseError as e:
            print("{}".format(str(e)))
            code = ErrorCode.DATA_BASE_ERROR
        except foo_exception as e:
            code = int(e)
        cur.close()
        self.conn.commit()
        self.conn.close()
        return message(code)

    def add_book(self, uid, shop_id, key, value):
        book_id = value[0]
        padding = ', '.join(['?' for i in range(len(value))])
        self.conn = DB_handler().db_connect()
        cur = self.conn.cursor()
        code = ErrorCode.OK
        try:
            check_code = check_uid_existence(cur, uid)
            if check_code == ErrorCode.USER_NOT_EXIST:
                raise foo_exception(check_code)
            check_code = check_shop_id_existence(cur, shop_id)
            if check_code == ErrorCode.SHOP_NOT_EXIST:
                raise foo_exception(check_code)
            check_code = check_book_existence(cur, book_id)
            if check_code == ErrorCode.BOOK_HAS_EXISTED:
                raise foo_exception(check_code)
            cur.execute("begin;")
            cur.execute("LOCK TABLE books IN ACCESS EXCLUSIVE MODE;")
            query = "INSERT INTO books(?) VALUES(" + padding + ");"
            cur.execute(query, (key, value));
            cur.execute("END;")
        except psycopg2.DatabaseError as e:
            print("{}".format(str(e)))
            code = ErrorCode.DATA_BASE_ERROR
        except foo_exception as e:
            code = int(e)
        cur.close()
        self.conn.commit()
        self.conn.close()
        return message(code)

    def add_stock_level(self, uid, shop_id, book_id, offset):
        self.conn = DB_handler().db_connect()
        cur = self.conn.cursor()
        code = ErrorCode.OK
        try:
            check_code = check_uid_existence(cur, uid)
            if check_code == ErrorCode.USER_NOT_EXIST:
                raise foo_exception(check_code)
            check_code = check_shop_id_existence(cur, shop_id)
            if check_code == ErrorCode.SHOP_NOT_EXIST:
                raise foo_exception(check_code)
            if check_code == ErrorCode.BOOK_NOT_EXIST:
                raise foo_exception(check_code)
            cur.execute("begin;")
            cur.execute("LOCK TABLE books IN ACCESS EXCLUSIVE MODE;")
            cur.execute('UPDATE books SET QUANTITY = QUANTITY - ? \
                        WHERE shop_id = ? AND book_id = ?;', (offset, shop_id, book_id))
            cur.execute("end;")
        except psycopg2.DatabaseError as e:
            print("{}".format(str(e)))
            code = ErrorCode.DATA_BASE_ERROR
        except foo_exception as e:
            code = int(e)
        cur.close()
        self.conn.commit()
        self.conn.close()
        return message(code.value)


s = Seller()
s.add_book()
