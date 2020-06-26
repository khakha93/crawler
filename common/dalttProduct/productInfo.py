from product.productPage import ProductInfo as Pi


class ProductInfo(Pi):
    def get_basic_info(self):
        name_xpath = '//*[@id="-payment"]/div/ul/li[1]/div/div[1]/h1'
        price_xpath = '//*[@id="-payment"]/div/ul/li[1]/div/div[2]/table/tbody/tr[2]/td'
        name = self.ch.driver.find_element_by_xpath(name_xpath).text
        self.code = name
        price = self.ch.driver.find_element_by_xpath(price_xpath).text

        self.col = ['brand', 'category', 'code', 'name', 'price', 'url']
        self.val = ['daltt', self.category, self.code, name, price, self.url]
        print(f'{self.col}: {self.val}')
        return

    # get_basic_info() 에서 얻은 데이터를 DB로
    def product_insert_2_db(self):

        self.get_basic_info()

        # print(code)
        # DB 에 넣기 & product id 가져오기
        dup_num = self.db.is_duplication('product', 'code', self.code)
        if dup_num == 0:  # 코드가 같은게 하나도 없으면 -> 아무 생각 말고 긁어
            product_id = self.db.insert_sub_data('product', self.col, self.val)
        else:
            # 전체보기 카테고리인지 확인
            if '전체보기' in self.db.get_data('category', 'name', 'id', self.category):
                return -1
            if dup_num == 1:  # 겹치는게 하나 있으면 -> 그거 에러테이블에 표시해. 코드 겹친다고
                dup_id = self.db.get_data('product', 'id', 'code', self.code)
                dup_url = self.db.get_data('product', 'url', 'code', self.code)
                self.fill_err_product('same_code_error', dup_url, product_id=dup_id, etc=self.code)
            # 그리고나서는 product table 에만 넣고 나머지 과정은 패스한다. 에러테이블에 표시해놨으니깐.
            product_id = self.db.insert_sub_data('product', self.col, self.val)
            self.fill_err_product('same_code_error', self.url, product_id=product_id, etc=self.code)
            return -1
        return product_id


