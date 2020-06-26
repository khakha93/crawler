import re
import csv

from product.productPage import ProductInfo as Pi


class ProductInfo(Pi):
    def get_basic_info(self):
        # 상품코드 가져오기
        all_text = str(self.html.find('body'))
        need_text = re.compile("option_stock_data = '{\\\\\".+?(?=000[A-Z]\\\\)").search(all_text).group()
        self.code = need_text.split('\\"')[1]

        # name
        name = self.html.find('div', {'class': 'infoArea'}).find('h2').text
        name = re.compile('[\\n\\r\\t]').sub('', name)
        name = re.compile('\\s$').sub('', name)

        # 판매가
        selling_price = self.html.find('strong', {'id': 'span_product_price_text'}).text
        selling_price = int(re.compile('[,원\\s$]').sub('', selling_price))

        # 힐인판매가 가져올 수 있는데 굳이...
        # strong, id = span_product_price_text 가져오면 됨

        # 상품가
        commodity_price = round(selling_price*10/11)

        # option 처리
        option_text = self.get_option_info()

        # 제품 설명
        detail = self.html.find('div', {'class': 'cont'}).text

        # 들어갈 칼럼 & 값
        self.col = ['brand', 'category', 'code', 'name', 'selling_price', 'commodity_price', 'option', 'url']
        self.val = ['uniceleb', self.category, self.code, name, selling_price, commodity_price, option_text, self.url]

        print(f'detail: {detail}')
        # detail
        # f = open('/mnt/sdb/crawling/saved_files/detail.csv', 'a', newline='')
        # wr = csv.writer(f)
        # wr.writerow([self.code, detail])
        # f.close()
        return

    def get_option_info(self):
        # 옵션 부분 차례대로 정보 가져오고 클릭까지
        option_text = ''
        # 일단 옵션 전부 찾는다
        options = self.ch.driver.find_elements_by_xpath(
            '//table[@class="xans-element- xans-product xans-product-option xans-record-"]/tbody')[1:-1]

        for opt in options:
            if option_text != '':
                option_text += '//'

            # 옵션 선택지 전부 가져온다.
            opt_name = opt.find_element_by_xpath('./tr/th').text
            # print(opt_name)
            opt_list = opt.find_elements_by_xpath('./tr/td/select/option')[2:]
            opt_values = [v.text for v in opt_list]
            # print(opt_values)

            opt_value_text = repr(opt_values)
            opt_value_text = re.compile('\\[').sub('', opt_value_text)
            opt_value_text = re.compile('\\]').sub('', opt_value_text)
            opt_value_text = re.compile('\'').sub('', opt_value_text)
            opt_value_text = re.compile(', ').sub('|', opt_value_text)

            added_text = f'{opt_name}{{{opt_value_text}}}'
            option_text += added_text

            # 옵션 중 하나 선택한다.
            opt_list[0].click()

        return option_text

    # 다 읽어와서 데이터프레임으로 추가하면 되는데, 데이터가 많아지면, 매우 비효율적일 것이다.
    # def save_2_csv(self):
    #     # df = pd.DataFrame(columns=self.col, data=[self.val])
    #     test_col = ['가재준', '가가가']
    #
    #     f = open('/mnt/sdb/crawling/crawler_mutnam/saved_files/basic.csv', 'a', newline='')
    #     wr = csv.writer(f)
    #     wr.writerow(test_col)
    #     f.close()
    #     return

# val_dic = {'brand': 'mutnam', 'category': self.category, 'code': self.code, 'name': name,
#            'selling_price': selling_price, 'commodity_price': commodity_price, 'option': option_text,
#            'url': self.url}


