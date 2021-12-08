from os import times
from flask import Blueprint
from flask import request
import flask
from flask.scaffold import _matching_loader_thinks_module_is_package
from be.model.db_handler import DB_handler 
from bookstore import error
from bookstore.error import ErrorCode



bp = Blueprint('buyer', __name__, url_prefix = "/buyer")
conn = DB_handler().db_connect()

@bp.route('/new_order', ['POST'])
def new_order():
    params = request.json
    user_id = params["user_id"]
    store_id = params["store_id"]
    books = params["books"] # {id, count}
    cur = conn.cursor()
    cur.execute("LOCK TABLE books IN ACCESS EXCLUSIVE MODE;")
    code = 200
    for book in books:
        book_id = book['id']
        buy_count = book['count']
        cur.execute("SELECT quantity FROM books WHERE book_id = ?;", [book_id])
        row = cur.fetchone()
        if row is None:
            code = ErrorCode.BOOK_NOT_EXIST
        elif row[0] < buy_count:
            code = ErrorCode.INVENTORY_SHORTAGE
        if code != 200:
            break
    if code != 200:
        cur.close()
        return error.message(code)
    cur.execute("SELECT MAX(oid) FROM orders")
    row = cur.fetchone()
    oid = 0 if row is None else row[0] + 1
    for book in books:
        book_id = book['id']
        buy_count = book['count']
        cur.execute(
            "UPDATE books SET quantity = quantity - ? "
            "WHERE book_id = ?;"
            , [buy_count, book_id])
        cur.execute(
            "INSERT INTO orders(oid, UID, SHOP_ID, BOOK_ID, ORDER_QUANTITY) "
            "VALUES(?, ?, ?, ?, ?, ?);",
            [oid, user_id, store_id, book_id, buy_count]
        )
    cur.close()
    return {'order_id': oid}, 200


@bp.route('/payment', ['POST'])
#   "user_id": "buyer_id",
#   "order_id": "order_id",
#   "password": "password"
def payment():
    params = request.json
    user_id = params['user_id']
    order_id = params['order_id']
    password = params['password']
    # TODO: 权限检查
    pass


@bp.route("/add_funds", ["POST"])
# "user_id": "user_id",
# "password": "password",
# "add_value": 10
def add_funds():
    params = request.json
    user_id = params['user_id']
    password = params['password']
    add_value = params['add_value']
    code = 200
    # TODO: 权限检查

    if add_value < 0:
        code = ErrorCode.INVAILD_PARAMS

    cur = conn.cursor()
    cur.execute("LOCK TABLE users IN ACCESS EXCLUSIVE MODE;")
    cur.execute(
        "UPDATE users SET BALANCE = BALANCE + ? "
        "WHERE uid = ?;"
        , [add_value, user_id])
    cur.close()
    return code 
