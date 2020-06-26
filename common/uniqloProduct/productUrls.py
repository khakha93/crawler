from category.productUrls import ProductUrls as Pu
from browser.circleXpath import CircleXpath
# from .page import CategoryPage
from .productPage import ProductPage
# from sitePage.siteInformation import ProductXpathInfo


class ProductUrls(Pu):

    # 추상화: productUrls 에 채워지는 부분
    def product_crawling(self, product_url, rec):
        ProductPage(product_url, self.ch, self.category).crawling_by_product(rec)
        # raise NotImplementedError

    # def get_product_urls(self):
    #     product_urls = []
    #
    #     product_stat = '//*[@id="content1"]'
    #     product_dyn = '/div[3]/div/ul/li[1]'
    #     product_suffix = '/div[1]/p/a'
    #
    #     product_xpath_s = CircleXpath(self.ch, cir_xpath_elements).completed_xpath_s
    #     for x in product_xpath_s:
    #         try:
    #             # print(f'append {x}')
    #             product_urls.append(self.ch.driver.find_element_by_xpath(x).get_attribute('href'))
    #         except chrome.sel_exceptions.NoSuchElementException:
    #             # # 상품이 하나도 없는 경우임. 카테고리 전체를 끝낸다.
    #             # print(x)
    #             # # <$$$> 논리가 잘못 됨.
    #             # print('빈 페이지(ListedPage)')
    #             # return None
    #             # print(f'do not append {x}')
    #             pass
    #         except Exception as ex:
    #             print(f'{type(ex)}: {ex}')
    #     return product_urls
