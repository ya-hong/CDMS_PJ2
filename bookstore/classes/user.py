from werkzeug.datastructures import FileStorage
from bookstore.classes.sql import SQL
from bookstore import error
from bookstore.classes.order import Order
from bookstore.classes.shop import Shop
import uuid


class User:
    """
    user_id, pwd, balance
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

    def unregister(self, password):
        with self.sql.transaction():
            ret = self.sql.execute("DELETE FROM users WHERE uid = %s AND pwd = %s", [self.user_id, password])
            if ret == 0:
                raise error.NO_PERMISSION({'message': '密码错误'})

    def login(self, password, terminal):
        with self.sql.transaction():
            ret = self.sql.execute("UPDATE users SET terminal = %s WHERE uid = %s AND pwd = %s",
                                   [terminal, self.user_id, password])
            if ret == 0:
                raise error.NO_PERMISSION({'message': '密码错误'})

    def password(self, old_password, new_password):
        with self.sql.transaction():
            ret = self.sql.execute("UPDATE users SET pwd = %s WHERE uid = %s AND pwd = %s",
                                   [new_password, self.user_id, old_password])
            if ret == 0:
                raise error.NO_PERMISSION({'message': '原始密码有误'})

    def logout(self):
        with self.sql.transaction():
            self.sql.execute("UPDATE users SET terminal = NULL where uid = %s", [self.user_id])

    def fetch(self):
        # 密码
        print(self.sql.find_by_id('users', self.user_id))
        (user_id, password, balance, token, terminal) = self.sql.find_by_id('users', self.user_id)
        self.pwd = password
        self.balance = balance
        # 商店
        ret = self.sql.transaction("SELECT shop_id FROM shops WHERE uid = %s", [self.user_id])
        self.shops = [Shop(ret[i][0]) for i in range(len(ret))]
        # 订单
        ret = self.sql.transaction("SELECT order_id FROM orders WHERE uid = %s", [self.user_id])
        self.orders = [Order(ret[i][0]) for i in range(len(ret))]

    def new_order(self, shop: Shop, books):
        with self.sql.transaction():
            order_id = str(uuid.uuid1())
            for book in books:
                book_id = book['id']
                count = int(book['count'])
                ret = self.sql.execute("SELECT quantity FROM books WHERE shop_id = %s AND book_id = %s",
                                       [shop.shop_id, book_id])
                if len(ret) == 0 or ret[0][0] < count:
                    raise error.INVENTORY_SHORTAGE
                else:
                    self.sql.execute("UPDATE books SET quantity=quantity-%s WHERE shop_id=%s AND book_id=%s",
                                     [count, shop.shop_id, book_id])
        order = Order.create(order_id, self.user_id, shop.shop_id, books)
        return order

    def payment(self, order: Order):
        self.fetch()
        print('uid', self.user_id, 'order_id', order.order_id)
        with self.sql.transaction():
            if len(self.sql.execute("SELECT * FROM orders WHERE uid = %s AND order_id = %s",
                                    [self.user_id, order.order_id])) == 0:
                print("无订单")
                raise error.INVALID_PARAMS
            ret = self.sql.execute(
                """SELECT SUM(order_quantity * price) 
                FROM order_book 
                    JOIN orders ON order_book.order_id = orders.order_id
                    JOIN books ON (orders.shop_id = books.shop_id AND order_book.book_id = books.book_id) 
                WHERE orders.order_id = %s;""", [order.order_id])
            print('ret', ret, 'balance', self.balance)
            price = 0 if ret[0][0] is None else ret[0][0]
            if price > self.balance:
                raise error.INSUFFICIENT_BALANCE
            self.sql.execute('UPDATE users SET balance = balance - %s WHERE uid = %s;', [price, self.user_id])
            order.pay()

    def add_funds(self, funds):
        self.sql.transaction("UPDATE users SET balance = balance + %s WHERE uid = %s;", [funds, self.user_id])

    def receipt(self, order_id,  password):
        self.fetch()
        if order_id in self.orders and password == self.pwd:
            ret = self.sql.execute("UPDATE orders SET current_state = %s WHERE order_id = %s and current_state = %s",
                                   [error.OrderState.COMPLETED.value[0], order_id, error.OrderState.DELIVERED.value[0]])
            if ret == 0:
                raise error.INVALID_PARAMS({'message': '订单号有误'})
        else:
            if order_id not in self.orders:
                raise error.INVALID_PARAMS({'message': '订单号有误'})
            elif password != self.pwd:
                raise error.NO_PERMISSION({'message': '密码有误，授权失败'})