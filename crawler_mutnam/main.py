from sitePage.sitePage import SitePage
from settings.myError import NotPreparedError
from settings.database import DataBase


# site table에 있는 모든 사이트들을 차례로 크롤링
def crawling_all_site():
    # DB 에서 사이트의 id, url 를 전부 가져옴
    d = DataBase('test_db')
    sql = 'select id, url from site'
    site_info = list(zip(*d.etc_command(sql)))[1]

    for u in site_info:
        site_crawling(u)
    return


# 입력한 url을 가진 사이트를 찾아서 그 사이트만 크롤링
def site_crawling(site_url):

    try:
        # 사이트메이지 객체 생성
        s = SitePage(site_url)
    except NotPreparedError:
        # enroll_site(site_url, ch, site_name)
        print('Need enroll this site!')
        pass
    else:
        s.crawling_by_site(1)       # 비정상종료 카테고리만 찾아서 크롤링
        s.crawling_by_site(2)       # 모든 카테고리 크롤링
    finally:
        pass


# 전체 이미지 폴더 생성
# settings.make_directory('./image')

# crawling_all_site()
url = 'https://mutnam.com/'
site_crawling(url)

# <$$$> productUrls 랑 이미지 부분 다시 바꿔야함

# url = 'https://topten.topten10mall.com/'
# url = 'https://store-kr.uniqlo.com/'
# url = 'https://store.musinsa.com/app/'
# url = 'https://daltt.co.kr/'
# url = 'http://leehee.co.kr/'
# url = 'http://imvely.com/'


