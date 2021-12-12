from flask import Blueprint
from flask import request
from bookstore import error
from bookstore import Token
from bookstore.classes.model import *
from bookstore.classes.sql import SQL


bp = Blueprint('buyer', __name__, url_prefix = "/buyer")


@bp.route('/new_order', methods=['POST'])
def new_order():
    params = request.json
    user_id = params["user_id"]
    store_id = params["store_id"]
    books = params["books"] # {id, count}
    # token = request.headers["token"]

    # if not Token.check_token(token):
    #     pass 

    try:
        user = User(user_id)
        user.new_order(Shop(store_id), books)
    except error.Err as err:
        print(err)
        return err.ret()

    return error.ok.ret()


@bp.route('/payment', methods = ['POST'])
#   "user_id": "buyer_id",
#   "order_id": "order_id",
#   "password": "password"
def payment():
    params = request.json
    user_id = params['user_id']
    order_id = params['order_id']
    password = params['password']
    token = request.headers["token"]

    if not Token.check_token(token):
        pass 
    try:
        User(user_id).payment(Order(order_id))
    except error.Err as err:
        return err.ret()
    return error.ok.ret()

@bp.route("/add_funds", methods = ["POST"])
# "user_id": "user_id",
# "password": "password",
# "add_value": 10
def add_funds():
    params = request.json
    user_id = params['user_id']
    password = params['password']
    add_value = params['add_value']
    token = request.headers["token"]

    if not Token.check_token(token):
            pass 
    
    if add_value < 0:
        return error.INVAILD_PARAMS.ret()

    try:
        User(user_id).add_funds(add_value)
    except error.Err as err:
        return err.ret()
    return error.ok.ret()