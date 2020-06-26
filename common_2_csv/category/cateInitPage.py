from browser import chrome
from page import CategoryPage
from category.listedPage import ListedPage
# from sitePage.siteInformation import EtcInfo


class CateInitPage(CategoryPage):

    # def __init__(self, url, ch: chrome.Chrome, category):
    #     print(f'Create CateInitPage: {category}')
    #     super().__init__(url, ch, category)
    #     self.sort_by_new()  # 신상품순으로 정렬
    #     return

    def sort_by_new(self):
        raise NotImplementedError

    def crawling_by_category(self):
        print(f'\n[Crawling category] ({self.category})')
        # <$$$> 이거 확신이 없다...
        ListedPage.flag = True

        str_page = 1
        # <선 수행> case3: 처음 페이지로 이동 or 에러페이지로 이동
        if self.cr_type == 3:
            print(f'err_page: {self.err_page}')
            str_page = self.err_page

        # 페이지 넘겨가면서 크롤링 해준다
        self.through_page(str_page)
        # try:
        #     pass
        # except Exception as ex:     # 페이지 넘기고 하다보면 에러자 자주 발생함. 걍 넘어가는게 상책
        #     print(ex)
        #     # self.fill_err_product('unknown_error', self.url, etc=str(type(ex)))
        #     return

        # 정상 종료했으니, 가장 먼저 긁은거 표시하고 정상종료 표시하고 종료
        latest_url = self.db.get_data('history', 'latest_url', 'category', self.category)
        self.db.update_data('history', 'end_url', latest_url, 'category', self.category)
        self.db.update_data('history', 'cr_type', 2, 'category', self.category)
        print(f'Finish category({self.category}) crawling\n')
        return

    def through_page(self, now_page):
        raise NotImplementedError
        # while True:
        #     now_url = self.ch.driver.current_url
        #
        #     ret = self.listed_crawling(now_url, now_page)
        #
        #     if ret == -1:  # 카테고리 전체를 끝내야하는 경우
        #         break
        #
        #     # 다음 페이지로 이동
        #     self.move_next_page(now_page)
        #     after_url = self.ch.driver.current_url
        #
        #     # 마지막 페이지가 되면 반복문 탈출
        #     if now_url == after_url:
        #         break
        #
        #     now_page = now_page + 1
        # return

    def listed_crawling(self, url, page_idx):
        # # 리스티드 페이지 생성
        # product_urls = Listed.ProductUrls(now_url, self.ch, self.category, now_page)
        # # 리스티드페이지 크롤링
        # ret = product_urls.crawling_in_product_urls()
        raise NotImplementedError

# for i in range(self.err_page - 1):
#     self.move_next_page(self.next_page_xpath)
#     a_url = self.move_next_page(now_page)
#     self.ch.move(a_url)
#     now_page = now_page + 1


# 신상품순으로 정렬하는데, 홈페이지마다 다름
# <$$$> 따로 빼서 오버라이딩 처리하기
# def sort_by_new(url):
#     # sorted_url = url + '&sortType=02'
#     # 이희은닷컴 예시
#     # sorted_url = url + '&sort_method=5#Product_ListMenu'
#     # 무신사
#     sorted_url = url + '/?&sort=new'
#     return sorted_url

