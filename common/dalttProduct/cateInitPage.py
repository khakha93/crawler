from category.cateInitPage import CateInitPage as Ci
from .page import CategoryPage
from .productUrls import ProductUrls


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



