from product.productPage import ProductPage as Pp
from .productInfo import ProductInfo
from .productImage import ProductImage
from .productSize import ProductSize

import csv
import re


def info_2_list(col, val, added_row):
    col_idx = {'code': 0, 'auto_code': 1, 'category': 4, 'name': 7, 'commodity_price': 21, 'selling_price': 22,
               'option': 36, 'brand': 52, 'big': 46, 'medium': 47, 'tiny': 48, 'small': 49}

    for i in range(len(col)):
        added_row[col_idx[col[i]]] = val[i]
    return


def list_2_csv(added_row):
    f = open('/mnt/sdb/crawling/saved_files/product.csv', 'a', newline='')
    wr = csv.writer(f)
    wr.writerow(added_row)
    f.close()
    print(added_row)
    return


def fill_static_values():
    return


class ProductPage(ProductInfo, ProductImage, ProductSize, Pp):

    def crawling_by_product(self, rec):
        added_row = ['' for i in range(90)]

        # 기본정보 처리: 기본정보 가져와서 리스트로 만들고 csv파일에 추가한다.
        self.get_basic_info()
        # brand, url 은 뺀다
        # info_2_list(self.col[1:-1], self.val[1:-1], added_row)

        # 이미지 처리: 이미지 src를 가져와서 파일로 저장하고 src 는 csv파일 추가되는 부분에 포함되야함
        # img_types = self.save_image(self.code)
        # cut_img_src_s = [re.compile('^http.+(big|medium|small|tiny)/').sub('', src) for src in self.img_src_s]
        # info_2_csv(img_types, cut_img_src_s, added_row)

        # 사이즈표
        # 사이즈표를 가져오는건 만들었으나, 사이즈표는 여기서 필요 없다.
        # self.fill_size_table()

        # csv 로 저장
        list_2_csv(added_row)
        return










