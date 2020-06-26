from product.productImage import ProductImage as Pi


class ProductImage(Pi):

    def get_img_src(self):
        # 이미지 src 가져오기: xpath 를 먼저 구한 후 src를 가져오는 방식
        stat = '//*[@id="slideshow"]'
        dyn = '/li[1]'
        suffix = '/button/img'
        x_list = self.ch.cir_xpath(stat, stat + dyn, suffix)
        for x in x_list:
            img_src = self.ch.driver.find_element_by_xpath(x).get_attribute('src')
            self.img_src_s.append(img_src)
        return
