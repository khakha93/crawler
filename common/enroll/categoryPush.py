from enroll.categoryInformation import CategoryInformation
import pandas as pd
import os


# CategoryInformation을 상속받아서, 카테고리 정보를 csv 파일이나 데이터베이스로 저장하는 메소드를 가진 클래스
class CategoryPush(CategoryInformation):

    # 위에서 언급한 두 과정 중 전자에 해당
    def push_2_csv(self):

        self.ch.driver.maximize_window()  # 창 크기 최대화
        self.ch.move(self.url)  # 페이지로 이동
        # depth 1 부터 최종 뎁스까지 xpath 들을 만들고 url 과 텍스트를 가져와서 저장한다.
        # parameter: category_text, before_category_xpath, category_depth
        self.drive_next_cate('', '', 1)

        # 카테고리 url, text 를 가져와서 엑셀에 저장. 아래 과정이 이해가 안 간다면, pandas의 Dataframe에 대해서 검색해볼것.
        # text 와 url 캄럼을 가진 Dataframe을 생성
        data = pd.DataFrame(data=[], columns=['text', 'url'])
        # 모든 카테고리의 이름, url 을 각각 text, url 로 가지는 Dataframe 을 생성한 후 위에서 생성한 Dataframe 에 붙이는 과정을 반복한다.
        for i in range(len(self.cate_names)):
            row = pd.DataFrame(data=[[self.cate_names[i], self.urls[i]]], columns=['text', 'url'])
            data = data.append(row, ignore_index=True)

        data.to_csv(f'./categoryCSV/{self.site_name}_category.csv')
        return

    # 맨 위에서 언급한 두 과정 중 후자에 해당
    def push_2_db(self):
        # csv파일을 읽는다
        data = pd.read_csv(f'./categoryCSV/{self.site_name}_category.csv')
        # 읽어들인 정보를 category table 에 넣고 그 id 값을 가져온다. 그 값을 이용해 history table을 채운다.
        for i in range(len(data)):
            cate_id = self.db.insert_sub_data('category', ['name', 'site', 'cate_url'],
                                              [data.text[i], self.site_id, data.url[i]])
            if cate_id == -1:       # 이미 있는 데이터(중복된 데이터일 경우 id 대신 -1을 리턴하므로, 다시 id를 찾아서 대입해줘야한다.
                cate_id = self.db.get_data('category', 'id', 'cate_url', data.url[i])
            self.db.insert_sub_data('history', ['category', 'cr_type'], [cate_id, 1])
        self.db.update_data('site', 'settings', 'True', 'id', self.site_id)
        return

