from product.productSize import ProductSize as Ps
from settings.myError import NoSizeTableError
# from browser import chrome
# import settings.matrix as mat


class ProductSize(Ps):

    # 가져온 사이즈표에서 필요없는 부분은 버린다.
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

        # for r in reversed(range(len(self.size_table))):
        #     if self.size_table[r][0] not in self.xpath_info.size_list:
        #         del self.size_table[r]

        del self.size_table[0]

        # row 가 하나도 안 남으면 노사이즈 에러
        if len(self.size_table) == 0:
            raise NoSizeTableError

    pass


