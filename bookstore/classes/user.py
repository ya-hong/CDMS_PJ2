from werkzeug.datastructures import FileStorage
from bookstore.classes.sql import SQL
from bookstore import error
from bookstore.classes.order import Order
from bookstore.classes.shop import Shop
import uuid
from bookstore.error import OrderState


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
        orders = [self.orders[i].order_id for i in range(len(self.orders))]
        if not order.order_id in orders:
            raise error.INVALID_PARAMS({'message': "订单不存在"})
        order.fetch()

        with self.sql.transaction():
            if order.price > self.balance:
                raise error.INSUFFICIENT_BALANCE
            self.sql.execute('UPDATE users SET balance = balance - %s WHERE uid = %s;', 
                [order.price, self.user_id])
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

    def delivery(self, shop_id, order_id):
        self.fetch()
        flag = False
        for shop in self.shops:
            if shop_id == shop.shop_id:
                flag = True
                break
        if flag:
            ret = self.sql.execute("SELECT * FROM orders WHERE order_id = %s", [order_id])
            # print('status', ret)
            ret = self.sql.execute("UPDATE orders SET current_state = %s WHERE order_id = %s and current_state = %s",
                                   [error.OrderState.DELIVERED.value[0], order_id, error.OrderState.UNDELIVERED.value[0]])
            # print("return ", ret)
            if ret == 0:
                raise error.INVALID_PARAMS
        else:
            raise error.NO_PERMISSION({'message': '权限不足'})

    def history(self):
        self.fetch()
        orders = []
        for order in self.orders:
            order.fetch()
            orders.append({
                'order_id': order.order_id,
                'state': order.current_state
            })
        return orders

    def cancel(self, order:Order):
        self.fetch()
        orders = [self.orders[i].order_id for i in range(len(self.orders))]
        if not order.order_id in orders:
            raise error.INVALID_PARAMS({'message': '订单ID不存在'})
        order.fetch()
        if not order.current_state in [OrderState.UNPAID.value[0], OrderState.UNDELIVERED.value[0]]:
            print('订单状态', order.current_state)
            raise error.CANT_CANCEL
        if order.current_state != OrderState.UNPAID.value[0]:
            self.add_funds(order.price)
        order.cancel()