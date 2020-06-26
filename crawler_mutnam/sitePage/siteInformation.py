# <$$$> 데이터베이스에서 불러오게 바꾸자


class CateXpathInfo(object):
    def __init__(self, site_id):
        # xpath information 을 다 가져와서 넣는다.
        # 맨 아래 주석처리한 거에서 복사해서 쓴다. <$$$> 이희은 예시

        # 해당 사이트의 카테고리 depth
        self.n = 2
        # 사이트의 카테고리 xpath 정보 모음
        self.xpath_info = []
        cate1 = [1, '/html/body/div[1]/div/div[2]/div[3]/div/div[2]/ul[1]', '/li[3]', '/a', False, (3, 7)]
        cate2 = [1, '/html/body/div[1]/div/div[3]/div/div[1]/ul', '/li[1]', '/a', True, (1, 0)]
        # cate3 = [-1, '', '/ul/li[4]', '/a', False, (1, 0)]
        self.xpath_info.append(cate1)
        self.xpath_info.append(cate2)
        # self.xpath_info.append(cate3)

    # depth = n 인 category 의 xpath list 를 리턴한다
    def get_xpath_elements_cate_n(self, dep, cate_b):
        stat = self.get_static(cate_b, dep)
        dyn = self.xpath_info[dep - 1][2]
        suffix = self.xpath_info[dep - 1][3]

        xpath_elements = [stat, dyn, suffix]
        return xpath_elements

    # static 부분 구하기: 이전카테고리(cate_b) 와 뺄 구간의 수(stat_sub) 더할 부분(stat_add) 이용
    def get_static(self, cate_b, dep):
        stat_sub = self.xpath_info[dep - 1][0]
        stat_add = self.xpath_info[dep - 1][1]

        if stat_sub > 0:
            stat = stat_add
        elif stat_sub == 0:
            stat = cate_b + stat_add
        else:
            idx = -1
            for i in range(-stat_sub):
                while cate_b[idx] != '/':
                    idx = idx - 1
                idx = idx - 1
            stat = cate_b[:idx + 1] + stat_add
        return stat

    def get_need_click(self, dep):
        need_c = self.xpath_info[dep - 1][4]
        return need_c

    # 해당 뎁스의 xpath_list 중 실제로 사용할 범위를 구하는 과정
    def get_used_range(self, x_paths_of_dep, dep):
        # 미리 정해놓은 구간만 들어간다 ex: li[4] ~ li[9] 면 (4,9)
        range_str = int(self.xpath_info[dep - 1][5][0]) - 1  # li[4] xpath 에서 4번째이므로 cate_n[3]
        range_end = int(self.xpath_info[dep - 1][5][1])  # li[9] 는 cate[8]
        if range_end > 0:
            range_end = min([len(x_paths_of_dep), range_end])
        else:  # 0보다 작거나 같으면
            range_end = len(x_paths_of_dep) + range_end
        return range(range_str, range_end)


