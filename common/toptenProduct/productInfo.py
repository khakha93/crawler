from product.productInfo import ProductInfo as Pi
import re


class ProductInfo(Pi):

    def get_basic_info(self):
        print('Get basic information')

        # 정보 가져오기 (이건 노가다임 어쩔 수 없다)
        code = self.ch.driver.find_element_by_xpath('//*[@id="goods_form"]/div[1]/p').text
        self.code = re.compile('[\\w\\d]+$').search(code).group()
        name = self.ch.driver.find_element_by_xpath('//*[@id="goods_form"]/div[1]/h2').text
        price = self.ch.driver.find_element_by_xpath('//*[@id="goods_form"]/div[2]/ul/li[2]/span').text
        price = re.compile('[\\d,]+').search(price).group()

        # col, val
        self.col = ['brand', 'category', 'code', 'name', 'price', 'url']
        self.val = ['topten', self.category, self.code, name, price, self.url]
        # print(f'{col}: {val}')
        return
