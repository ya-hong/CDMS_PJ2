from enum import auto
from bookstore.classes.shop import Shop
from bookstore.classes.sql import SQL
from bookstore.error import OrderState
import time
from bookstore.classes.thread import orderThread


class Order:
    """
    order_id, 
    user_id, shop_id, (买家id， 卖家商店id)
    books[book_id -> count]
    price
    ORDER_TIME, CURRENT_STATE
    """

    def __init__(self, order_id) -> None:
        self.order_id = order_id
        self.sql = SQL()

    def create(order_id, user_id, shop_id, books):
        sql = SQL()
        sql.insert('orders', [order_id, user_id, shop_id, str(time.time()), OrderState.UNPAID.value[0]])
        thread = orderThread(order_id)
        thread.start()
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
            ret = self.sql.execute(
                """SELECT SUM(order_quantity * price) 
                FROM order_book 
                    JOIN orders ON order_book.order_id = orders.order_id
                    JOIN books ON (orders.shop_id = books.shop_id AND order_book.book_id = books.book_id) 
                WHERE orders.order_id = %s;""", [self.order_id])
            self.price = 0 if ret[0][0] is None else ret[0][0]
        except Exception as e:
            print(e)

    def pay(self):
        with self.sql.transaction():
            self.sql.execute("UPDATE orders SET current_state = %s WHERE order_id = %s", [OrderState.UNDELIVERED.value[0], self.order_id])

    def cancel(self, auto_cancel = False):
        if auto_cancel:
            code = OrderState.AUTO_CANCEL.value
        else:
            code = OrderState.BUYER_CANCEL.value 
        print('code', code)
        self.sql.transaction("UPDATE orders SET current_state = %s WHERE order_id = %s", [code, self.order_id])
        self.fetch()
        shop = Shop(self.shop_id)
        for (book_id, count) in self.books.items():
            shop.add_stock_level(book_id, count)