# <$$$> 클래스 이름 바꾸자
class ProductXpathInfo(object):
    def __init__(self, site_name):
        self.need_trans = False
        # 무신사
        if site_name == 'musinsa':
            product_stat = '//div[@class="list-box box"]/descendant::li[@class="li_box" and position()=1]/..'
            product_dyn = '/li[1]'
            product_suffix = '/div[@class="li_inner"]/div[1]/a'
            self.cir_elements = [product_stat, product_dyn, product_suffix]

            self.dic = {'총장': 'total_length', '어깨너비': 'shoulder', '가슴단면': 'chest', '소매길이': 'sleeve', '허리단면': 'waist',
                        '허벅지단면': 'thigh', '밑위': 'croth', '밑단단면': 'hem', '암홀': 'arm_hole'}
            self.t_head_xpath = '//table[@class="table_th_grey"]/thead'
            self.t_body_xpath = '//table[@class="table_th_grey"]/tbody'
            self.size_list = ('FREE', 'XXXS', 'XXS', 'XS', 'M', 'L', 'XL', 'XXL', 'XXXL')
        # 탑텐
        elif site_name == 'topten':
            self.t_head_xpath = '//*[@id="detail2"]/div[2]/table/thead'
            self.t_body_xpath = '//*[@id="detail2"]/div[2]/table/tbody'
            self.dic = {'사이즈': 'bulk', '어깨너비': 'shoulder', '가슴둘레': 'chest', '밑단둘레': 'hem', '소매길이': 'sleeve',
                        '총길이': 'total_length', '허리둘레': 'waist', '엉덩이둘레': 'hip', '앞밑위길이': 'croth', '허벅지둘레': 'thigh'}
            pass
        # 달트
        elif site_name == 'daltt':
            product_stat = '/html/body/div[3]/div[2]/div[4]/div[2]'
            product_dyn = '/div[1]'
            product_suffix = '/div[1]/a'
            self.cir_elements = [product_stat, product_dyn, product_suffix]
            self.t_head_xpath = '//div[@class="mSize"]/descendant::thead'
            self.t_body_xpath = '//div[@class="mSize"]/descendant::tbody'
            self.size_list = ('FREE', 'XXXS', 'XXS', 'XS', 'M', 'L', 'XL', 'XXL', 'XXXL')
            self.dic = {'사이즈': 'bulk', '어깨': 'shoulder', '가슴': 'chest', '소매': 'sleeve', '팔통': 'arm_width',
                        '암홀': 'arm_hole', '밑단': 'hem', '허리': 'waist', '엉덩이': 'hip', '허벅지': 'thigh',
                        '밑위': 'croth', '총길이': 'total_length'}
        # 유니클로
        elif site_name == 'uniqlo':
            product_stat = '//*[@id="content1"]'
            product_dyn = '/div[3]/div/ul/li[1]'
            product_suffix = '/div[1]/p/a'
            self.cir_elements = [product_stat, product_dyn, product_suffix]
            self.t_head_xpath = '//div[@class="size_table"]/table/thead'
            self.t_body_xpath = '//div[@class="size_table"]/table/tbody'
            self.need_trans = True
            self.size_list = ('FREE', 'XXXS', 'XXS', 'XS', 'M', 'L', 'XL', 'XXL', 'XXXL', '4XL')
            self.dic = {'전체길이A': 'total_length', '전체길이B': 'total_length', '어깨너비': 'shoulder', '가슴너비': 'chest',
                        '소매길이': 'sleeve', '밑단폭': 'hem', 'B:허리둘레 상품사이즈(단위:cm)': 'waist', '엉덩이둘레': 'hip',
                        '허벅지너비': 'thigh', '밑위길이': 'croth', '다리길이': 'leg_length', '전체길이': 'total_length',
                        'B:허리둘레상품사이즈(단위:cm)': 'waist', '허리둘레상품사이즈(단위:cm)': 'waist', '치마길이': 'total_length',
                        '전체길이A(어깨끈길이포함)': 'total_length', '전체길이(끈길이포함)': 'total_length'}

        # 이희은닷컴
        elif site_name == 'leehee':
            product_stat = '//ul[@class="prdList grid3"]'
            product_dyn = '/li[1]'
            product_suffix = '/div/a'
            self.cir_elements = [product_stat, product_dyn, product_suffix]
            self.t_body_xpath = '//*[@id="prdDetail"]/div[3]/div/center[3]/table/tbody'
            self.dic = {'사이즈': 'bulk', '어깨': 'shoulder', '가슴': 'chest', '소매': 'sleeve', '팔통': 'arm_width',
                        '암홀': 'arm_hole', '밑단': 'hem', '허리': 'waist', '엉덩이': 'hip', '허벅지': 'thigh',
                        '밑위': 'croth', '총길이': 'total_length', '총기장': 'total_length'}
            self.size_list = ('프리', 'free', 'XXXS', 'XXS', 'XS', 'M', 'L', 'XL', 'XXL', 'XXXL', '4XL')

        # 임블리
        elif site_name == 'imvely':
            product_stat = '//div[@class="xans-element- xans-product xans-product-normalpackage package_box "]/div/ul'
            product_dyn = '/li[1]'
            product_suffix = '/div/p[1]/a'
            self.cir_elements = [product_stat, product_dyn, product_suffix]
            self.t_head_xpath = '//div[@class="wrap_info size_info"]/descendant::thead'
            self.t_body_xpath = '//div[@class="wrap_info size_info"]/descendant::tbody'
            self.need_trans = True
            self.dic = {'어깨': 'shoulder', '가슴': 'chest', '허리': 'waist', '암홀': 'arm_width', '소매': 'sleeve',
                        '밑단': 'hem', '총길이': 'total_length', '힙': 'hip', '허벅지': 'thigh', '밑위': 'croth'}
        return


# class EtcInfo(object):
#     def __init__(self, site_id):
#         # 무신사
#         if site_id == 1:
#             self.next_page_xpath = '//*[@id="contentsItem_list"]/div[2]/div[5]/div/div/a[13]'
#         # 탑텐
#         elif site_id == 2:
#             self.next_page_xpath = '//*[@id="div_id_paging"]/ul/li[12]/a'
#         elif site_id == 65:
#             self.next_page_xpath = '//*[@id="-content"]/div[6]/ul/li[3]/a'
#         # 유니클로는 없는데...
#         elif site_id == 1:
#             self.next_page_xpath = ''
#         elif site_id == 99:
#             self.next_page_xpath = '/html/body/div[4]/div/div/div[6]/a[3]'
#         return


