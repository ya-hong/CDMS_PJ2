from _typeshed.wsgi import ErrorStream
from flask import Blueprint
from flask import request
from flask import jsonify
from bookstore import error
from bookstore.error import ErrorCode, message
from bookstore.bp import seller
import json

bp_seller = Blueprint("seller", __name__, url_prefix="/seller")


@bp_seller.route("/create_store", methods=['POST'])
def seller_create_store():
    params = request.json
    token = params['token']  ############### ToDo
    uid = params['user_id']
    shop_id = params['store_id']
    s = seller.Seller()
    message, code = s.create_store(uid, shop_id)
    return jsonify({"message": message}), code


@bp_seller.route("/add_book", methods=['POST'])
def seller_add_book():
    params = request.json
    token = params['token']  ############### ToDo
    uid = params['user_id']
    shop_id = params['store_id']
    book_info = params['book_info']
    quantity = int(params['stock_level'])
    if quantity < 0:
        message, code = error.message(ErrorCode.INPUT_NEGATIVE)
        return jsonify({"message": message}), code
    insert_key = ", ".join(['book_id', 'uid', 'shop_id', 'quantity'].extend(list(book_info.keys())[1:]))
    insert_value = tuple([book_info[id], uid, shop_id, int(quantity)].extend(list(book_info.values())[1:]))
    s = seller.Seller()
    message, code = s.add_book(uid, shop_id, insert_key, insert_value)
    return jsonify({"message": message}), code


@bp_seller.route("/add_stock_level", methods=['POST'])
def seller_add_stock_level():
    params = request.json
    token = params['token']  ############### ToDo
    uid = params['user_id']
    shop_id = params['store_id']
    book_id = params['book_id']
    offset = int(params['add_stock_level'])
    if int(offset) <= 0:
        message, code = error.message(ErrorCode.OFFSET_NOT_POSITIVE)
    else:
        s = seller.Seller()
        message, code = s.add_stock_level(uid, shop_id, book_id, offset)
    return jsonify({"message": message}), code
