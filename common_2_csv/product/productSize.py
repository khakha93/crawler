import settings.matrix as matrix
from .productSizeTable import ProductSizeTable
from settings.myError import NoSizeTableError


class ProductSize(ProductSizeTable):

    def get_size_info(self, product_id):
        print('Get size from size_table')
        # 그냥 일단 전부 가져와서 2차원배열로 만들자

        # 테이블을 전부 찾아논다
        t_heads = self.ch.driver.find_elements_by_xpath(self.xpath_info.t_head_xpath)
        t_bodies = self.ch.driver.find_elements_by_xpath(self.xpath_info.t_body_xpath)

        num = len(t_heads)
        if num == 0:
            raise NoSizeTableError

        # 첫번째 사이즈표부터 채우고 다시 size_table 을 리셋한다.
        for i in range(num):

            # 사이즈표를 채운다
            self.fill_table(t_heads[i], t_bodies[i])

            # 테이블을 확인 후 필요하면 전치
            try:
                self.conf_n_trans()
            except IndexError:
                self.fill_err_product('size_error', self.url, product_id, 'Is not matrix')
            finally:
                # 테이블 가공 후에 디비에 저장
                self.cut_n_insert(product_id, i)
                # 사이즈표 리셋 : 다음 사이즈표를 위해서
                del self.size_table[:]
        return

    def conf_n_trans(self):
        # 확인 작업 & 전치 필요하면 전치시킨다
        try:
            if not matrix.confirm_matrix(self.size_table):
                pass
                # raise IndexError
        finally:
            if self.xpath_info.need_trans:
                self.size_table = matrix.transpose_matrix(self.size_table)
        return

    def cut_n_insert(self, product_id, i):
        # 확인해서 문제가 있어도, 임의처리해서 디비에 넣긴 하자.
        col = ['product_id', 'dsc_idx', 'bulk']
        # DB 에 넣기 위해 column, value 맞춰주기
        self.cut_table(col)
        # DB 에 넣기
        self.insert_2_db(product_id, i + 1, col)
        return

    def insert_2_db(self, product_id, idx, col):
        # DB 에 넣기
        for row in self.size_table:
            val = [product_id, idx]
            val.extend(row)
            # print(f'{col}: {val}')
            self.db.insert_sub_data('size_info', col, val)
        return
