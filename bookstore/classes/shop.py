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


    def create(user_id, shop_id):
        SQL().insert('shops', [shop_id, user_id], "shop_id, uid")
        return Shop(shop_id)


    def fetch(self):
        try:
            (self.shop_id, self.user_id, self.ranking) = self.sql.find_by_id('shops', self.shop_id)
            ret = self.sql.transaction("SELECT book_id, quantity FROM books WHERE shop_id = ?", [self.shop_id])
            self.books = dict(zip(
                [ret[i][0] for i in range(len(ret))],
                [ret[i][1] for i in range(len(ret))]
            ))
        except Exception as error:
            pass

