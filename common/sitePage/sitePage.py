from page import Page
from browser import chrome
from settings.myError import NotPreparedError
from settings.fileNDirectory import make_directory
# from category.cateInitPage import CateInitPage
from musinsaProduct.cateInitPage import CateInitPage as MuCate
from uniqloProduct.cateInitPage import CateInitPage as UniCate
from dalttProduct.cateInitPage import CateInitPage as DalCate
from toptenProduct.cateInitPage import CateInitPage as TopCate
from leeheeProduct.cateInitPage import CateInitPage as LeeCate


class SitePage(Page):
    # 생성자: 사이트 url, name 을 입력받아서 category,
    def __init__(self, url, ch: chrome.Chrome):
        super().__init__(url, ch)

        if self.db.get_data('site', 'settings', 'url', self.url) == 'True':
            Page.site_id = self.db.get_data('site', 'id', 'url', self.url)
            Page.site_name = self.db.get_data('site', 'name', 'url', self.url)
        else:
            raise NotPreparedError

        # 이미지 폴더 생성
        di = f'./image/{self.site_id}'
        make_directory(di)
        return

    def crawling_by_site(self, cr):
        if cr == 1:
            # 사이트가 자기이면서 cr_type 이 3인 것을 찾으면 되잖아
            sql = f'SELECT id, cate_url from category where id in (select category FROM history WHERE cr_type = 3) ' \
              f'and site = {self.site_id};'
        else:
            sql = f'select id, cate_url from category where site = {self.site_id}'

        cate_info = list(zip(*self.db.etc_command(sql)))
        try:
            cate_id_list = cate_info[0]
            cate_urls = cate_info[1]
            num = len(cate_id_list)
        except IndexError:
            return

        for idx_c in range(num):
            cate_id = cate_id_list[idx_c]
            cate_url = cate_urls[idx_c]
            self.cate_crawling(cate_id, cate_url)
        return

    def cate_crawling(self, cate_id, cate_url):
        # Category page 객체 생성
        if self.site_name == 'musinsa':
            cate_init_page = MuCate(cate_url, self.ch, cate_id)
        elif self.site_name == 'uniqlo':
            cate_init_page = UniCate(cate_url, self.ch, cate_id)
        elif self.site_name == 'daltt':
            cate_init_page = DalCate(cate_url, self.ch, cate_id)
        elif self.site_name == 'topten':
            cate_init_page = TopCate(cate_url, self.ch, cate_id)
        elif self.site_name == 'leehee':
            cate_init_page = LeeCate(cate_url, self.ch, cate_id)
        else:
            print(f'{self.site_name}: 준비가 안 되어있음')
            return

        cate_init_page.sort_by_new()
        # Category page 크롤링
        cate_init_page.crawling_by_category()
        return


