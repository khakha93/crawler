from browser import chrome
from page import ExtendedPage


class ProductInfo(ExtendedPage):

    def __init__(self, url, ch: chrome.Chrome, category):
        super().__init__(url, ch, category)
        self.code = None
        self.col = None
        self.val = None
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
            if dup_num == 1:  # 겹치는게 하나 있으면 -> 그거 에러테이블에 표시해. 코드 겹친다고
                self.copy_product_2_err_product()
            # 그리고나서는 product table 에만 넣고 나머지 과정은 패스한다. 에러테이블에 표시해놨으니깐.
            product_id = self.db.insert_sub_data('product', self.col, self.val)
            self.fill_err_product('same_code_error', self.url, product_id=product_id, etc=self.code)
            return -1
        return product_id

    def copy_product_2_err_product(self):
        dup_id = self.db.get_data('product', 'id', 'code', self.code)
        dup_url = self.db.get_data('product', 'url', 'code', self.code)
        dup_cate = self.db.get_data('product', 'category', 'code', self.code)
        err_col = ['product_id', 'category', 'error_code', 'status', 'etc', 'url']
        err_val = [dup_id, dup_cate, 'same_code_error', 'not solved', self.code, dup_url]
        self.db.insert_sub_data('err_product', err_col, err_val)
        return

    # 상품의 기본 정보를 가져와 DB에 insert하기 위해 columns 와 그에 해당하는 values를 완성시킨다.
    def get_basic_info(self):
        raise NotImplementedError

