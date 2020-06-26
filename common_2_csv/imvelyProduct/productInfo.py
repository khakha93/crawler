from product.productPage import ProductInfo as Pi


class ProductInfo(Pi):
    def get_basic_info(self):
        name_xpath = '//div[@class="prdInfo"]/div[1]/h3'
        price_xpath = '//div[@class="prdInfo"]/div[2]/table/descendant::tr[@class="판매가  xans-record-"]/td'
        name = self.ch.driver.find_element_by_xpath(name_xpath).text
        self.code = name
        price = self.ch.driver.find_element_by_xpath(price_xpath).text

        self.col = ['brand', 'category', 'code', 'name', 'price', 'url']
        self.val = ['imvely', self.category, self.code, name, price, self.url]
        # print(f'{self.col}: {self.val}')
        return




