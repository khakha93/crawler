# from page import ExtendedPage
# from settings.reText import rm_blank
import re
from product.productInfo import ProductInfo as Pi


def refine_season_sex_text(text):
    text = re.compile('[\\n\\t]').sub('', text)
    text = re.compile('^\\s').sub('', text)
    text = re.compile('/(?=[^/]+$)').sub('-', text)
    return text


class ProductInfo(Pi):

    def get_basic_info(self):

        self.col = ['category', 'brand', 'code', 'price', 'name', 'url']

        table_xpath = '//table/tbody'
        table_mass = self.ch.driver.find_element_by_xpath(table_xpath)
        row = table_mass.find_elements_by_xpath('./tr[@class=" xans-record-"]')
        for r in row:
            if r.find_element_by_xpath('./th').text == '상품코드':
                self.code = r.find_element_by_xpath('./td').text

        name_xpath = '//div[@class="infoArea"]/h2'
        name = self.ch.driver.find_element_by_xpath(name_xpath).text

        price_xpath = '//*[@id="span_product_price_text"]'
        price = self.ch.driver.find_element_by_xpath(price_xpath).text

        self.val = [self.category, 'LEEHEE', self.code, price, name, self.url]

        # print(f'{self.col}: {self.val}')
        return


