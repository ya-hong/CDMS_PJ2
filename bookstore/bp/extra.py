from configparser import Error
from flask import Blueprint
from flask import request
from bookstore import error
from bookstore import Token
from bookstore.classes import searcher
from pprint import pprint
from bookstore.classes.order import Order

from bookstore.classes.user import User


bp = Blueprint('extra', __name__, url_prefix = "/extra")


@bp.route('/search', methods=['POST'])
def search():
    try:
        params = request.json
        title = params.get('title') or []
        tags = params.get("tags") or []
        content = params.get("content") or []
        shop_id = params.get("shop_id")
        page_num = params['page_num']
    except KeyError:
        return error.INVALID_PARAMS().ret()
    
    try:
        ret = searcher.search(page_num, title, tags, content, shop_id)
        pprint(ret)
    except error.Err as err:
        print(err)
        return err.ret()
    return error.OK({'books': ret}).ret()


@bp.route('/history', methods=['POST'])
def history():
    try:
        params = request.json
        user_id = params['user_id']
        token = request.headers["token"]
    except KeyError:
        return error.INVALID_PARAMS().ret()
    
    if not Token.check_token(user_id, token):
        return error.NO_PERMISSION().ret()

    try:
        user = User(user_id)
        orders = user.history()
    except error.Err as err:
        return err.ret()
    return error.OK({'orders': orders}).ret()



@bp.route('/cancel_order', methods=['POST'])
def cancel_order():
    try:
        params = request.json
        user_id = params['user_id']
        order_id = params['order_id']
        password = params['password']
    except KeyError:
        return error.INVALID_PARAMS().ret()
    try:
        user = User(user_id)
        user.fetch()
        if user.pwd != password:
            raise error.NO_PERMISSION({'message': "密码错误"})
        user.cancel(Order(order_id))
    except error.Err as err:
        return err.ret()
    return error.ok.ret()