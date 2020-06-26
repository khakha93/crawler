from page import CategoryPage
# from dalttProduct.productPage import ProductPage
# from uniqloProduct.productPage import ProductPage
# from leeheeProduct.productPage import ProductPage
from browser import chrome
from sitePage.siteInformation import ProductXpathInfo
from browser.circleXpath import CircleXpath


# 딱 상품들 나열된 페이지 (해당 카테고리 전체를 지칭하지 않음)
class ListedPage(CategoryPage):
    # <$$$> 첫 상품 긁었는지 확인하는 지표. 이거 어떻게 관리해햐할지 아직 미흡
    flag = None

    def __init__(self, url, ch: chrome.Chrome, category, page_num):
        print(f'Create {page_num}\'th ListedPage')
        self.page_num = page_num
        super().__init__(url, ch, category)
        self.product_urls = self.get_product_urls()

    def get_product_urls(self):
        product_urls = []
        cir_xpath_elements = ProductXpathInfo(self.site_name).cir_elements
        product_xpath_s = CircleXpath(self.ch, cir_xpath_elements).completed_xpath_s
        for x in product_xpath_s:
            try:
                # print(f'append {x}')
                product_urls.append(self.ch.driver.find_element_by_xpath(x).get_attribute('href'))
            except chrome.sel_exceptions.NoSuchElementException:
                # # 상품이 하나도 없는 경우임. 카테고리 전체를 끝낸다.
                # print(x)
                # # <$$$> 논리가 잘못 됨.
                # print('빈 페이지(ListedPage)')
                # return None
                # print(f'do not append {x}')
                pass
            except Exception as ex:
                print(f'{type(ex)}: {ex}')
        return product_urls

    def check_duplication(self, product_url):
        # url 이 이미 DB에 있는 경우
        if self.db.is_duplication('product', 'url', product_url) > 0:
            # DB에 있는 거랑 카테고리가 다르면: 에러처리해줘야함
            if self.db.get_data('product', 'category', 'url', product_url) != self.category:
                p_id = self.db.get_data('product', 'id', 'url', product_url)
                self.fill_err_product('category_match_error', product_url, product_id=p_id)

            # 모든 검사를 끝낸 경우 : 또 긁을 필요는 없지
            if self.db.get_data('product', 'all_fin', 'url', product_url) == 'True':
                # Case 1 인 경우 이 상품만 패스
                if self.cr_type == 1:
                    return 1
                # case 2, case 3 인 경우
                else:
                    # 이게 end_url 이면, 카테고리 전체를 끝내야한다
                    if product_url == self.end_url:
                        print('이후 모든 상품은 패스')
                        return 2
                    else:
                        print('어쩌다 꼬여서 중복')
                        return 1
            # 긁긴 했는데 중간에 끊긴 경우 : 다시 크롤링해줘야함
            else:
                return 3
        # DB에 없는 경우: 그냥 크롤링 해주면 된다
        else:
            print('없는 상품이므로 크롤링')
            return 4

    def after_first_product_crawling(self, product_url):
        if self.cr_type != 3:
            self.db.update_data('history', 'latest_url', product_url, 'category', self.category)
        self.db.update_data('history', 'cr_type', 3, 'category', self.category)
        # err_page update
        self.db.update_data('history', 'err_page', self.page_num, 'category', self.category)
        ListedPage.flag = False
        return

"""
1. continue

2. return -1

3. rec = True

4. rec = False

"""













