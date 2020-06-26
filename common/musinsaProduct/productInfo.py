# from page import ExtendedPage
# from settings.reText import rm_blank
import re
from product.productInfo import ProductInfo as Pi
from browser.chrome import sel_exceptions


def refine_season_sex_text(text):
    text = re.compile('[\\n\\t]').sub('', text)
    text = re.compile('^\\s').sub('', text)
    text = re.compile('/(?=[^/]+$)').sub('-', text)
    return text


class ProductInfo(Pi):

    def get_basic_info(self):
        x_path = '//div[@class="explan_product product_info_section"]/ul/li'
        info_mass = self.ch.driver.find_elements_by_xpath(x_path)
        num = len(info_mass)

        self.col = ['category', 'brand', 'code', 'price', 'name', 'url']

        brand_code_text = self.ch.driver.find_element_by_xpath(x_path + f'[1]/p[2]').text
        q = re.compile('^.*?/')
        brand = re.compile('\\s+/$').sub('', q.search(brand_code_text).group())
        self.code = re.compile('^\\s+').sub('', q.sub('', brand_code_text))

        try:
            price = self.ch.driver.find_element_by_xpath('//span[@id="sale_price"]').text
        except sel_exceptions.NoSuchElementException:
            price = self.ch.driver.find_element_by_xpath('//span[@id="goods_price"]').text
            price = re.compile('[\\r\\n\\t]+').sub('', price)
        else:
            price = re.compile('[\\r\\n\\t]+').sub('', price)

        name = self.ch.driver.find_element_by_xpath('//span[@class="product_title"]/span').text

        self.val = [self.category, brand, self.code, price, name, self.url]

        for i in range(2, num):
            change_eng = {'시즌': 'season', '성별': 'sex'}

            left_text = self.ch.driver.find_element_by_xpath(x_path + f'[{i}]/p[1]').text
            # left_text = rm_blank(left_text)
            re.compile('[\\n\\r\\s\\t]').sub('', left_text)
            right_text = self.ch.driver.find_element_by_xpath(x_path + f'[{i}]/p[2]').text
            if '시즌' in left_text and '성별' in left_text:
                self.col = self.col+['season', 'sex']
                # season_sex
                season_sex_list = re.split('-', refine_season_sex_text(right_text))
                for e in season_sex_list:
                    self.val.append(e)
            else:
                left_text = re.compile('(시즌|성별)').search(left_text)
                if left_text is not None:
                    self.col.append(change_eng[left_text.group()])
                    self.val.append(re.compile('[\\n\\r\\s\\t]').sub('', right_text))
        return


