from product.productImage import ProductImage as Pi


class ProductImage(Pi):
    def get_img_src(self):
        # 색상 변경하면서 저장
        temp = self.ch.driver.find_elements_by_xpath('//*[@id="listChipColor"]/li')
        num_color = len(temp)
        for i in range(num_color):
            color_p = self.ch.driver.find_element_by_xpath(f'//*[@id="listChipColor"]/li[{i + 1}]')
            color_p.click()  # 컬러 선택하고
            self.ch.driver.implicitly_wait(1)

            x = '//div[@id="prodImgDefault"]/a'  # 저장할 이미지의 위치
            big_img_src = self.ch.driver.find_element_by_xpath(x).get_attribute('href')  # 이미지 소스 가져옴
            self.img_src_s.append(big_img_src)

        # 왼쪽에 있는 사진들 클릭하면서 저장
        x = '//ul[@class="listimage clearfix"]/li'
        left_img_html = self.ch.driver.find_elements_by_xpath(x)
        num_left = len(left_img_html)
        for i in range(num_left):
            img_url = self.ch.driver.find_element_by_xpath(f'{x}[{i + 1}]/a').get_attribute('rel')
            self.img_src_s.append(img_url)
        return

