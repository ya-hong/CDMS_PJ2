from bookstore.classes.sql import SQL
from bookstore.error import OrderState
import time


class Order:
    """
    order_id, 
    user_id, shop_id, (买家id， 卖家商店id)
    books[(book_id, count)]  
    ORDER_TIME, CURRENT_STATE
    """

    def __init__(self, order_id) -> None:
        self.order_id = order_id
        self.sql = SQL()

    def create(order_id, user_id, shop_id, books):
        sql = SQL()
        sql.insert('orders', [order_id, user_id, shop_id, str(time.time()), OrderState.UNPAID.value[0]])
        for book in books:
            book_id = book['id']
            count = int(book['count'])
            sql.insert('order_book', [order_id, book_id, count])
        return Order(order_id)

    def fetch(self):
        try:
            (self.order_id, self.user_id, self.shop_id, 
                self.order_time, self.current_state) = self.sql.find_by_id('orders', self.order_id)
            ret = self.sql.transaction("SELECT book_id, order_quantity FROM order_book WHERE order_id = %s", [self.order_id])
            self.books = dict(zip(
                [ret[i][0] for i in range(len(ret))],
                [ret[i][1] for i in range(len(ret))]
            ))
        except Exception as e:
            print(e)

    def pay(self):
        with self.sql.transaction():
            self.sql.execute("UPDATE orders SET current_state = %s WHERE order_id = %s", [OrderState.UNDELIVERED.value[0], self.order_id])
