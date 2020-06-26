from enroll.categoryPush import CategoryPush
from browser.chrome import Chrome


# 역시 이름이 맘에 안 들지만,
# is_p 가 True 면 사이트에서 얻은 카테고리 정보를 csv파일로 저장하는 메소드(push_2_csv())를 호출하고,
# False면 csv파일을 읽어 category, history table 을 채우는 메소드 호출한다.
def do_using_csv(is_p):
    c = CategoryPush(url, ch, name)
    if is_p:
        c.push_2_csv()
    else:
        c.push_2_db()
    return


# 위의 push_2_csv()메소드를 수행하기 전에, 콘솔 창으로 확인하는 메소드. 카테고리 정보를 csv로 저장하냐, 콘솔창을 확인하냐의 차이만 있다.
def test_in_console():
    # 크롬 창을 최대화
    ch.driver.maximize_window()
    try:
        c = CategoryPush(url, ch, name)
        print(c.site_id)

        # 이 패키지 전체에서 핵심이 되는 메소드. 자세한 설명은 categoryPush.py 에서
        c.drive_next_cate('', '', 1)

        # 콘솔창으로 결과를 출력
        print('-'*50)
        # 카테고리의 이름들. ex) outer>jumper, women>top>반팔 등
        for n in c.cate_names:
            print(n)
        print('-'*50)
        # 카테고리의 url 출력
        for u in c.urls:
            print(u)
    finally:
        ch.driver.close()
    return


# [전체과정]
# 크롬 브라우저를 실행
ch = Chrome()

# 원하는 사이트의 url과 이름을 입력
url = 'https://mutnam.com/'
name = 'mutnam'

# 해당 사이트로 브라우저 이동
ch.move(url)

# 콜솔창으로 보면서 테스트하기
# try:
#     test_in_console()
# finally:
#     pass

# push 하기
try:
    is_2_csv = False
    # do_using_csv 에 관한 설명은 위에서 했으니 생략
    do_using_csv(is_2_csv)
finally:
    ch.driver.close()
    pass


# url = 'https://daltt.co.kr/'
# name = 'daltt'
# url = 'https://store-kr.uniqlo.com/'
# name = 'uniqlo'
# url = 'http://leehee.co.kr/'
# name = 'leehee'
# url = 'https://store.musinsa.com/app/'
# name = 'musinsa'
# url = 'https://topten.topten10mall.com/'
# name = 'topten'
# url = 'http://imvely.com/'
# name = 'imvely'




