from unicelebProduct.productPage import ProductPage
from browser.chrome import Chrome
from page import Page
from browser.chrome import Chrome
import re


ch = Chrome()

# p_url = 'http://www.uniceleb.com/product/detail.html?product_no=259&cate_no=42&display_group=1'
p_url = 'http://www.uniceleb.com/product/detail.html?product_no=245&cate_no=24&display_group=1'
# 상품페이지 이동
ch.move(p_url)

ProductPage.site_id = 114

p = ProductPage(p_url, ch, 42)

p.get_basic_info()


ch.driver.close()

# txt = "option_stock_data = '{\"P00000JY000A"
# print(txt)
#
# need_text = re.compile("option_stock_data = '{\".+?(?=000A)").search(txt)
#
# print(need_text)

