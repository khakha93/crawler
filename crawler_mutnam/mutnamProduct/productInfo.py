import re

from product.productPage import ProductInfo as Pi


class ProductInfo(Pi):
    def get_basic_info(self):
        # 상품코드 가져오기
        all_text = str(self.html.find('body'))
        try:
            need_text = re.compile("option_stock_data = '{\\\\\".+?(?=\\w{4}\\\\)").search(all_text).group()
            self.code = need_text.split('\\"')[1]
        except AttributeError:
            need_text = re.compile("product_code = '.+?';").search(all_text).group()
            self.code = re.compile("'([A-Z\\d]+)'").search(need_text).group()[1:-1]

        name = self.html.find('div', {'class': 'headingArea'}).text
        name = re.compile('[\\n\\r\\t]').sub('', name)
        name = re.compile('\\s$').sub('', name)

        # 판매가
        selling_price = self.html.find('strong', {'id': 'span_product_price_text'}).text
        selling_price = re.compile('[,\\d]+?(?=원)').search(selling_price).group()
        selling_price = re.compile(',').sub('', selling_price)

        # 상품가
        # commodity_price = round(selling_price*10/11)

        # option 처리
        option_text = ''
        options = self.html.find('tbody', {'class': 'xans-element- xans-product xans-product-option xans-record-'}).find_all('tr')
        # 마지막 원소는 삭제해줘야함
        options.pop()

        for opt in options:
            if option_text != '':
                option_text += '//'

            opt_name = opt.th.text
            # print(f'옵션: {opt_name}')
            opt_value_tags = opt.find_all('option')[2:]
            opt_values = [v.text for v in opt_value_tags]
            opt_value_text = repr(opt_values)
            opt_value_text = re.compile('\\[').sub('', opt_value_text)
            opt_value_text = re.compile('\\]').sub('', opt_value_text)
            opt_value_text = re.compile('\'').sub('', opt_value_text)
            opt_value_text = re.compile(', ').sub('|', opt_value_text)

            added_text = f'{opt_name}{{{opt_value_text}}}'
            option_text += added_text

        # 들어갈 칼럼 & 값
        self.col = ['brand', 'category', 'code', 'name', 'price', 'option_info', 'url']
        self.val = ['mutnam', self.category, self.code, name, selling_price, option_text[:199], self.url]

        return


