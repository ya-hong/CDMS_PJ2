# from bookstore.classes.sql import SQL
# from bookstore.classes.model import *
# from bookstore.bp import auth
from bookstore import error
from bookstore.classes.sql import SQL

# try:
#     dic = dict()
#     dic['111']
# except KeyError as err:
#     print(err)
#     raise error.INVALID_PARAMS
# except error.INVALID_PARAMS as err:
#     print(err)

sql = SQL()
# ret = sql.transaction("SELECT * FROM users;")
# print(ret)

# ret = sql.transaction("SELECT * FROM shops;")
# print(ret)

ret = sql.transaction("SELECT quantity FROM books where book_id = '1000067' AND shop_id = 'test_new_order_store_id_70c84e5a-5c15-11ec-a0a3-00155db1fd38';")
print(ret)

# ret = sql.transaction("SELECT * FROM order_book;")
# print(ret)


# sql.transaction("DELETE FROM users;")
# sql.transaction("DELETE FROM order_book;")
# sql.transaction("DELETE FROM orders;")
# sql.transaction("DELETE FROM books;")
# sql.transaction("DELETE FROM shops;")
# sql.transaction("DELETE FROM order_book;")
# sql.transaction("DELETE FROM orders;")