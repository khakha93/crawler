from browser import chrome
from settings import database
import requests as rq
from bs4 import BeautifulSoup as Bs
from pymysql.err import DataError
import re


class Page(object):
    site_id = None
    site_name = None

    def __init__(self, url, ch: chrome.Chrome):
        self.url = url
        self.ch = ch
        self.db = database.DataBase('united_crawler')
        # # Bs 사용 준비 : 원래는 많이 사용했으나, selenium 위주로 사용하면서, 쓸 일이 없어져서 주석처리함.
        # res = rq.get(self.url)
        # self.html = Bs(res.content, 'html.parser')
        return


# category 를 추가로 가진다.
class ExtendedPage(Page):
    def __init__(self, url, ch: chrome.Chrome, category):
        print(f'Create Page {url}')
        super().__init__(url, ch)
        self.category = category
        return

    def fill_err_product(self, err_type, url, product_id=-1, etc='NULL'):
        # print('fill err_product table')
        err_col = ['product_id', 'category', 'error_code', 'status', 'etc', 'url']
        try:
            if product_id < 0:
                product_id = 'NULL'
            err_val = [product_id, self.category, err_type, 'not solved', etc, url]
            self.db.insert_sub_data('err_product', err_col, err_val)
        except DataError:
            etc = etc[:50]
            err_val = [product_id, self.category, err_type, 'not solved', etc, url]
            self.db.insert_sub_data('err_product', err_col, err_val)
        else:
            pass
        return


# 후에 나올 CateInitPage와 ListedPage의 부모클래스.
class CategoryPage(ExtendedPage):
    def __init__(self, url, ch: chrome.Chrome, category):
        super().__init__(url, ch, category)
        # Crawling type, end_url, err_url, err_page
        self.cr_type = self.db.get_data('history', 'cr_type', 'category', category)
        # if self.cr_type is None:
        #     self.cr_type = 1
        self.end_url = None
        self.err_url = None
        self.err_page = None
        if self.cr_type != 1:
            self.end_url = self.db.get_data('history', 'end_url', 'category', category)
            if self.cr_type == 3:
                self.err_url = self.db.get_data('history', 'err_url', 'category', category)
                self.err_page = self.db.get_data('history', 'err_page', 'category', category)
        return

    def move_next_page(self, now_page):
        raise NotImplementedError
        # print(f'\nMove to next page! (from: {self.url})')
        # self.ch.click_by_xpath(next_page_xpath)

    def move_n_th_page(self, now_page):
        raise NotImplementedError

    # # <$$$> 무신사 임시. 사이트별로 오버라이딩하는게 정석.
    # def move_next_page(self, now_page):
    #     print(f'\nMove to next page! (from: {self.url})')
    #     search_syn = re.compile('&page=\\d+')
    #     if search_syn.search(self.url) is None:
    #         new_url = self.url + f'&page={now_page+1}'
    #     else:
    #         new_url = search_syn.sub(f'&page={now_page+1}', self.url)
    #     return new_url


