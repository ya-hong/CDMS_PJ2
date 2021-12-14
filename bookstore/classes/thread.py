import threading
import time
from bookstore.classes.order import Order
from bookstore.db_handler import DB_handler
from bookstore.classes.sql import SQL
from bookstore.error import OrderState


sleep_time = 10


class orderThread(threading.Thread):
    def __init__(self, option):
        threading.Thread.__init__(self)
        self.latency = 3600
        self.conn = DB_handler().db_connect()
        self.sql = SQL()
        self.option = option

    def time_check(self):
        threading.Lock.acquire()
        ret = self.sql.transaction("SELECT order_id, order_time, shop_id FROM orders WHERE\
                                    current_state != 0 order by order_time;", [])
        if ret is None:
            return
        to_del_num = 0
        for time_stamp in [float(i[1]) for i in ret]:
            if (time.time() - time_stamp) >= self.latency:
                to_del_num += 1
            else:
                break
        to_del_info = [(i[0], i[2]) for i in ret][:to_del_num]
        for order_id, shop_id in to_del_info:
            self.sql.transaction("UPDATE orders SET current_state = %s WHERE order_id = %s",
                                    [str(OrderState.AUTO_CANCEL.value[0]), order_id])
            ret = self.sql.transaction("SELECT book_id, order_quantity FROM order_book WHERE order_id = %s", [order_id])
            for (book_id, quantity) in ret:
                self.sql.transaction("UPDATE book SET QUANTITY = QUANTITY + %s WHERE shop_id = %s AND book_id = %s",
                                    [quantity, shop_id, book_id])
        threading.Lock.release()

    def deliver(self):
        threading.Lock.acquire()
        ret = self.sql.transaction("SELECT order_id FROM orders WHERE current_state = %s;", [OrderState.UNDELIVERED.value[0]])
        if ret is None:
            return
        for order_id in [i[0] for i in ret]:
            self.sql.transaction("UPDATE orders SET current_state = %s WHERE order_id = %s",
                                    [str(OrderState.DELIVERED.value[0]), order_id])
        threading.Lock.release()

    def run(self):
        while True:
            if self.option == 1:
                self.time_check()
            else:
                self.deliver()
            time.sleep(sleep_time)


if __name__ == "__main__":
    thread_auto_cancel = orderThread(1)
    thread_deliver = orderThread(2)
    thread_auto_cancel.start()
    thread_deliver.start()