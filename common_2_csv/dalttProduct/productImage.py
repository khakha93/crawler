from product.productImage import ProductImage as Pi
import re


class ProductImage(Pi):

    def get_img_src(self):
        # big image src
        xpath = '//*[@id="-content"]/div[2]/div/div[3]/div[1]/div[2]/div[1]/a/img'
        big_img_src = self.ch.driver.find_element_by_xpath(xpath).get_attribute('src')
        self.img_src_s.append(big_img_src)

        # review images

        # iframe 창으로 이동
        iframe_xpath = '//iframe[@id="crema-product-reviews-1"]'
        iframe_src = self.ch.driver.find_element_by_xpath(iframe_xpath).get_attribute('src')
        # print(iframe_src)
        self.ch.move(iframe_src)
        # iframe 창의 이미지들 가져오기
        xpath = '//li[@class="photo_thumbnail_box__photo"]'
        img_list = self.ch.driver.find_elements_by_xpath(xpath)
        for img in img_list:
            img_src = img.find_element_by_xpath('./a/img[1]').get_attribute('src')
            img_src = re.compile('thumbnail_').sub('', img_src)
            self.img_src_s.append(img_src)
        self.ch.move_back()
        return


