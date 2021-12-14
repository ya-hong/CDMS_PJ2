from bookstore.classes.sql import SQL
from bookstore import error


def gen_query(table, query):
    q = []
    for terms in query:
        s = []
        for term in terms:
            s.append("{} LIKE '%%{}%%'".format(table, term))
        if len(s):
            q.append("({})".format(' AND '.join(s)))
    if len(q):
        return "({})".format(' OR '.join(q))
    return None


def search(page, title = [], tags = [], content = [], shop_id = None):
    sql = SQL()
    querys = []
    for (table, query) in [
        ('title', title), 
        ('tags', tags),
        ('content', content)
    ]:
        q = gen_query(table, query)
        if q != None:
            querys.append(q)
    if shop_id:
        querys.append("shop_id = '{}'".format(shop_id))
    query = ' AND '.join(querys)
    ret = sql.transaction("SELECT book_id, shop_id FROM books WHERE " 
        + query 
        + "LIMIT {} OFFSET {};".format(20, (page - 1) * 20))
    result = []
    for book in ret:
        (book_id, shop_id) = book
        result.append({
            "book_id": book_id,
            "shop_id": shop_id
        })
    return result