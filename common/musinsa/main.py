import page
import browser
import os
import pandas
import database
import re

'''
<<할 일>>
뒤로 밀리는거 처리하기
z
'''


def crawling_by_category2(cate_name, is_first, was_success):
    print('\n' + cate_name + ' category crawling~~')
    list_page = page.ListPage(ch.driver.current_url)  # 상품들이 나열된 페이지
    max_page = list_page.total_page  # total page 수
    num_total_product = list_page.get_total_product()

    return


def crawling_by_category(cate_name, is_first, was_success):
    print('\n' + cate_name + ' category crawling~~')
    list_page = page.ListPage(ch.driver.current_url)  # 상품들이 나열된 페이지
    max_page = list_page.total_page  # total page 수

    # 에러포인트 가져오기
    err_point = None
    if not (is_first or was_success):       # case 3 : 이전에 비정상 종료
        err_point = list_page.db.get_data('history', 'err_point', 'category', cate_name)

    # 각 페이지에서 수행
    hand_cond = True    # 비정상종료, 처음이 아님을 표시할 때 사용할거
    for idx_page in range(1, max_page+1):  # 임시조작*************************************** max_page+1
        print(f'\n{idx_page} page crawling...')
        max_pro = list_page.amount_product  # page에 있는 상품의 개수
        str_pro = 0

        # 임시조작*************************************************************************************
        if cate_name == 'Top':
            return

        # 선 조건 검사: error_point 로 이동하기
        if not (is_first or was_success):  # 비정상종료였을 경우
            try:
                error_idx = list_page.product_list.index(err_point)     # error가 난 url의 index
                print('\n' + str(error_idx) + '번째 상품으로 이동..(이전 비정상 종료)')
                # error 부터 크롤링하도록 start point 설정
                str_pro = error_idx
                # 이후 for 문은 정상수행
                was_success = True
            except ValueError:  # 이 페이지에 error point 가 없을 경우
                # 다음 페이지로 이동
                print('\n다음 페이지로 이동(error 지점 찾는 중)..')
                ch.next_list(idx_page + 1)
                list_page = page.ListPage(ch.driver.current_url)
                continue

        # 상품별로 for 문
        for idx_pro in range(str_pro, max_pro):     # 임시조작**************************** max_pro
            print(f'\n{idx_pro}번째 product crawling...')
            # err_point : url ( 비정상 종료 대비)
            err_point = list_page.product_list[idx_pro]
            # err_point 백업
            list_page.db.update_data('history', 'err_point', err_point, 'category', cate_name)
            print('error point 백업 완료')

            if hand_cond:   # 조건들 처리---------------------------------------------------------------
                # 비정상 종료 표시 (한번만 하면 됨)
                list_page.db.update_data('history', 'was_success', 'False', 'category', cate_name)
                # 처음이 아니라고 표시 (한번만 하면 됨)
                list_page.db.update_data('history', 'is_first', 'False', 'category', cate_name)
                hand_cond = False
            print('조건 확인 완료')

            # 상품 페이지로 이동 후 정보 긁어오기 *******************************************************
            product_url = list_page.product_list[idx_pro]
            print(f'product url : {product_url}')
            product_page = page.ProductPage(product_url)
            print('상품페이지 객체 생성 완료')
            try:
                exist = product_page.get_product_info2(cate_name)  # 진짜 실제 리얼 크롤링 구간 &!@*%$^&!@*%$^
                if exist:
                    print('여기서부터는 이미 한거라 전부 패스합니다.')
                    # 정상 종료 표시 후 종료
                    list_page.db.update_data('history', 'was_success', 'True', 'category', cate_name)
                    return
            except Exception as ex:     # 중복체크하는 중에 오류가 난 경우
                print(err_point, end='에서 ')
                print(ex)
                err_col = ['cate_name', 'error_code', 'status', 'url']
                err_values = [cate_name, 'etc_error', 'not_solved', product_page.url]
                product_page.db.insert_sub_data('err_product', err_col, err_values)
        # 다음 페이지로 이동************************************************
        if idx_page == max_page:
            print('마지막 페이지까지 끝남~')
            break
        # 여기서 자꾸 에러가 나는데..... *************************************
        ch.next_list(idx_page + 1)
        print('move to next page~')
        try:
            list_page = page.ListPage(ch.driver.current_url)
        except AttributeError:
            # print(f'{ch.driver.current_url} 에서 AttributeError')
            print(f'page 전체 에러(AttributeError): {ch.driver.current_url}')
            continue
        except Exception as ex:
            # print(f'{type(ex)}: {ex}, {ch.driver.current_url}')
            print(f'page 전체 에러({type(ex)}): {ch.driver.current_url}')
            continue
        # print(ch.driver.current_url)
    # 정상 종료 표시
    list_page.db.update_data('history', 'was_success', 'True', 'category', cate_name)
    return


url = 'https://store.musinsa.com/app/'

# 무신사 메인 페이지
ch = browser.Chrome(url)
mu = page.InitPage(url)


# # TEMP (블랙프라이데이 임시)
# ch.driver.find_element_by_xpath('/html/body/section/div[3]/a[2]').click()
# ch.driver.implicitly_wait(3)
# mu = page.InitPage(url, ch.driver.page_source)

# 이미지 폴더 생성
mu.make_cate_img_folder()  # 각 카테고리별 폴더 다시 생성

# 쌩처름인지 확인
if mu.db.get_data('check_t', 'id', 'is_first', 'True') is None:
    mu.enroll_site('musinsa')
    mu.fill_history()
    mu.db.insert_sub_data('check_t', ['is_first'], ['True'])

# 카테고리별로 for 문 돌린다.
for idx_cate in range(mu.p_cate_num):  # mu.p_cate_num : 부모카테고리의 개수
    # 일단 카테고리 선택
    ch.move(mu.cate_urls[idx_cate])  # category url 로 이동
    print(f'\nmove to {idx_cate} category page!!')
    # 그 다음에 신상품순으로 정렬
    sc = 'getGoodsList(document.f1, document.f1.sort, \'new\', \'N\')'
    ch.driver.execute_script(sc)
    # print(f'move to {ch.driver.current_url}!!!')

    # is_first 가져오기
    f = mu.db.get_data('history', 'is_first', 'category', mu.cate_names[idx_cate])
    if f == 'True':
        print('\nFirst crawling start!!!s')
        crawling_by_category(mu.cate_names[idx_cate], True, True)
    elif f == 'False':
        for i in range(2):  # 비정상종료일 경우 2번 돌려야함
            # was_success 가져오기
            s = mu.db.get_data('history', 'was_success', 'category', mu.cate_names[idx_cate])
            if s == 'True':
                print('\n이전에 정상 종료했음')
                crawling_by_category(mu.cate_names[idx_cate], False, True)
                break
            elif i == 0:
                print('\n이전에 비정상 종료했음')
                crawling_by_category(mu.cate_names[idx_cate], False, False)
            else:
                break
    else:
        print('history 에서 is_first 가져올 때 error')

ch.driver.close()
