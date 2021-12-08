from enum import Enum
from typing import cast

class ErrorCode(Enum):
    INVENTORY_SHORTAGE = 505
    BOOK_NOT_EXIST = 506
    USER_NOT_EXIST = 507
    SHOP_NOT_EXIST = 508
    ORDER_NOT_EXIST = 509
    NO_PERMISSION = 401
    INVAILD_PARAMS = 510

def message(code):
    return {
        ErrorCode.INVENTORY_SHORTAGE: '库存不足',
        ErrorCode.BOOK_NOT_EXIST: '图书不存在',
        ErrorCode.USER_NOT_EXIST: '用户不存在',
        ErrorCode.SHOP_NOT_EXIST: '商店不存在',
        ErrorCode.ORDER_NOT_EXIST: '订单不存在',
        ErrorCode.INVAILD: '授权失败',
    }[code], code