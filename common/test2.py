import browser.chrome as chrome
# import pandas as pd
# from sitePage.sitePage import SitePage
from musinsaProduct.productPage import ProductPage
from settings.database import DataBase


sql = "SELECT category, url from err_product where category < 39 and error_code = 'basic_info_error';"
d = DataBase('crawling_db')
cate_url_list = d.etc_command(sql)

ProductPage.site_id = 1
ProductPage.site_name = 'musinsa'
ch = chrome.Chrome()

for cate_url in cate_url_list:
    cate = cate_url[0]
    p_url = cate_url[1]

    dup = d.is_duplication('product', 'url', p_url)
    if dup > 0:
        rec = True
    else:
        rec = False

    ch.move(p_url)

    p = ProductPage(p_url, ch, cate)
    res = p.crawling_by_product(rec)
    print(f'{res}: {p_url}')
    p.db.update_data('err_product', 'status', 'solved', 'url', p_url)


# url = 'https://store.musinsa.com/app/'
#
# ch = Chrome()
# s = SitePage(url, ch)
#
# ch.move(url)
#
# cate_id = 2
# cate_url = 'https://store.musinsa.com/app/items/lists/001010'
#
#
# try:
#     s.cate_crawling(cate_id, cate_url)
# finally:
#     ch.driver.close()
