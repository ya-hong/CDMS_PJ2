from os import error
from bookstore.classes.sql import SQL
from bookstore.classes.model import *
from bookstore.bp import auth


sql = SQL()
ret = sql.transaction("SELECT * FROM users;")
print(ret)

ret = sql.transaction("SELECT * FROM shops;")
print(ret)

ret = sql.transaction("SELECT * FROM books;")
print(ret)

ret = sql.transaction("SELECT * FROM order_book;")
print(ret)


# sql.transaction("DELETE FROM order_book;")
# sql.transaction("DELETE FROM orders;")