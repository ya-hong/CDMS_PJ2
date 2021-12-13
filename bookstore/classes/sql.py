"""
对数据库的封装。有两种方式使用事务:

1. SQL().transaction(string, args[])
2.  sql = SQL()  
    with sql.transaction():
        sql.execute(string, args[]) # 由于支持子事务，所以也可以直接使用 sql.transaction(string, args[])
        ...

以及一些常用功能的实现：
1. sql.insert(table, arr[], labels) # 插入数据到表table对应的列
2. sql.find_by_id(table, id) # 在表table中查询主键为id的数据的所有项目 (返回一个列表)
3. sql.check(table, id) # 查询表table中是否有主键为id的数据
"""

from bookstore.db_handler import DB_handler
import psycopg2

ID = {
    'users': 'uid',
    'shops': 'shop_id',
    'books': 'book_id',
    'orders': 'order_id',
    'order_book': 'book_id',
}


def get_id(table):
    return ID[table.lower()]


class SQL:
    def __init__(self) -> None:
        self.conn = DB_handler().db_connect()

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def transaction(self, str=None, arg=[]):
        if str is None:
            return self.conn
        if str[-1] != ';':
            str = str + ';'
        with self.conn:
            ret = self.execute(str, arg)
            return ret

    def execute(self, str, arg=[]):
        try:
            cur = self.conn.cursor()
            cur.execute(str, tuple(arg))
            if str.split()[0].lower() == 'select':
                ret = cur.fetchall()
            elif str.split()[0].lower() == 'delete' or str.split()[0].lower() == 'update':
                ret = cur.rowcount
            else:
                ret = True
        except Exception as error:
            print("数据库错误", error)
            print("查询： ", str, arg)
            raise error
        else:
            return ret

    def insert(self, table, arr, tags=""):
        values = ""
        for v in arr:
            if isinstance(v, str):
                v = "'{}'".format(v)
            else:
                v = str(v)
            if values == "":
                values = v
            else:
                values += ',' + v
        if tags != "":
            tags = "({})".format(tags)
        ret = self.transaction("INSERT INTO {} {} VALUES({});".format(table, tags, values))
        return ret

    def find_by_id(self, table, id):
        try:
            ret = self.transaction("SELECT * FROM {} WHERE {} = %s;".format(table, ID[table]), [id])
            if len(ret):
                return ret[0]
            else:
                return None
        except Exception as err:
            print("find_by_id 错误")
            print(err)
            return err

    def check(self, table, id):
        try:
            ret = self.find_by_id(table, id)
            return not ret is None
        except Exception as err:
            print(err)
            return err
