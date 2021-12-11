from werkzeug.datastructures import FileStorage
from bookstore.classes.sql import SQL
from bookstore import error
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
        sql.insert('orders', [order_id, user_id, shop_id, str(time.time()), 0])
        for book in books:
            (book_id, order_quantity) = book
            sql.insert('order_book', [order_id, book_id, order_quantity])
        return Order(shop_id)


    def fetch(self):
        try:
            (self.order_id, self.user_id, self.shop_id, 
                order_time, current_state) = self.sql.find_by_id('shops', self.shop_id)
            ret = self.sql.transaction("SELECT book_id, order_quantity FROM order_book WHERE order_id = ?", [self.order_id])
            self.books = dict(zip(
                [ret[i][0] for i in range(len(ret))],
                [ret[i][1] for i in range(len(ret))]
            ))
        except Exception as error:
            pass


    def pay(self):
        with self.sql.transaction():
            self.sql.execute("DELETE orders WHERE order_id = ?", [self.order_id])
            self.sql.execute("DELETE order_book WHERE order_id = ?", [self.order_id])
