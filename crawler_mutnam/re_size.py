from settings.database import DataBase
from mutnamProduct.productPage import ProductPage

# 사이즈표 안 긁어서 사이즈표만 다시 긁어야함. 그래서 만든 파일임!!

# 디비에서 상품 읽어
d = DataBase('crawling_db')
sql = 'select id, category, url, category from product where category > 356 and id > 121079'
res = d.etc_command(sql)

# 상품갯수
num = len(res)
z = list(zip(*res))
# 상품 id 들
p_ids = z[0]
# 상품 category 들
p_categories = z[1]
# 상품 url 들
p_urls = z[2]

# 이제 사이즈표만 가져와서 넣으면 돼
for i in range(num):
    p = ProductPage(p_urls[i], p_categories[i])
    p.get_size_info(p_ids[i])




