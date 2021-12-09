from configparser import Error
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
    INVAILD_PARAMS = 510
    INSUFFICIENT_BALANCE = 511

    SHOP_HAS_EXISTED = 580
    BOOK_HAS_EXISTED = 581
    USER_HAS_EXISTED = 582
    BASE_EXCEPTION_OCCURED = 583
    OFFSET_NOT_POSITIVE = 584
    INPUT_NEGATIVE = 585

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
               ErrorCode.SHOP_HAS_EXISTED: '商店已存在',
               
               ErrorCode.BOOK_HAS_EXISTED: '图书已存在',
               ErrorCode.USER_HAS_EXISTED: '用户已存在',
               ErrorCode.BASE_EXCEPTION_OCCURED: '数据库连接出错',
               ErrorCode.INPUT_NEGATIVE: '输入为负数',
               ErrorCode.OFFSET_NOT_POSITIVE: '增量非正',
           }[code], code


def check_uid_existence(cur, uid):
    try:
        cur.execute("begin;")
        cur.execute("LOCK TABLE users IN EXCLUSIVE MODE;")
        cur.execute("SELECT uid FROM users WHERE uid = ?;", (uid))
        row = cur.fetchone()
        cur.excute("end;")
        if row is not None:
            return ErrorCode.USER_HAS_EXISTED
        else:
            return ErrorCode.USER_NOT_EXIST
    except BaseException as e:
        print("{}".format(str(e)))
        return ErrorCode.BASE_EXCEPTION_OCCURED


def check_shop_id_existence(cur, shop_id):
    try:
        cur.execute("begin;")
        cur.execute("LOCK TABLE shops IN EXCLUSIVE MODE;")
        cur.execute("SELECT shop_id FROM shops WHERE uid = ?;", (shop_id))
        row = cur.fetchone()
        cur.excute("end;")
        if row is not None:
            return ErrorCode.SHOP_HAS_EXISTED
        else:
            return ErrorCode.SHOP_NOT_EXIST
    except BaseException as e:
        print("{}".format(str(e)))
        return ErrorCode.BASE_EXCEPTION_OCCURED


def check_book_existence(cur, book_id):
    try:
        cur.execute("begin;")
        cur.execute("LOCK TABLE books IN EXCLUSIVE MODE;")
        cur.execute("SELECT book_id FROM books WHERE uid = ?;", (book_id))
        row = cur.fetchone()
        cur.excute("end;")
        if row is not None:
            return ErrorCode.BOOK_HAS_EXISTED
        else:
            return ErrorCode.BOOK_NOT_EXIST
    except BaseException as e:
        print("{}".format(str(e)))
        return ErrorCode.BASE_EXCEPTION_OCCURED


def check_order_existence(cur, order_id):
    try:
        cur.execute("begin;")
        cur.execute("LOCK TABLE orders IN EXCLUSIVE MODE;")
        cur.execute("SELECT order_id FROM orders WHERE uid = ?;", (order_id))
        row = cur.fetchone()
        cur.excute("end;")
        if row is not None:
            return ErrorCode.OK
        else:
            return ErrorCode.ORDER_NOT_EXIST
    except BaseException as e:
        print("{}".format(str(e)))
        return ErrorCode.BASE_EXCEPTION_OCCURED