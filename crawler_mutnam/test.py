from sitePage.sitePage import SitePage
from settings.database import DataBase
from page import Page
from mutnamProduct.productPage import ProductPage
import re

# *************************************************************
# 상품코드 잘못 찾아서 못 긁은 애들 다시 긁는 코드임 건들면 안 됨!!!!!!!!!!
# *************************************************************

Page.site_id = 7
Page.site_name = 'mutnam'

d = DataBase('crawling_db')
sql = "select id, category, url from err_product where error_code = 'image_error' and category > 356 and status = 'not solved';"
res = d.etc_command(sql)

# 상품갯수
num = len(res)
z = list(zip(*res))
# err_product 의 id 기억
e_ids = z[0]
# 상품 category 들
p_categories = z[1]
# 상품 url 들
p_urls = z[2]

for i in range(num):
    p = ProductPage(p_urls[i], p_categories[i])
    p.crawling_by_product(True)
    p.db.update_data('err_product', 'status', 'solved', 'id', e_ids[i])
