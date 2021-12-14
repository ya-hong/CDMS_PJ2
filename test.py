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
ret = sql.transaction("""SELECT title FROM books WHERE content LIKE '%%，%%';""")
print(ret)