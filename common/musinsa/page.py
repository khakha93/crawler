import os
import re
import urllib
import database
# import pandas as pd
import requests as rq
from bs4 import BeautifulSoup as Bs


class Page(object):
    original_url = None

    def __init__(self, url):
        self.url = url
        self.db = database.Database('crawling_musinsa')
        # BS 사용 선언
        res = rq.get(self.url)
        self.html = Bs(res.content, 'html.parser')


class InitPage(Page):
    def __init__(self, url):
        super().__init__(url)
        Page.original_url = url
        self.p_cate_num = 5

        # 카테고리 이름 목록 생성
        self.cate_names = []
        li = self.html.find_all('div', {'class': 'nav_category item_menu_btn'})
        print(len(li))
        for i in range(self.p_cate_num):
            t = re.compile('[\\n\\t]').sub('', li[i].div.text)
            t = re.compile('[a-zA-Z]+').match(t).group()    # 상위 카테고리 이름들
            self.cate_names.append(t)

        # 카테고리별 url 획득
        self.cate_urls = []
        sub_menu = self.html.find_all('div', {'class': 'item_sub_menu_all'})
        for i in range(self.p_cate_num):
            self.cate_urls.append(url[:-5] + sub_menu[i].a['href'])
        return

    def enroll_site(self, name):
        self.db.insert_sub_data('site', ['name', 'url'], [name, self.url])
        print('Enroll this site!')
        return

    def fill_history(self):     # 상위 카테고리 별로 크롤링할거라서 결과를 알려주는 테이블을 만들어준다
        for c in self.cate_names:
            self.db.insert_sub_data('history', ['category', 'is_first'], [c, 'True'])  # 디비에 넣는다
        print('Fill history table!!')
        return

    def make_cate_img_folder(self):        # 상위카테고리별 이미지 저장 폴더 생성
        try:    # 전체 이미지폴더
            if not os.path.isdir('image'):
                os.mkdir('image')
                print('make image folder')
            else:
                print('Image folder is already exist!!')
        except OSError:
            print('Failed to create image folder!!!!')
        for c in self.cate_names:   # 카테고리 이미지 폴더
            try:
                if not os.path.isdir(f'image/{c}'):
                    os.mkdir(f'image/{c}')
                    print('make category image folder')
                else:
                    print('Category image folder is already exist!!')
            except OSError:
                print('Failed to create category image folder!!!!')
        return


class ListPage(Page):
    def __init__(self, url):
        super().__init__(url)  # ***********이거 모름*****************************
        # 상품 개수, 총 페이지 수 필요
        mass = self.html.find('div', {'id': 'product_list'})  # 페이지에 있는 상품의 리스트
        product_list = mass.find_all('li', {'class': 'li_box'})
        self.product_list = [self.original_url[:-5] + p_list.find('div', {'class': 'list_img'}).a.get('href') for p_list
                             in product_list]
        self.amount_product = len(self.product_list)
        self.total_page = int(self.html.find('span', {'class': 'totalPagingNum'}).text)

    def get_total_product(self):
        text = self.html.find('span', {'class': 'counter box_num_goods'}).text
        num = (re.compile('\\d+,*\\d+').search(text).group())
        num = int(re.compile(',').sub('', num))
        return num


