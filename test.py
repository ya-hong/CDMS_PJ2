from os import error
from bookstore.classes.sql import SQL
from bookstore.classes.model import *
from bookstore.bp import auth


sql = SQL()
ret = sql.transaction("SELECT * FROM users;")
print(ret)