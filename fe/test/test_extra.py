import pytest
from fe.access import seller

from fe.access.new_buyer import register_new_buyer
from fe.access.new_seller import register_new_seller
from fe.test.gen_book_data import GenBook
from fe.access import buyer
import uuid

def gen_order(self):
    # do before test
    
    ## gen seller
    self.seller_id = "test_extra_seller_id_{}".format(str(uuid.uuid1()))
    self.store_id = "test_extra_store_id_{}".format(str(uuid.uuid1()))
    self.seller_password = self.seller_id
    self.gen_book = GenBook(self.seller_id, self.store_id)
    self.seller = self.gen_book.seller
    
    ## gen buyer
    self.buyer_id = "test_extra_buyer_id_{}".format(str(uuid.uuid1()))
    self.buyer_password = self.buyer_id
    self.buyer = register_new_buyer(self.buyer_id, self.buyer_password)

    ## gen order 
    ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
    assert(ok)
    self.buy_book_info_list = self.gen_book.buy_book_info_list
    code, self.order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
    assert(code == 200)


class TestDelivery:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        gen_order(self)
        self.total_price = 0
        for item in self.buy_book_info_list:
            book = item[0]
            num = item[1]
            if book.price is None:
                continue
            else:
                self.total_price = self.total_price + book.price * num

        code = self.buyer.add_funds(self.total_price)
        assert code == 200
        code = self.buyer.payment(self.order_id)
        assert code == 200

        yield
        # do after test

    def test_ok(self):
        code = self.seller.delivery(self.seller_id, self.store_id, self.order_id)
        assert code == 200
        code = self.buyer.delivery(self.order_id)
        assert code == 200

    def test_no_permission(self):
        code = self.seller.delivery(self.seller_id + '1', self.store_id, self.order_id)
        assert code == 401

    def test_no_order(self):
        code = self.seller.delivery(self.seller_id, self.store_id, self.order_id + '1')
        assert(code != 200)

    def test_no_store(self):
        code = self.seller.delivery(self.seller_id, self.store_id + '1', self.order_id)
        assert(code != 200)



class TestHistory:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        # do before test
        gen_order(self)
        yield
        # do after test

    def test_ok(self):
        code, orders = self.buyer.history(self.buyer.user_id)
        assert code == 200
        assert(self.order_id == orders[0]['order_id'])

    def test_no_permission(self):
        code, _ = self.buyer.history(self.buyer.user_id + '1')
        assert code == 401


class TestCancelOrder:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        gen_order(self)

        # 充钱
        self.total_price = 0
        for item in self.buy_book_info_list:
            book = item[0]
            num = item[1]
            if book.price is None:
                continue
            else:
                self.total_price = self.total_price + book.price * num

        code = self.buyer.add_funds(self.total_price)
        assert code == 200
        
        yield
    
    def test_ok(self):
        code = self.buyer.cancel_order(self.order_id)
        assert(code == 200)
    
    def test_no_order(self):
        code = self.buyer.cancel_order(self.order_id + '1')
        assert(code != 200)

    def test_cant_cancel(self):
        code = self.buyer.payment(self.order_id)
        assert(code == 200)
        code = self.seller.delivery(self.seller_id, self.store_id, self.order_id)
        assert(code == 200)
        code = self.buyer.cancel_order(self.order_id)
        assert(code != 200)


class TestSearch:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_search_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_search_store_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_search_buyer_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        self.gen_book = GenBook(self.seller_id, self.store_id)
        self.seller = self.gen_book.seller
        self.buyer = register_new_buyer(self.buyer_id, self.password)
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
        assert ok
        yield

    def test_ok(self):
        code = self.buyer.search({
            "title": [["唐诗"]],
            "tags": [["唐诗", "宋词"], ["元曲"]],
            "content": [[]],
            "shop_id": self.store_id,
            "page_num": 1
        })
        assert code == 200