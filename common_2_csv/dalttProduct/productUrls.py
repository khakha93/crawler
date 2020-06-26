from category.productUrls import ProductUrls as Pu
from .productPage import ProductPage


class ProductUrls(Pu):

    # 추상화: productUrls 에 채워지는 부분
    def product_crawling(self, product_url, rec):
        ProductPage(product_url, self.ch, self.category).crawling_by_product(rec)
        # raise NotImplementedError

    def check_duplication(self, product_url):
        # url 이 이미 디비에 있는 경우
        if self.db.is_duplication('product', 'url', product_url) > 0:
            # DB에 있는 거랑 카테고리가 다르면
            if self.db.get_data('product', 'category', 'url', product_url) != self.category:
                p_id = self.db.get_data('product', 'id', 'url', product_url)
                self.fill_err_product('category_match_error', product_url, product_id=p_id)

            # 모든 검사를 끝낸 경우 : 또 긁을 필요는 없지
            if self.db.get_data('product', 'all_fin', 'url', product_url) == 'True':
                # Case 1 인 경우 이 상품만 패스
                if self.cr_type == 1:
                    return 1
                # case 2, case 3 인 경우
                else:
                    # 이게 end_url 이면, 카테고리 전체를 끝내야한다
                    if product_url == self.end_url:
                        print('이후 모든 상품은 패스')
                        return 2
                    else:
                        print('어쩌다 꼬여서 중복')
                        return 1
            else:       # 긁긴 했는데 중간에 끊긴 경우 : 다시 크롤링해줘야함
                return 3

        else:           # 디비에 없는 경우: 그냥 크롤링 해주면 된다.
            print('없는 상품이므로 크롤링')
            return 4



