from category.productUrls import ProductUrls as Pu
from .productPage import ProductPage


class ProductUrls(Pu):

    # 추상화: productUrls 에 채워지는 부분
    def product_crawling(self, product_url, rec):
        ProductPage(product_url, self.ch, self.category).crawling_by_product(rec)
        # raise NotImplementedError

