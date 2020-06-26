from product.productSize import ProductSize as Ps
from settings.myError import NoSizeTableError
import re
# from browser import chrome
# import settings.matrix as mat


class ProductSize(Ps):

    def fill_t_head(self, t_head_web_element):
        # 사이즈테이블 채우는 구간
        t_head = t_head_web_element.find_elements_by_xpath('./tr/th')
        if len(t_head) == 0:
            raise NoSizeTableError
        self.size_table.append([re.compile('\\d\\.').sub('', e.text) for e in t_head])  # 첫번째 row 를 추가한다.
        return

    def get_size_info(self, product_id):
        print('Get size from size_table')
        # 그냥 일단 전부 가져와서 2차원배열로 만들자

        # 테이블을 전부 찾아논다
        t_heads = self.ch.driver.find_elements_by_xpath(self.xpath_info.t_head_xpath)
        t_bodies = self.ch.driver.find_elements_by_xpath(self.xpath_info.t_body_xpath)

        num = len(t_heads)
        if num == 0:
            self.fill_err_product('no_edibot', self.url, product_id, 'No edibot-fit size table')

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


