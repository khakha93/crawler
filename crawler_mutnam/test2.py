from mutnamProduct.productPage import ProductPage
from settings.database import DataBase
from page import Page
from settings.matrix import print_matrix

url = 'https://mutnam.com/product/detail.html?product_no=32394&cate_no=123&display_group=1'

p = ProductPage(url, 365)
# p.get_size_info(127065)

t_tag = p.html.select('#tab1 > div.detail_info_area > div:nth-child(3) > table:nth-child(108)')[0]

t_head_tag = t_tag.find('thead').find_all('th')
temp = [t.text for t in t_head_tag]
p.size_table.append(temp)

row_tags = t_tag.find('tbody').find_all('tr')
for row_tag in row_tags:
    row_values = []
    for cell in row_tag.children:
        try:
            row_values.append(cell.text)
        except AttributeError:
            pass
    p.size_table.append(row_values)

print_matrix(p.size_table)

col = ['product_id', 'dsc_idx', 'bulk']

p.cut_table(col)

for row in p.size_table:
    val = [127065, 1]
    val.extend(row)
    # print(f'{col}: {val}')
    p.db.insert_sub_data('size_info', col, val)
