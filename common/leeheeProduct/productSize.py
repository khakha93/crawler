from product.productSize import ProductSize as Ps
import settings.matrix as matrix
import re

from settings.myError import NoSizeTableError


class ProductSize(Ps):
    def get_size_info(self, product_id):

        t_body = self.ch.driver.find_element_by_xpath(self.xpath_info.t_body_xpath)

        self.fill_t_body(t_body)

        # matrix.print_matrix(self.size_table)

        # 테이블을 확인 후 필요하면 전치
        try:
            self.conf_n_trans()
        except IndexError:
            self.fill_err_product('size_error', self.url, product_id, 'Is not matrix')
        finally:
            # 테이블 가공 후에 디비에 저장
            self.cut_n_insert(product_id, 0)
            # 사이즈표 리셋 : 다음 사이즈표를 위해서
            del self.size_table[:]
        return

    def cut_table(self, col):
        # 무신사 dic 로 columns 채우고, 필요없는 부분은 지워버린다.
        for j in reversed(range(1, len(self.size_table[0]))):
            try:
                col.append(self.xpath_info.dic[self.size_table[0][j]])
            except KeyError as key:
                print(f'{key} 는 사이즈표에서 안 가져옴')
                for row in self.size_table:
                    del row[j]
        # 가져올 칼럼이 없으면 노사이즈 에러
        if len(self.size_table[0]) <= 1:
            raise NoSizeTableError

        for r in reversed(range(len(self.size_table))):
            bulk = self.size_table[r][0]
            bulk = re.compile('\\(.+\\)').sub('', bulk)
            if bulk not in self.xpath_info.size_list:
                del self.size_table[r]

        # row 가 하나도 안 남으면 노사이즈 에러
        if len(self.size_table) == 0:
            raise NoSizeTableError

