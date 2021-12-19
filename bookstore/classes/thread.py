import threading
import time
from bookstore.db_handler import DB_handler
from bookstore.classes.sql import SQL
from bookstore import error


sleep_time = 5 * 60


class orderThread(threading.Thread):
    def __init__(self, order_id):
        threading.Thread.__init__(self)

    def time_check(self):
        sql = SQL()
        threading.Lock.acquire()
        ret = sql.transaction("SELECT current_time, shop_id FROM orders WHERE order_id = %s;", [self.order_id])
        if ret[0] != error.OrderState.UNPAID.value[0]:
            return
        shop_id = ret[1]
        sql.transaction("UPDATE orders SET current_state = %s WHERE order_id = %s",
                                [str(error.OrderState.AUTO_CANCEL.value[0]), self.order_id])
        ret = sql.transaction("SELECT book_id, order_quantity FROM order_book WHERE order_id = %s", [self.order_id])
        for (book_id, quantity) in ret:
            sql.transaction("UPDATE book SET QUANTITY = QUANTITY + %s WHERE shop_id = %s AND book_id = %s",
                                [quantity, shop_id, book_id])
        threading.Lock.release()

    def run(self):
        time.sleep(sleep_time)
        self.time_check()        