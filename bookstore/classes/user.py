from _typeshed import Self
from werkzeug.datastructures import FileStorage
from bookstore.classes.sql import SQL
from bookstore import error
from bookstore.classes.order import Order
from bookstore.classes.shop import Shop

class User:
    """
    user_id, password, balance
    token,
    orders[], shops[]
    """

    def __init__(self, user_id) -> None:
        self.user_id = user_id
        self.sql = SQL()
        if not self.sql.check('users', user_id):
            raise error.NO_USER


    def create(user_id, password):
        sql = SQL()
        with sql.transaction():
            ret = sql.execute("SELECT * FROM users WHERE uid = %s", [user_id])
            if len(ret):
                raise error.DUPLICATE_USERID
            sql.execute("INSERT INTO users(uid, pwd, balance) VALUES (%s, %s, 0)", [user_id, password])


    def fetch(self):
        # 密码
        print(self.sql.find_by_id('users', self.user_id))
        (user_id, password, balance, token, terminal) = self.sql.find_by_id('users', self.user_id)
        self.password = password
        self.balance = balance
        # 商店
        ret = self.sql.transaction("SELECT shop_id FROM shops WHERE uid = %s", [self.user_id])
        self.shops = [Shop(ret[i][0]) for i in range(len(ret))]
        # 订单
        ret = self.sql.transaction("SELECT order_id FROM orders WHERE uid = %s", [self.user_id])
        self.orders = [Order(ret[i][0]) for i in range(len(ret))]


    def new_order(self, shop: Shop, books):
        with self.sql.transaction():
            order_id = '1'
            for book in books:
                (book_id, count) = book 
                ret = self.sql.execute("SELECT quantity FROM books WHERE shop_id = %s book_id = %s", [shop.shop_id, book_id])
                if len(ret) == 0 or ret[0][0] < count:
                    raise error.INVENTORY_SHORTAGE
                else:
                    self.sql.insert('order_book', [order_id, book_id, count])
                    self.sql.execute("UPDATE books SET quantity=quantity-%s WHERE shop_id=%s book_id=%s", 
                        [shop.shop_id, book_id])
            order = Order.create(order_id, self.user_id, shop.shop_id, books)
        return order


    def payment(self, order: Order):
        self.fetch()
        with self.sql.transaction():
            if self.sql.execute("SELECT * FROM orders WHERE uid = %s AND order_id = %s", [self.user_id, order.order_id]) is None:
                raise error.INVALID_PARAMS
            ret = self.sql.execute(
                """SELECT SUM(order_quantity * price) 
                FROM order_book 
                    JOIN orders ON order_book.order_id = orders.order_id
                    JOIN books ON (orders.shop_id = books.shop_id AND order_book.book_id = books.book_id) 
                WHERE orders.order_id = %s;""", [order.order_id])
            price = 0 if ret[0][0] is None else ret[0][0] 
            if price > self.balance:
                raise error.INSUFFICIENT_BALANCE
            self.sql.execute('UPDATE users SET balance = balance - %s WHERE uid = %s;', [price, self.user_id])
            order.pay()


    def add_funds(self, funds):
        self.sql.transaction("UPDATE users SET balance = balance + %s WHERE uid = %s;", [funds, self.user_id])
