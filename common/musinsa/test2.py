import page
import re

url = 'https://store.musinsa.com/app/product/detail/1231241/0'
# url2 = 'https://store.musinsa.com/app/product/detail/1219047/0'

p = page.ProductPage(url)

info_mass = p.html.find('ul', {'class': 'product_article'})  # table 일단 찾아
info_list = info_mass.find_all('li')  # 표에 있는 항목들 가져와
amt_idx = len(info_list)  # 표에서 가져올 항목의 개수

# tags = info_list[amt_idx - 1].p.text
tags = '#가재준'
# print(tags)
tags = re.compile('\\n').sub('', tags)
tags = re.compile('^#').sub('', tags)
print(tags)
tag_list = re.split('#', tags)

print(tag_list)
