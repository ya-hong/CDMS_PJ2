import threading
import time
from bookstore.db_handler import DB_handler
from bookstore.classes.sql import SQL
from bookstore.error import OrderState


sleep_time = 10


class orderThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.latency = 3600
        self.conn = DB_handler().db_connect()
        self.sql = SQL()

    def time_check(self):
        threading.Lock.acquire()
        ret = self.sql.transaction("SELECT order_id, order_time FROM orders WHERE\
                                    current_state != 0 order by order_time;", [])
        if ret is None:
            return
        to_del_num = 0
        for time_stamp in [float(i[1]) for i in ret]:
            if (time.time() - time_stamp) >= self.latency:
                to_del_num += 1
            else:
                break
        to_del_id = [i[0] for i in ret][:to_del_num]
        for order_id in to_del_id:
            self.sql.transaction("UPDATE orders SET current_state = %s WHERE order_id = %s",
                                    [str(OrderState.AUTO_CANCEL.value[0]), order_id])
        threading.Lock.release()

    def run(self):
        while True:
            self.time_check()
            time.sleep(sleep_time)


if __name__ == "__main__":
    thread = orderThread()
    thread.start()