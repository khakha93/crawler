from category.productUrls import ProductUrls as Pu
from .productPage import ProductPage


def text_2_file(text):
    f = open('/mnt/sdb/crawling/saved_files/error.txt', 'a')
    f.write(text)
    f.close()

    # with 문으로 쓰면 더 멋있겠다.
    # with open("foo.txt", "w") as f:
    #     f.write("Life is too short, you need python")
    return


class ProductUrls(Pu):

    # 추상화: productUrls 에 채워지는 부분
    def product_crawling(self, product_url, rec):
        try:
            self.ch.move(product_url)
            ProductPage(product_url, self.ch, self.category).crawling_by_product(rec)
        except Exception as ex:
            text_2_file(f'{product_url}::{type(ex)}::{ex}\n')
            self.fill_err_product('error', product_url)
        # raise NotImplementedError

    def get_product_urls(self):
        product_urls = []

        product_li_tags = self.html.find('ul', {'class': 'prdList grid4'}).find_all('li')

        for pro_tag in product_li_tags:
            try:
                product_urls.append('http://www.uniceleb.com' + pro_tag.find('a')['href'])
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



