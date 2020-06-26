from product.productImage import ProductImage as Pi
import re


class ProductImage(Pi):

    def get_img_src(self):
        # 이미지 src 가져오기: xpath 를 먼저 구한 후 src를 가져오는 방식
        big_img_xpath = '//*[@id="contents"]/div[2]/div[2]/div[1]/div[1]/div[1]/a/img'
        self.img_src_s.append(self.ch.driver.find_element_by_xpath(big_img_xpath).get_attribute('src'))

        small_img_x = '//*[@id="contents"]/div[2]/div[2]/div[1]/div[2]/ul/li'
        img_elements = self.ch.driver.find_elements_by_xpath(small_img_x)
        for e in img_elements:
            src = e.find_element_by_xpath('./img').get_attribute('src')
            self.img_src_s.append(src)
        return
