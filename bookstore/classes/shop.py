from werkzeug.datastructures import FileStorage
from bookstore.classes.sql import SQL
from bookstore import error




class Shop:
    """
    shop_id, user_id, ranking
    books{book_id -> count}
    """

    def __init__(self, shop_id) -> None:
        self.shop_id = shop_id
        self.sql = SQL()
        if not self.sql.check('shops', shop_id):
            raise error.NO_SHOP


    def create(user_id, shop_id):
        sql = SQL()
        if sql.check('shops', shop_id):
            raise error.DUPLICATE_SHOPID
        sql.insert('shops', [shop_id, user_id], "shop_id, uid")
        return Shop(shop_id)


    def fetch(self):
        try:
            (self.shop_id, self.user_id, self.ranking) = self.sql.find_by_id('shops', self.shop_id)
            ret = self.sql.transaction("SELECT book_id, quantity FROM books WHERE shop_id = %s", [self.shop_id])
            self.books = dict(zip(
                [ret[i][0] for i in range(len(ret))],
                [ret[i][1] for i in range(len(ret))]
            ))
        except Exception as error:
            pass


    def add_book(self, book_info, quantity):
        if self.sql.check("books", book_info['id']):
            raise error.DUPLICATE_BOOKID

        l = ['shop_id', 'quantity']
        l.extend(list(book_info.keys())[2:])
        tags = ", ".join(l)
        arr = [self.shop_id, int(quantity)]
        arr.extend(list(book_info.values())[2:])
        print('shop.py')
        print(arr)
        print(tags)
        self.sql.insert("books", arr, tags)



    def add_stock_level(self, book_id, offset):
        if not self.sql.check("books", book_id):
            raise error.NO_BOOK
        self.sql.transaction("UPDATE books SET quantity = quantity + %s WHERE shop_id = %s AND book_id = %s;",
                             [offset, self.shop_id, book_id])

