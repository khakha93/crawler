from category.productUrls import ProductUrls as Pu
from .productPage import ProductPage


class ProductUrls(Pu):

    # 추상화: productUrls 에 채워지는 부분
    def product_crawling(self, product_url, rec):
        ProductPage(product_url, self.category).crawling_by_product(rec)
        # raise NotImplementedError

    def get_product_urls(self):
        product_urls = []

        product_li_tags = self.html.find('ul', {'class': 'prdList grid3'}).find_all('li')

        for pro_tag in product_li_tags:
            try:
                product_urls.append('https://mutnam.com' + pro_tag.find('a')['href'])
            except TypeError:
                pass
        return product_urls

    def after_check(self, product_url, rec):
        # 에러포인트 표시: 에러 상품의 url
        self.db.update_data('history', 'err_url', product_url, 'category', self.category)

        self.product_crawling(product_url, rec)

        if self.flag:
            self.after_first_product_crawling(product_url)

        return



