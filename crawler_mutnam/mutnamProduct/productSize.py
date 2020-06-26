from product.productSize import ProductSize as Ps
import pandas as pd
import re
import settings.matrix as mat
from settings.myError import NoSizeTableError


class ProductSize(Ps):

    # 가져온 사이즈표에서 필요없는 부분은 버린다.
    def get_size_info(self, product_id):

        table_type = self.fill_size_table()
        if table_type == 1:
            self.size_table = mat.transpose_matrix(self.size_table)

        # mat.print_matrix(self.size_table)
        # return
        col = ['product_id', 'dsc_idx', 'bulk']

        # 필요없는 부분 자르기
        self.cut_table(col)

        # 디비에 넣기
        self.insert_2_db(product_id, 1, col)

        return

    # fill size table
    def fill_size_table(self):
        table_type = 1
        t_tag = self.html.find('table', {'class': 'tbl_size'})

        if t_tag is None:
            table_type = 2
            try:
                t_tag = self.html.find('div', {'class': 'box_tem'}).table
            except AttributeError:
                t_tag = self.html.find('table', {'class': 'table_style_tem'})

        t_head_tag = t_tag.find('thead').find_all('th')
        temp = [t.text for t in t_head_tag]
        self.size_table.append(temp)

        row_tags = t_tag.find('tbody').find_all('tr')
        for row_tag in row_tags:
            row_values = []
            for cell in row_tag.children:
                try:
                    row_values.append(cell.text)
                except AttributeError:
                    pass
            self.size_table.append(row_values)
        return table_type

    def insert_2_db(self, product_id, idx, col):
        # DB 에 넣기
        for row in self.size_table:
            val = [product_id, idx]
            val.extend(row)
            # print(f'{col}: {val}')
            self.db.insert_sub_data('size_info', col, val)
        return

    def cut_table(self, col):

        dic = {'어깨': 'shoulder', '가슴': 'chest', '소매': 'sleeve', '팔통': 'arm_width', '암홀': 'arm_hole',
               '밑단': 'hem', '허리': 'waist', '엉덩이': 'hip', '허벅지': 'thigh', '밑위': 'croth', '총기장': 'total_length'}

        # 무신사 dic 로 columns 채우고, 필요없는 부분은 지워버린다.
        for j in reversed(range(1, len(self.size_table[0]))):
            try:
                col.insert(3, dic[self.size_table[0][j]])
            except KeyError as key:
                print(f'{key} 는 사이즈표에서 안 가져옴')
                for row in self.size_table:
                    del row[j]

        del self.size_table[0]

        # 가져올 칼럼이 없으면 노사이즈 에러
        if len(self.size_table[0]) <= 1:
            raise NoSizeTableError

        # row 가 하나도 안 남으면 노사이즈 에러
        if len(self.size_table) == 0:
            raise NoSizeTableError


