from product.productSize import ProductSize as Ps


class ProductSize(Ps):
    def get_size_info(self, product_id):
        print("Get size from size_table")

        # 사이즈페이지 버튼 클릭
        xpath = '/html/body/div[2]/div[2]/div[3]/div[1]/form/dl[2]/dd/div[1]/a'
        self.ch.click_by_xpath(xpath)
        ori_window = self.ch.driver.window_handles[0]  # 상품페이지

        try:
            # 화면 전환
            n_window = self.ch.driver.window_handles[1]  # 사이즈표 페이지
        except IndexError:
            self.fill_err_product('size_error', self.url, product_id=product_id, etc='IndexError')
            return
        else:
            self.ch.driver.switch_to_window(n_window)  # 사이즈표로 화면 전환

            super().get_size_info(product_id)

            self.ch.driver.close()
            self.ch.driver.switch_to_window(ori_window)  # 다시 상품페이지로 화면 전환
    pass


# try:
#     s.get_size_info(product_id)  # 사이즈표 크롤링
# except Exception as ex:
#     print(f'{product_id}의 사이즈 정보 저장하다가 {type(ex)}: {ex}\n{self.url}')
#     self.fill_err_product('size_error', product_id, etc=f'{type(ex)}')
#     re_val = -1


