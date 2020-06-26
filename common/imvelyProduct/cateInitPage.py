from category.cateInitPage import CateInitPage as Ci
from .page import CategoryPage
from .productUrls import ProductUrls
import re


class CateInitPage(Ci, CategoryPage):

    def sort_by_new(self):
        self.url = self.url + '&sort_method=5'
        self.ch.move(self.url)
        return

    # 추상화: category.cateInit 에 채워지는 부분
    def listed_crawling(self, url, page_idx):
        # 리스티드 페이지 생성
        product_urls = ProductUrls(url, self.ch, self.category, page_idx)
        # 리스티드페이지 크롤링
        ret = product_urls.crawling_in_product_urls()
        return ret

    def through_page(self, now_page):
        while True:
            now_url = self.ch.driver.current_url

            ret = self.listed_crawling(now_url, now_page)

            if ret == -1:  # 카테고리 전체를 끝내야하는 경우
                break

            # 다음 페이지로 이동
            self.move_next_page(now_page)
            after_url = self.ch.driver.current_url
            after_url = re.compile('#none$').sub('', after_url)

            # 마지막 페이지가 되면 반복문 탈출
            if now_url == after_url:
                break

            now_page = now_page + 1
        return

