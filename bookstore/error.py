from enum import Enum
from typing import cast


class ErrorCode(Enum):
    OK = 200
    INVENTORY_SHORTAGE = 505
    BOOK_NOT_EXIST = 506
    USER_NOT_EXIST = 507
    SHOP_NOT_EXIST = 508
    ORDER_NOT_EXIST = 509
    NO_PERMISSION = 401
    INVALID_PARAMS = 510
    INSUFFICIENT_BALANCE = 511


def message(code):
    return {
               ErrorCode.INVENTORY_SHORTAGE: '库存不足',
               ErrorCode.BOOK_NOT_EXIST: '图书不存在',
               ErrorCode.USER_NOT_EXIST: '用户不存在',
               ErrorCode.SHOP_NOT_EXIST: '商店不存在',
               ErrorCode.ORDER_NOT_EXIST: '订单不存在',
               ErrorCode.NO_PERMISSION: '权限不足',
               ErrorCode.OK: '',
               ErrorCode.INVAILD_PARAMS: '参数错误',
               ErrorCode.INSUFFICIENT_BALANCE: '余额不足',
           }[code], code
