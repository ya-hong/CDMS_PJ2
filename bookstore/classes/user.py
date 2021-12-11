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
        SQL().insert('users', [user_id, password], "uid, password")


    def fetch(self):
        # 密码
        (user_id, password, balance, terminal) = self.sql.find_by_id('users', self.user_id)
        self.password = password
        self.balance = balance
        # 商店
        ret = self.sql.transaction("SELECT shop_id FROM shops WHERE user_id = ?", [self.user_id])
        self.shops = [Shop(ret[i][0]) for i in range(len(ret))]
        # 订单
        ret = self.sql.transaction("SELECT order_id FROM orders WHERE user_id = ?", [self.user_id])
        self.orders = [Order(ret[i][0]) for i in range(len(ret))]


    def new_order(self, shop: Shop, books):
        with self.sql.transaction():
            for book in books:
                (book_id, count) = book 
                ret = self.sql.execute("SELECT quantity FROM books WHERE shop_id = ? book_id = ?", [shop.shop_id, book_id])
                if len(ret) == 0 or ret[0][0] < count:
                    raise error.INVENTORY_SHORTAGE
                else:
                    self.sql.execute("UPDATE books SET quantity=quantity-? WHERE shop_id=? book_id=?", 
                        [shop.shop_id, book_id])
            order = Order.create('1', self.user_id, shop.shop_id, books)
        return order


    def payment(self, order: Order):
        self.fetch()
        order.fetch()
        with self.sql.transaction():
            flag = False
            for ord in self.orders:
                if order.order_id == ord.order_id:
                    flag = True
            if not flag:
                raise
            ret = self.sql.execute(
                "SELECT SUM(quantity * price) "
                "FROM order_book join orders WHERE order_book.order_id = orders.order_id "
                "WHERE orders.order_id = ?;", [order.order_id])
            price = ret[0][0]
            if price > self.balance:
                raise 
            self.sql.execute('UPDATE users SET balance = balance - ? WHERE uid = ?;', [price, self.user_id])
            order.pay()


    def add_funds(self, funds):
        self.sql.transaction("UPDATE users SET balance = balance + ? WHERE uid = ?;", [funds])
