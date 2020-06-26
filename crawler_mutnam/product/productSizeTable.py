from page import ExtendedPage
from sitePage.siteInformation import ProductXpathInfo
from settings.myError import NoSizeTableError


class ProductSizeTable(ExtendedPage):
    def __init__(self, url, category):
        super().__init__(url, category)
        self.size_table = []
        self.xpath_info = ProductXpathInfo(self.site_name)

    # 사이즈표의 내용을 size_table로 옯기는 과정
    def fill_table(self, t_head_web_element, t_body_web_element):
        # 거의 대부분의 table 속성은 thead, tbody로 나뉘어져있다.
        self.fill_t_head(t_head_web_element)
        self.fill_t_body(t_body_web_element)
        return

    def fill_t_head(self, t_head_web_element):
        # table의 첫번째 row가 thead
        t_head = t_head_web_element.find_elements_by_xpath('./tr/th')
        if len(t_head) == 0:
            raise NoSizeTableError

        self.size_table.append([e.text for e in t_head])
        return

    def fill_t_body(self, t_body_web_element):
        num_of_body_row = len(t_body_web_element.find_elements_by_xpath(f'./tr'))  # 남은 row 의 수

        for j in range(num_of_body_row):
            # th (가장 왼쪽 셀의 element) 를 row 에 넣어줌
            try:
                row = [t_body_web_element.find_element_by_xpath(f'./tr[{j + 1}]/th').text]
            except chrome.sel_exceptions.NoSuchElementException:  # <th> 가 없이  <td>만 있는 경우도 있음
                row = []
            # row 의 나머지 element(td)를 append 해줘야함
            td_list = t_body_web_element.find_elements_by_xpath(f'./tr[{j + 1}]/td')
            for td in td_list:
                try:
                    c = td.get_attribute('colspan')
                    col_span = int(c)
                    for s in range(col_span):
                        row.append(td.text)
                except TypeError:  # colspan 이 없는 경우
                    row.append(td.text)
            self.size_table.append(row)
        return

    # 가져온 사이즈표에서 필요없는 부분은 버린다.
    def cut_table(self, col):
        # 무신사 dic 로 columns 채우고, 필요없는 부분은 지워버린다.
        for j in reversed(range(1, len(self.size_table[0]))):
            try:
                col.append(self.xpath_info.dic[self.size_table[0][j]])
            except KeyError as key:
                print(f'{key} 는 사이즈표에서 안 가져옴')
                for row in self.size_table:
                    del row[j]
        # 가져올 칼럼이 없으면 노사이즈 에러
        if len(self.size_table[0]) <= 1:
            raise NoSizeTableError

        for r in reversed(range(len(self.size_table))):
            if self.size_table[r][0] not in self.xpath_info.size_list:
                del self.size_table[r]
        # row 가 하나도 안 남으면 노사이즈 에러
        if len(self.size_table) == 0:
            raise NoSizeTableError


