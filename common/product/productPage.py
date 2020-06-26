from product.productInfo import ProductInfo
from product.productImage import ProductImage
from product.productSize import ProductSize
from settings.myError import NoSizeTableError


class ProductPage(ProductInfo, ProductImage, ProductSize):

    def crawling_by_product(self, rec):
        # 기본정보 처리
        try:
            if rec:  # 재크롤링이면 insert할 필요가 없음. product_id 만 받아오면 된다.
                product_id = self.db.get_data('product', 'id', 'url', self.url)
            else:       # 이 상품 첫 크롤링
                product_id = self.product_insert_2_db()

            # 위 과정에서 나올 수 있는 특이 케이스(에러로 추정)
            if product_id is None:
                raise ValueError
            if product_id == -1:    # -1을 리턴한 경우는 이미 그 과정에서 에러처리를 했다.
                return -1
        except Exception as ex:
            self.fill_err_product('basic_info_error', self.url, etc=f'{type(ex)}: {ex}')
            return -1

        # 이미지 저장
        try:
            self.save_image(product_id)
        except Exception as ex:
            self.fill_err_product('image_error', self.url, product_id=product_id, etc=f'{type(ex)}: {ex}')
            return -2

        # 사이즈정보 저장
        try:
            self.get_size_info(product_id)
        except NoSizeTableError:
            self.fill_err_product('no_size_table_error', self.url, product_id=product_id)
        except Exception as ex:
            self.fill_err_product('size_error', self.url, product_id=product_id, etc=f'{type(ex)}: {ex}')
            return -3

        # 상품 긁는 모든 과정을 거쳤다고 표시
        self.db.update_data('product', 'all_fin', 'True', 'id', product_id)
        return 0