class ProductPage(Page):

    def get_price(self):
        price = self.html.find('span', {'id': 'goods_price'}).text
        price = re.compile('[\\r\\n\\t]+').sub('', price)
        return price

    def get_product_info2(self, cate_name):
        print("'get_product_info' method start!!!")
        print(f'product url : {self.url}')

        # 우측 상단 테이블 정보 담기
        col = []  # column of product table
        values = []  # value of product table

        # 준비과정 & 칼럼 만들기
        info_mass = self.html.find('ul', {'class': 'product_article'})  # table 일단 찾아
        try:
            info_list = info_mass.find_all('li')  # 표에 있는 항목들 가져와
        except AttributeError:  # 위에거 말고 이렇게 해야 되는거 있음 (무신사 스탠다드 어쩌구 하는 상품들)
            info_mass = info_mass.find_next('ul', {'class': 'product_article'})
            info_list = info_mass.find_all('li')

        change_eng = {'브랜드': 'brand', '품번': 'code', '시즌': 'season', '성별': 'sex', '인기도': 'popular', '누적판매': 'sales',
                      '좋아요': 'likes', '구매 후기': 'review'}
        # left_item = ('시즌', '성별', '인기도', '누적판매', '좋아요', '구매 후기')

        # brand & code
        clause = ['브랜드', '품번']
        for c in clause:
            if c in info_list[0].p.text:
                col.append(change_eng[c])
        brand_code_text = info_list[0].p.next_sibling.next_sibling.strong.text
        brand_code_text = re.compile('\\s').sub('', brand_code_text)
        brand_code_list = re.split('/', brand_code_text)
        for e in brand_code_list:
            values.append(e)

        # 코드는 식별자 역할을 하므로 따로 기억해야함
        code_idx = col.index('code')
        code = values[code_idx]

        # <<error table>> 준비
        err_col = ['code', 'cate_name', 'error_code', 'status', 'url']
        err_values = [code, cate_name, 'not_solved', self.url]  # error code 는 나중에 insert 할거임
        err_content = []  # 여기에 error 들을 담아서 error_code 로 쓸거
        if 'brand' in col:  # 브랜드는 없을 수도 있기때문
            err_col.insert(0, 'brand')
            err_values.insert(0, brand_code_list[0])

        # 이미 한 번 다 긁은 상품인지 확인*************************************************************
        try:
            # code 가 겹치면? : product 에 있고 그 product 의 all_fin 이 True 이고 color 에 이미 있는 url 일 경우
            if self.db.is_duplication('product', 'code', code) and self.db.get_data('product', 'all_fin', 'code', code) == 'True':
                if self.db.is_duplication('color', 'url', self.url):      # url 도 겹치면? -> 같은 상품이므로 종료
                    print(code, end=': ')
                    print('already crawled!!')
                    return True
                else:       # code 는 같은데 url 이 다르면? -> color 가 다른 경우라고밖에...
                    # color 처리해줘야함****************************************
                    color_col = ['product_code', 'url']
                    color_val = [code, self.url]
                    self.db.insert_sub_data('color', color_col, color_val)      # 일단 color table 에 저장하고
                    # 이미지파일도 저장 and 사이즈랑 태그는 필요없음
                    self.save_image(code, cate_name)
                    print(f'{code}: color add finished!!')
                    return False
            else:       # 겹치지 않는 경우 그냥 크롤링 해주면 된다.
                print(code, end=': ')
                print('괜찮아 아직 없어')
        except Exception as ex:
            print(code + '_duplication check fail')
            print(ex)
            err_content.append('dup_check_error')

        try:
            # 정보 가져오기
            for i in range(1, len(info_list)):
                left_text = info_list[i].p.text
                if '시즌' in left_text and '성별' in left_text:
                    col.append('season')
                    col.append('sex')
                    # season_sex
                    season_sex = info_list[i].p.next_sibling.next_sibling.text
                    season_sex_text = re.compile('[\\n\\t]').sub('', season_sex)
                    season_sex_text = re.compile('^\\s').sub('', season_sex_text)
                    season_sex_text = re.compile('/(?=.$)').sub('-', season_sex_text)
                    season_sex_list = re.split('-', season_sex_text)
                    for e in season_sex_list:
                        values.append(e)
                else:
                    left_text = re.compile('(시즌|성별|인기도|누적판매|좋아요|구매 후기)').search(left_text)
                    if left_text is not None:
                        col.append(change_eng[left_text.group()])
                        content = info_list[i].p.next_sibling.next_sibling.text
                        content = re.compile('[\\n\\t]').sub('', content)
                        values.append(content)
            # url
            col.append('url')  # url 은 따로 추가
            values.append(self.url)

            # Getting full_name
            full_name = self.html.find('span', {'class': 'product_title'}).span.text
            col.insert(2, 'full_name')
            values.insert(2, full_name)
            print('col', end=': ')
            print(col)
            print('values', end=': ')
            print(values)
        except Exception as ex:
            print(code + '_information fail')
            print(ex)
            err_content.append('get_information_error')

            # price
            price = self.get_price()

        # 카테고리 처리
        try:
            # Getting categories -> category table 에 저장
            category_mass = self.html.find('p', {'class': 'item_categories'})
            category_list = [s.text for s in category_mass.find_all('a')]
            category_list.pop()
            self.db.insert_category(category_list)
            # 기본 정보에 추가해줘
            cate_id = self.db.get_cate_id(category_list)
            col.insert(2, 'category')
            values.insert(2, cate_id)
            print(code + '_category success')
        except Exception as ex:
            print(code + '_category fail')
            print(ex)
            err_content.append('category_error')

        # product 기본정보 DB 에 저장하기
        try:
            self.db.insert_sub_data('product', col, values)
            print(code + '_information to db success!')
        except Exception as ex:
            print(code + '_information to db fail!')
            print(ex)
            err_content.append('save_information_error')

        # color table 에도 product 넣어야함!!!
        try:
            color_col = ['product_code', 'url']
            color_val = [code, self.url]
            self.db.insert_sub_data('color', color_col, color_val)
            print(code + '_information is saved to color table!')
        except Exception as ex:
            print(code + '_information is NOT!!!! saved to color table!')
            print(ex)
            err_content.append('information_to_color_table_error')

        # 태그들*/****************************************************************************
        tags = info_list[-1].p.text
        tags = re.compile('\\n').sub('', tags)
        tags = re.compile('^#').sub('', tags)
        tag_list = re.split('#', tags)
        try:  # 태그
            if len(tags) > 0:
                self.db.insert_list_data('tags', tag_list, code)  # fill tags, tags_mapping table
            elif len(tags) == 0:
                print('tag가 없습니다.')
            print(code + '_tags success!')
        except Exception as ex:
            print(code + '_tags fail!')
            print(ex)
            err_content.append('tag_error')

        # 이미지
        try:
            self.save_image(code, cate_name)
            print(code + '_image saved!!')
        except Exception as ex:
            print(code + '_image fail!!')
            print(ex)
            err_content.append('image_error')
        # 사이즈 정보
        try:
            self.get_size_info(code)
            print(code + '_size_info saved!!')
        except Exception as ex:     # AttributeError
            print(code + '_size_info fail!!')
            print(ex)
            err_content.append('size_error')

        # error 났을 경우 에러테이블 채워주기
        if len(err_content) > 0:
            err_values.insert(-2, str(err_content))
            self.db.insert_sub_data('err_product', err_col, err_values)

        # 상품이 모든 코드를 수행했다고 표시
        self.db.update_data('product', 'all_fin', 'True', 'code', code)
        return False

    def get_size_info(self, code):

        table = self.html.find('table', {'class': 'table_th_grey'})

        change_eng = {'총장': 'total_length', '어깨너비': 'shoulder', '가슴단면': 'chest', '소매길이': 'sleeve', '허리단면': 'waist',
                      '허벅지단면': 'thigh', '밑위': 'croth', '밑단단면': 'hem'}

        # column 만들기 (어깨너비, 가슴단면 등)
        col_group = table.thead.tr.children
        col_list = [re.compile('[\n\t]+').sub('', child.text) for child in col_group if
                    str(type(child)) != "<class 'bs4.element.NavigableString'>"]
        del col_list[0]
        col = [change_eng[kor] for kor in col_list]
        col_cnt = len(col)
        col.insert(0, 'product_code')
        col.insert(1, 'bulk')

        # 행에 있는 데이터 가져오기
        t_body = table.tbody.tr
        for i in range(4):  # 데이터가 있는 첫 행으로 이동
            t_body = t_body.next_sibling
        while t_body is not None:
            temp = [code]
            bulk = t_body.th.text
            temp.append(bulk)
            t_row = t_body.td
            for i in range(col_cnt):
                temp_element = t_row.text
                temp.append(temp_element)
                t_row = t_row.next_sibling.next_sibling
            self.db.insert_sub_data('size_info', col, temp)
            t_body = t_body.next_sibling.next_sibling
        return

    def save_image(self, code, cate_name):

        di = f'./image/{cate_name}/' + code
        # 이미지 저장할 폴더
        try:
            if not os.path.isdir(di):
                os.mkdir(di)
        except OSError:
            print('Failed to create directory!!!!')

        extension = 'jpg'       # 확장자
        filepath = di + '/'    # 파일 경로

        image_order = len(next(os.walk(di))[2]) + 1         # 몇번째 이미지인지(현재 파일 개수 + 1)
        image_mass = self.html.find('ul', {'class': 'product_thumb'}).li    # 이미지 정보 부분
        image_src = 'https:' + image_mass.img.get('src')                     # image url

        filename = str(image_order).zfill(2) + '.' + extension                       # file name
        if not os.path.exists(filepath + filename):
            urllib.request.urlretrieve(image_src, filepath + filename)
        else:
            print('This image file already exists!')

        img_pk = code + str(image_order).zfill(2)        # 이미지 구분하기 쉽게 유니크값 하나 만듦

        info = [img_pk, code, image_order, image_src, filepath, filename, extension]
        self.db.insert_full_data('img', info)
        self.db.insert_full_data('img_mapping', [code, img_pk])

        # 이미지가 하나 이상일 경우 계속 넣어주어야
        while image_order > 0:
            try:
                image_order = image_order + 1
                image_mass = image_mass.next_sibling.next_sibling
                image_src = 'http:' + image_mass.img.get('src')
                # 작은 이미지를 큰 이미지로 바꿈 (숫자만 60에서 500으로 바꾸면 됨)
                image_src = re.compile('60(?=\\.)').sub('500', image_src)

                filename = str(image_order).zfill(2) + '.' + extension
                urllib.request.urlretrieve(image_src, filepath + filename)

                img_pk = code + str(image_order).zfill(2)
                info = [img_pk, code, image_order, image_src, filepath, filename, extension]
                self.db.insert_full_data('img', info)
                self.db.insert_full_data('img_mapping', [code, img_pk])
            except AttributeError:
                image_order = 0
        return
