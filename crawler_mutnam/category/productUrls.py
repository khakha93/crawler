from category.listedPage import ListedPage


class ProductUrls(ListedPage):

    # 카테고리 전체를 끝내야하면 -1을 리턴, 아니면 0을 리턴한다
    def crawling_in_product_urls(self):

        print(f'[Crawling List] {self.page_num}\'th ListedPage')

        # 에러포인트 표시: 몇번째 페이지인지 우선 표시
        if not self.flag:
            self.db.update_data('history', 'err_page', self.page_num, 'category', self.category)

        # <선 수행> case3: error_point 로 이동, 근데 처음 페이지에서만 하면 된다.
        str_idx = self.get_str_idx()
        pro_num = len(self.product_urls)

        # 상품별로 할 것
        for pro_idx in range(str_idx, pro_num):
            print(f'\n[Crawling Product] {self.page_num} page {pro_idx} 번째')
            product_url = self.product_urls[pro_idx]

            # *****************제일 중요**************************** 중복에 관해 처리
            switch = self.check_duplication(product_url)

            if switch == 1:
                continue
            elif switch == 2:
                # 카테고리 전체를 끝내야함
                return -1
            elif switch == 3:
                rec = True
            else:
                rec = False

            self.after_check(product_url, rec)
            # print(f'{pro_idx}번째 상품 긁었다고 치자!!!')
        return 0

    def after_check(self, product_url, rec):
        raise NotImplementedError
        # # 에러포인트 표시: 에러 상품의 url
        # self.db.update_data('history', 'err_url', product_url, 'category', self.category)
        #
        # # Product page 객체 생성 후 크롤링
        # self.ch.move(product_url)
        # self.product_crawling(product_url, rec)
        #
        # self.ch.move_back()
        #
        # # 첫 상품 긁은 후 처리할 것: 최신상품 기억, 비정상종료라고 표시
        # if self.flag:
        #     self.after_first_product_crawling(product_url)
        # return

    def product_crawling(self, product_url, rec):
        # ProductPage(product_url, self.ch, self.category).crawling_by_product(rec)
        raise NotImplementedError

    def get_str_idx(self):
        # <선 수행> case3: error_point 로 이동, 근데 처음 페이지에서만 하면 된다.
        # flag 가 True 일 때만 에러포인트를 찾아가게했는데, 논리상 딱 맞아떨어지지는 않는다
        str_idx = 0
        if self.cr_type == 3 and self.flag:
            try:
                # error url 의 인덱스를 찾는다
                err_url = self.db.get_data('history', 'err_url', 'category', self.category)
                str_idx = self.product_urls.index(err_url)
            except Exception as ex:
                print(f'{type(ex)} : {ex}')
                pass
        return str_idx


