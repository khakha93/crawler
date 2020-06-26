from category.cateInitPage import CateInitPage as Ci
from .page import CategoryPage
from .productUrls import ProductUrls


class CateInitPage(Ci, CategoryPage):

    def sort_by_new(self):
        self.url = self.url + '/?&sort=new'
        self.ch.move(self.url)
        return

    # 추상화: cateInit 에 채워지는 부분
    def listed_crawling(self, url, page_idx):
        # 리스티드 페이지 생성
        product_urls = ProductUrls(url, self.ch, self.category, page_idx)
        # 리스티드페이지 크롤링
        ret = product_urls.crawling_in_product_urls()
        return ret

    def through_page(self, now_page):
        xpath = '//span[@class="totalPagingNum"]'
        page_num = int(self.ch.driver.find_element_by_xpath(xpath).text)

        while now_page <= page_num:
            now_url = self.ch.driver.current_url
            ret = self.listed_crawling(now_url, now_page)

            if ret == -1:
                break

            self.move_next_page(now_page)

            now_page = now_page + 1
        return


