from product.productInfo import ProductInfo as Pi
import re


class ProductInfo(Pi):
    def get_basic_info(self):

        self.col = ['brand', 'category', 'code', 'name', 'price', 'sex', 'url']

        code_xpath = '/html/body/div[2]/div[2]/div[1]/div[1]/ul[1]/li[1]'
        code = self.ch.driver.find_element_by_xpath(code_xpath).text
        self.code = re.compile('\\d+').search(code).group()

        name_xpath = '/html/body/div[2]/div[2]/div[1]/div[1]/h2'
        name = self.ch.driver.find_element_by_xpath(name_xpath).text

        price_xpath = '/html/body/div[2]/div[2]/div[1]/div[1]/ul[1]/li[2]/p'
        price = self.ch.driver.find_element_by_xpath(price_xpath).text

        sex_xpath = '/html/body/div[2]/div[2]/div[1]/div[1]/p'
        sex = self.ch.driver.find_element_by_xpath(sex_xpath).text

        self.val = ['uniqlo', self.category, self.code, name, price, sex, self.url]

        print(f'{self.col}: {self.val}')
        return

