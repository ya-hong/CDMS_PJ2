import psycopg2
from flask import Blueprint
from flask import request
from bookstore import error
from bookstore import Token
from bookstore.classes.model import *


bp = Blueprint('seller', __name__, url_prefix = "/seller")


@bp.route("/create_store", methods=['POST'])
def create_store():
    try:
        params = request.json
        user_id = params['user_id']
        # password = params['password']
        shop_id = params['store_id']
        token = request.headers["token"]
    except KeyError:
        return error.INVALID_PARAMS().ret()

    if not Token.check_token(user_id, token):
        return error.NO_PERMISSION().ret()
    
    try:
        Shop.create(user_id, shop_id)
    except error.Err as err:
        return err.ret()
    return error.ok.ret()


@bp.route("/add_book", methods=['POST'])
def add_book():
    try:
        params = request.json
        user_id = params['user_id']
        # password = params['password']
        shop_id = params['store_id']
        book_info = params['book_info']
        quantity = int(params['stock_level'])
        token = request.headers["token"]
    except KeyError:
        return error.INVALID_PARAMS().ret()

    if not Token.check_token(user_id, token):
        return error.NO_PERMISSION().ret()
    
    if quantity < 0:
        raise error.INVALID_PARAMS

    try:
        Shop(shop_id).add_book(book_info, quantity)
    except error.Err as err:
        return err.ret()
    return error.ok.ret()


@bp.route("/add_stock_level", methods=['POST'])
def seller_add_stock_level():
    try:
        params = request.json
        user_id = params['user_id']
        # password = params['password']
        shop_id = params['store_id']
        book_id = params['book_id']
        offset = int(params['add_stock_level'])
        token = request.headers["token"]
    except KeyError:
        return error.INVALID_PARAMS().ret()

    try:
        if not Token.check_token(user_id, token):
            raise error.NO_PERMISSION
    
        if offset <= 0:
            raise error.INVALID_PARAMS

        Shop(shop_id).add_stock_level(book_id, offset)
    except error.Err as err:
        return err.ret()
    return error.ok.ret()


@bp.route("/delivery", methods=['POST'])
def seller_delivery():
    order_id = request.json['order_id']
    deliver_thread = orderThread