# <카테고리 xpath 설명>
# 1. 빼야할 구간(static): 양수면 전부 다 지운다, 0이면 이전 카테고리 전부를 물려받는다. -2 면 2개 구간을 뺀다.
# 2. 더해야할 부분(static): 뺀 부분에 추가해야 하는 것들
# 3. 변하는 부분(dyn): ex) /li[1]/li[2] 면 /li[1]/li[1] 부터 끝까지 돌아간다
# 4. 뒤에 고정적으로 붙는 부분
# 5. 이전카테고리 클릭여부
# 6. 가져올 구간: 완성된 xpath 들을 x[1] ~ x[10] 이라고 하자.
# 다 가져오고싶으면 (1,10) 혹은 (1,0). 뒤에거 하나 빼고싶으면 (1,-1). 3번째부터 6번째는 (3,6)

# <<무산사>>
# 무신사 카테고리 xpath
# cate1 = [1, '/html/body/div[7]/div[3]/div[1]/div[1]/nav', '/div[2]', '/div[1]/a', False, (2, 6)]
# cate2 = [-2, '/div[2]', '/ul[1]/li[1]', '/a', False, (1, 0)]

# <<탑텐>>
# 탑텐 카테고리 xpath
# cate1 = [0, '/html/body/header/div[4]/div/div[2]/nav/ul', '/li[4]', '/strong/a', False, (4, 6)]
# cate2 = [1, '/html/body/form/section/div/section[2]/aside/nav/ul', '/li[1]', '/a', True, (1, 4)]
# cate3 = [1, '/html/body/form/section/div/section[2]/aside/nav/ul', '/li[1]', '/a', True, (1, 0)]
# cate4 = [-2, '', '/li[1]', '/a', True, (1, 0)]

# next_page_xpath = '//*[@id="div_id_paging"]/ul/li[12]/a'

# 탑텐 product xpath
# product_stat = '/html/body/form/section/div/section[2]/div/div[1]/ul'
# product_dyn = '/li[1]'
# product_suffix = '/a'

# 탑텐 table xpath
# t_head_x = '//*[@id="detail2"]/div[2]/table/thead'
# t_body_x = '//*[@id="detail2"]/div[2]/table/tbody'

# 탑텐 column dictionary
# dic = {'사이즈': 'bulk', '어깨너비': 'shoulder', '가슴둘레': 'chest', '밑단둘레': 'hem', '소매길이': 'sleeve',
#        '총길이': 'total_length', '허리둘레': 'waist', '엉덩이둘레': 'hip', '앞밑위길이': 'croth', '허벅지둘레': 'thigh'}

# <<유니클로>>
# 유니클로 카테고리 xpath
# cate1 = [1, '/html/body/div[2]/div[1]/div[1]/div[1]/ul', '/li[1]', '', False, (1,0)]
# cate2 = [0, '', '/div/div[3]/div[1]', '/h5', True, (2,0)]
# cate3 = [-1, '', '/ul/li[4]', '/a', False, (1,0)]

# t_head_x ='/html/body/section/div/section/div[5]/div[2]/table/thead'
# t_body_x = '/html/body/section/div/section/div[5]/div[2]/table/tbody'


# <<달트>>
# 달트 카테고리 xpath
# cate1 = [1, '/html/body/div[3]/div[1]/div[3]/ul/ul', '/li[2]', '/a', False, (6, 10)]
# cate2 = [-6, '/div[2]/div[1]/div[3]/ul', '/li[2]', '/a', True, (2, 0)]

# dic = {'사이즈': 'bulk', '어깨': 'shoulder', '가슴': 'chest', '소매': 'sleeve', '팔통': 'arm', '암홀': 'arm_hole',
# '밑단': 'hem', '허리': 'waist', '엉덩이': 'hip', '허벅지': 'thigh', '밑위': 'croth', '총길이': 'total_length'}

# 달트 product xpath

# <<이희은>>
# cate1 = [1, '//*[@id="category-lnb"]/div/ul', '/li[4]', '/a', False, (4, 8)]
# cate2 = [1, '//*[@id="contents"]/div[1]/ul', '/li[1]', '/a', True, (1, 0)]

# <<임블리 카테고리 xpath>>
# self.n = 2
# cate1 = [1, '//*[@id="nav"]/div/div[2]/dl[2]', '/dd[2]', '/a', False, (2, 7)]
# cate2 = [1, '//*[@id="smartskinListSubcate"]', '/li[1]', '/a', True, (2, 0)]

# cate1 = [1, '/html/body/div[1]/div/div[2]/div[3]/div/div[2]/ul[1]', '/li[3]', '/a', False, (3, 7)]
# cate2 = [1, '/html/body/div[1]/div/div[3]/div/div[1]/ul', '/li[1]', '/a', True, (1, 0)]
