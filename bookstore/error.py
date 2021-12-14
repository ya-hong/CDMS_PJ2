""""
包含错误码以及描述。
post接口返回 Err().ret() 即可返回错误。
若要生成特定的错误描述，使用Err({'message':'xxx'})
"""

from flask import jsonify, make_response
from bookstore import classes
from enum import Enum


class OrderState(Enum):
    UNPAID = 0,
    UNDELIVERED = 1,
    DELIVERED = 2,
    COMPLETED = 3,
    AUTO_CANCEL = 4,
    BUYER_CANCEL = 5


class Err(Exception):
    code = 501
    msg = "未知错误"

    def __init__(self, dic={}) -> None:
        self.message = {
            'message': self.msg
        } 
        self.message = {**self.message, **dic}
        super().__init__(self.msg)

    def ret(self):
        return make_response(jsonify(self.message), self.code) 


class OK(Err):
    code = 200
    msg = 'ok'


class INVENTORY_SHORTAGE(Err):
    code = 502
    msg = "库存不足"


class NO_USER(Err):
    code = 503
    msg = '用户ID不存在'


class NO_BUYER(Err):
    code = 504
    msg = '买家用户ID不存在'


class NO_SELLER(Err):
    code = 505
    msg = '卖家用户ID不存在'


class INVALID_PARAMS(Err):
    code = 506
    msg = '参数错误'


class DUPLICATE_USERID(Err):
    code = 507
    msg = '用户名重复'


class UNREGISTER_FAILED(Err):
    code = 508
    msg = '注销失败，用户名不存在或密码不正确'


class NO_PERMISSION(Err):
    code = 401
    # 可以用 NO_PERMISSION({'message': 'xx'}) 来指定特定类型的权限错误


class NO_SHOP(Err):
    code = 509
    msg = '商铺ID不存在'


class NO_BOOK(Err):
    code = 510
    msg = '购买的图书不存在'


class INSUFFICIENT_BALANCE(Err):
    code = 511
    msg = '账户余额不足'


class DUPLICATE_SHOPID(Err):
    code = 512
    msg = '商铺ID已存在'


class DUPLICATE_BOOKID(Err):
    code = 513
    msg = '图书ID已存在'


ok = OK()