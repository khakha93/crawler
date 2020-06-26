from browser import chrome
from browser.chrome import sel_exceptions
from page import Page
from sitePage.siteInformation import CateXpathInfo
from browser.circleXpath import CircleXpath
import re


# <$$$> 이 파일 이름이 맘에 안 들어..
# 지정한 사이트 url, 과 카테고리의 xpath 정보를 토대로 카테고리의 이름과 그 카테고리의 url을 구하기 위한 클래스
class CategoryInformation(Page):
    def __init__(self, url, ch: chrome.Chrome, name):
        super().__init__(url, ch)
        self.site_id = self.enroll_site(name)
        self.site_name = self.db.get_data('site', 'name', 'id', self.site_id)
        self.urls = []
        self.cate_names = []

        # 해당 사이트의 카테고리의 xpath 관한 정보를 가진 클래스를 그대로 가져온다
        self.cate_xpath_info = CateXpathInfo(self.site_id)
        # 이렇게 넣어도 되고 다중상속 처리해도 될 듯. 뭐가 나은지는 몰라.
        return

    # 사이트를 데이터베이스의 site 테이블에 넣는 과정
    def enroll_site(self, name):
        site_id = self.db.insert_sub_data('site', ['url', 'name'], [self.url, name])
        if site_id == -1:       # 이미 있는 데이터면 -1을 리턴
            print(f'Already enrolled. site name: {name}')
            site_id = self.db.get_data('site', 'id', 'url', self.url)
        return site_id

    # 부모 카테고리의 xpath, text 를 받아서 해당 depth 카테고리의 xpath 들을 얻는 과정 ('','',1) 로 호출
    def drive_next_cate(self, parent_cate_text, parent_category_xpath, dep):
        # 최종 카테고리에 도달한 후에는, url 이랑 텍스트를 가져온다.
        if dep > self.cate_xpath_info.n:
            self.reach_final_cate(parent_category_xpath, parent_cate_text)
            return
        else:
            # 클릭이 필요한지 확인 후 클릭.
            need_c = self.cate_xpath_info.get_need_click(dep)
            if need_c:
                self.ch.click_by_xpath(parent_category_xpath)

            # 해당 뎁스의 xpath를 가져온 후 다음 뎁스로 넘어감.
            self.drive_content(parent_cate_text, parent_category_xpath, dep)

            if need_c:  # 클릭해야하면 여러가지 경우가 나올 수 있으나 나중에 고려
                # self.ch.move_back()
                pass

    def drive_content(self, parent_cate_text, parent_category_xpath, dep):
        # 해당 댑스 카테고리의 xpath 들을 구하기
        cir_xpath_elements = self.cate_xpath_info.get_xpath_elements_cate_n(dep, parent_category_xpath)
        cate_n_x_paths = CircleXpath(self.ch, cir_xpath_elements).completed_xpath_s

        # <$$$> no such elements 에러 났을 경우 어떻게????. 아직 이런 경우는 없음.

        # 지정한 구간의 xpath 만 다음 카테고리로 넘어간다.
        used_range = self.cate_xpath_info.get_used_range(cate_n_x_paths, dep)

        # <$$$> range 돌게 없으면????? : 달트에 해당. 카테고리 뎁스가 일정하지가 않다.
        if len(used_range) == 0:
            self.reach_final_cate(parent_category_xpath, parent_cate_text)

        for idx_cate in used_range:
            cate_n_xpath = cate_n_x_paths[idx_cate]
            # 여기서 텍스트 가져와야함
            try:
                added_text = self.ch.driver.find_element_by_xpath(cate_n_xpath).text
                added_text = re.compile('[\\n\\r]').sub('', added_text)
                if added_text == '':
                    cate_n_text = f'{parent_cate_text}>None[{str(idx_cate).zfill(2)}]'
                else:
                    cate_n_text = f'{parent_cate_text}>{added_text}'
            except sel_exceptions.NoSuchElementException:
                cate_n_text = f'{parent_cate_text}>None[{str(idx_cate).zfill(2)}]'

            # 해당 뎁스의 카테고리와 xpath 들을 구했으니, 이를 이용해 또 다음 뎁스로 넘어간다
            self.drive_next_cate(cate_n_text, cate_n_x_paths[idx_cate], dep + 1)
        return

    # 최종 카테고리에 도달한 후에 할 것들: 카테고리의 url을 구해서 이름과 함께 저장.
    def reach_final_cate(self, cate_xpath, cate_text):
        # print('reach final category')
        cate_url = self.ch.get_url(cate_xpath)
        if cate_url == 'NSE':
            print('no such element')
            cate_url = self.ch.driver.current_url
        self.urls.append(cate_url)
        self.cate_names.append(cate_text)
        return

    # 내 뎁스의 카테고리 텍스트, xpath 받음 ('','',0) 으로 호출
    # def drive_next_cate_v2(self, cate_text, cate_xpath, dep):
    #
    #     # 최종 카테고리에 도달하면, url 이랑 텍스트를 저장한다.
    #     if dep == self.cate_xpath_info.n:
    #         cate_url = self.ch.get_url(cate_text)
    #         if cate_url == 'NSE':
    #             print('no such element')
    #             cate_url = self.ch.driver.current_url
    #         self.urls.append(cate_url)
    #         self.cate_names.append(cate_text)
    #         return
    #
    #     # dep category 의 정보 가져오기 : 이전 카테고리 정보, 여기서 얼마나 빠지고, 얼마나 붙고, 움직이는 부분, 뒤에 추가로 붙는 부분
    #     else:
    #         # need_click 해당 뎁스를 얻기위해서는 클릭이 필요하냐?
    #         need_click = self.cate_xpath_info.get_need_click(dep+1)
    #         if need_click:  # 클릭해야하면 여러가지 경우가 나올 수 있으나 나중에 고려
    #             self.ch.click_by_xpath(cate_text)
    #
    #         # 다음 댑스의 카테고리 xpath 들 구하기
    #         next_cate_x_paths = self.cate_xpath_info.get_x_paths_cate_n(dep+1, cate_xpath)
    #
    #         # 지정한 구간의 xpath 만 다음 카테고리로 넘어간다.
    #         used_range = self.cate_xpath_info.get_used_range(next_cate_x_paths, dep+1)
    #         for idx_cate in used_range:
    #             next_cate_xpath = next_cate_x_paths[idx_cate]
    #             # 여기서 텍스트 가져와야함
    #             try:
    #                 next_cate_text = f'{cate_text}>{self.ch.driver.find_element_by_xpath(next_cate_xpath).text}'
    #             except sel_exceptions.NoSuchElementException:
    #                 next_cate_text = f'{cate_text}>None[{str(idx_cate).zfill(2)}]'
    #             self.drive_next_cate(next_cate_text, next_cate_x_paths[idx_cate], dep+1)
    #
    #         if need_click:  # 클릭해야하면 여러가지 경우가 나올 수 있으나 나중에 고려
    #             self.ch.move_back()

# # DB 에 넣기
# cate_id = self.db.insert_sub_data('category', ['name', 'site', 'cate_url'],
#                                   [n_cate_text, self.site_id, cate_url])
# if cate_id == -1:
#     cate_id = self.db.get_data('category', 'id', 'name', n_cate_text)
# self.db.insert_sub_data('history', ['category'], [cate_id])

# category text 가져오는 부분에서 불필요한 거
# except AttributeError:
#     n_cate_text = cate_text
# finally:
#     print(n_cate_text)

# site id 가져오기
# self.site_id = self.db.insert_sub_data('site', ['name', 'url'], [site_name, self.url])
# if self.site_id == -1:
#     self.site_id = self.db.get_data('site', 'id', 'url', self.url)

# dep category 의 정보 가져오기 : 이전 카테고리 정보, 여기서 얼마나 빠지고, 얼마나 붙고, 움직이는 부분, 뒤에 추가로 붙는 부분




