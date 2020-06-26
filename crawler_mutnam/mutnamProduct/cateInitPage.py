from category.cateInitPage import CateInitPage as Ci
from .page import CategoryPage
from .productUrls import ProductUrls
import math


class CateInitPage(Ci, CategoryPage):

    def sort_by_new(self):
        self.move(self.url + '&sort_method=5')
        return

    # 추상화: category.cateInit 에 채워지는 부분
    def listed_crawling(self, url, page_idx):
        # 리스티드 페이지 생성
        product_urls = ProductUrls(url, self.category, page_idx)
        # 리스티드페이지 크롤링
        ret = product_urls.crawling_in_product_urls()
        return ret

    def through_page(self, str_page):
        # 총 페이지 수 구하기
        # 총 상품개수 찾기
        total_num = int(self.html.find('p', {'class': 'prdCount'}).find('strong').text)
        # 총 페이지 수 계산. 120으로 나누고 올림.
        page_num = math.ceil(total_num / 120)

        for i in range(str_page, page_num+1):

            # i번째 페이지로 이동
            # <$$$> 페이지 이동이 아니라 url만 구하면 된다 사실. 이게 논리적으로도 맞고
            self.move_n_th_page(i)

            ret = self.listed_crawling(self.url, i)

            if ret == -1:
                break
        return
