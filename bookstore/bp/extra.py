from flask import Blueprint
from flask import request
from bookstore import error
from bookstore import Token
from bookstore.classes import searcher
from pprint import pprint


bp = Blueprint('extra', __name__, url_prefix = "/extra")


@bp.route('/search', methods=['POST'])
def search():
    try:
        params = request.json
        print(params)
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