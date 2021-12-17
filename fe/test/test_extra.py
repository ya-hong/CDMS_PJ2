import pytest
from fe.access import seller

from fe.access.new_buyer import register_new_buyer
from fe.access.new_seller import register_new_seller
from fe.test.gen_book_data import GenBook
import uuid


class TestDelivery:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        # do before test
        
        ## gen seller
        self.seller_id = "test_extra_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_extra_store_id_{}".format(str(uuid.uuid1()))
        self.seller_password = self.seller_id
        self.gen_book = GenBook(self.seller_id, self.store_id)
        self.seller = self.gen_book.seller
        
        ## gen buyer
        self.buyer_id = "test_extra_buyer_id_{}".format(str(uuid.uuid1()))
        self.buyer_password = self.buyer_id + '_pwd'
        self.buyer = register_new_buyer(self.buyer_id, self.buyer_password)

        ## gen order 
        ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False)
        assert(ok)
        self.buy_book_info_list = self.gen_book.buy_book_info_list
        code, self.order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        assert(code == 200)

        
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

    def test_no_permission(self):
        code = self.seller.delivery(self.seller_id + '1', self.store_id, self.order_id)
        assert code == 401

    def test_no_order(self):
        code = self.seller.delivery(self.seller_id, self.store_id, self.order_id + '1')
        assert(code != 200)

    def test_no_store(self):
        code = self.seller.delivery(self.seller_id, self.store_id + '1', self.order_id)
        assert(code != 200)

