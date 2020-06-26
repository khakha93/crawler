import browser.chrome as chrome
from musinsaProduct.productPage import ProductPage

p_url = 'https://store.musinsa.com/app/product/detail/485145/0'
ch = chrome.Chrome()
ch.move(p_url)

try:
    ProductPage.site_id = 1
    p = ProductPage(p_url, ch, 1)

    res = p.crawling_by_product(False)
    print(res)
    # for src in p.get_size_info:
    #     print(src)
finally:
    ch.driver.close()


# 세트상품 예시
