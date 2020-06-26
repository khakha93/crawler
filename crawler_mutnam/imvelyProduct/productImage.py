from product.productImage import ProductImage as Pi


class ProductImage(Pi):

    def get_img_src(self):
        # big image src
        xpath = '//div[@class="detailArea "]/div[1]/div[1]/a/img'
        big_img_src = self.ch.driver.find_element_by_xpath(xpath).get_attribute('src')
        self.img_src_s.append(big_img_src)

        return


