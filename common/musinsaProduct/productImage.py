from product.productImage import ProductImage as Pi
from browser.circleXpath import CircleXpath
import re


class ProductImage(Pi):

    def get_img_src(self):
        # 이미지 src 가져오기: xpath 를 먼저 구한 후 src를 가져오는 방식
        stat = '//ul[@class="product_thumb"]'
        dyn = '/li[1]'
        suffix = '/img'
        # x_list = self.ch.cir_xpath(stat, dyn, suffix)
        x_list = CircleXpath(self.ch, (stat, dyn, suffix)).completed_xpath_s
        for x in x_list:
            img_src = self.ch.driver.find_element_by_xpath(x).get_attribute('src')
            img_src = re.compile('60(?=\\.jpg)').sub('500', img_src)
            self.img_src_s.append(img_src)
        return
