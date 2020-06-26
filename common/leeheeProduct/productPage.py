from product.productPage import ProductPage as Pp
from leeheeProduct.productInfo import ProductInfo
from leeheeProduct.productImage import ProductImage
from leeheeProduct.productSize import ProductSize


class ProductPage(ProductInfo, ProductImage, ProductSize, Pp):
    pass

    # def crawling_by_product(self, rec):
    #     # 기본정보 처리
    #     try:
    #         if rec:  # 재크롤링이면 insert할 필요가 없음. product_id 만 받아오면 된다.
    #             product_id = self.db.get_data('product', 'id', 'url', self.url)
    #             if product_id is None:
    #                 raise ValueError
    #         else:       # 이 상품 첫 크롤링
    #             product_id = self.get_basic_info()
    #             if product_id == -1:        # 뭔가 오류가 았다는 뜻(에러 처리는 이미 다 함)
    #                 return -1
    #     except Exception as ex:
    #         self.fill_err_product('basic_info_error', self.url, etc=f'{type(ex)}: {ex}')
    #         return -1
    #
    #     # 이미지 저장
    #     try:
    #         self.save_image(product_id)
    #     except Exception as ex:
    #         self.fill_err_product('image_error', self.url, product_id=product_id, etc=f'{type(ex)}: {ex}')
    #         return -2
    #
    #     # 사이즈정보 저장설
    #     try:
    #         self.get_size_info(product_id)
    #     except NoSizeTableError:
    #         self.fill_err_product('no_size__table_error', self.url, product_id=product_id)
    #     except Exception as ex:
    #         self.fill_err_product('size_error', self.url, product_id=product_id, etc=f'{type(ex)}: {ex}')
    #         return -3
    #
    #     # 상품 긁는 모든 과정을 거쳤다고 표시
    #     self.db.update_data('product', 'all_fin', 'True', 'id', product_id)
    #     return 0
