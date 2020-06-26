import pymysql
import re


class Database(object):
    def __init__(self, db_name):
        self.db_name = db_name
        return

    def make_tables(self):      # db 만들기 귀찮으니깐 아예 이걸로 만들면 더 편할 듯
        return

    def is_duplication(self, table_name, col, val):
        db = pymysql.connect(host='localhost', port=3306, user='kha', passwd='1234', db=self.db_name, charset='utf8')
        sql = f'SELECT * FROM {self.db_name}.{table_name} where {col} = {repr(val)};'
        try:
            with db.cursor() as cursor:
                cursor.execute(sql)
                f = cursor.fetchone()
                if f is not None:
                    return True
        except Exception as ex:
            print(val + ': is_duplication 검사 도중')
            print(ex)
        finally:
            db.close()
        return False

    def get_data(self, table_name, need_col, col, val):
        db = pymysql.connect(host='localhost', port=3306, user='kha', passwd='1234', db=self.db_name, charset='utf8')
        sql = f'SELECT {need_col} FROM {table_name} WHERE {col} = {repr(val)}'
        # print(sql)
        try:
            with db.cursor() as cursor:
                cursor.execute(sql)
                f = cursor.fetchone()
                if f is None:
                    print('해당 data가 없음')
                    return f
                else:
                    print(table_name + '에서 getting data..')
        except Exception as ex:
            print(table_name + '에서 get data 도중', end='...')
            print(ex)
        finally:
            db.close()
        return f[0]

    # 데이터 삽입
    def insert_full_data(self, table_name, data_list, dup_check=False):
        # 데이터 테이블의 column 모음
        dic = {}
        # product_col = '(code, brand, full_name, season, sex, popular, sales, likes, review, url)'
        img_col = '(img_pk, product_code, product_order, img_src, filepath, filename, extension)'
        # size_col = '(product_code, bulk, total_length, shoulder, chest, sleeve, waist, thigh, croth, hem)'
        # dic['product'] = product_col
        # dic['size_info'] = size_col
        dic['img'] = img_col
        # dic['category_mapping'] = '(product, category)'
        # dic['category'] = '(word)'
        dic['tags'] = '(word)'
        dic['tags_mapping'] = '(product, tag)'
        dic['img_mapping'] = '(product_code, image)'

        # 디비 접속
        db = pymysql.connect(host='localhost', port=3306, user='kha', passwd='1234', db=self.db_name, charset='utf8')

        # SQL문 실행(insert ignore 으로 했는데 필요하면 나중에 다른걸로 바꾸지 뭐)
        tup = re.compile('\\[').sub('(', repr(data_list))
        tup = re.compile('\\]').sub(')', tup)
        insert_sql = '''INSERT {} INTO {}.{}
        {}
        VALUES {};'''
        # 중복체크 할 것인지 무시할 것인지
        if dup_check is True:
            text = ''
        else:
            text = 'IGNORE'

        # sql문 실행
        try:
            with db.cursor() as cursor:
                cursor.execute(insert_sql.format(text, self.db_name, table_name, dic[table_name], tup))
            db.commit()
        except Exception as ex:
            print(table_name + '으로 insert full data 도중', end='...')
            print(ex)
        finally:
            db.close()

        return

    def insert_sub_data(self, table_name, columns, data_list):
        # 디비 접속
        db = pymysql.connect(host='localhost', port=3306, user='kha', passwd='1234', db=self.db_name, charset='utf8')

        tup = re.compile('^\\[').sub('(', repr(data_list))
        tup = re.compile('\\]$').sub(')', tup)

        # col 을 sql문에 넣기위해 스트링으로 만들어준다
        col_str = re.compile('\\[').sub('(', repr(columns))
        col_str = re.compile('\\]').sub(')', col_str)
        col_str = re.compile('\'').sub('', col_str)

        sql = f'INSERT INTO {table_name} {col_str} VALUES {tup}'

        # sql문 실행
        try:
            with db.cursor() as cursor:
                cursor.execute(sql)
            db.commit()
            print(table_name + '으로 data inserting 완료')
        except Exception as ex:
            print(table_name + '으로 insert data 도중', end='...')
            print(ex)
        finally:
            db.close()

        return

    # 매핑데이터를 보유한 데이터의 삽입 ( tags )
    def insert_list_data(self, table_name, data_list, code):
        mapping_table = table_name + '_mapping'
        for element in data_list:
            data = [element]
            self.insert_full_data(table_name, data, False)
            data = [code, element]
            self.insert_full_data(mapping_table, data, False)
        return

    def insert_category(self, category):
        db = pymysql.connect(host='localhost', port=3306, user='kha', passwd='1234', db=self.db_name, charset='utf8')
        dep = len(category)-1

        try:
            with db.cursor() as cursor:
                sql1 = f'SELECT * FROM category WHERE g_name={repr(category[0])};'
                cursor.execute(sql1)
                g_ord = len(cursor.fetchall())
                sql2 = f'INSERT IGNORE INTO category (g_name, name, g_ord, g_layer) VALUES ({repr(category[0])}, {repr(category[dep])}, {g_ord}, {dep});'
                cursor.execute(sql2)
            db.commit()
        finally:
            db.close()
        return

    def get_cate_id(self, category):
        db = pymysql.connect(host='localhost', port=3306, user='kha', passwd='1234', db=self.db_name, charset='utf8')
        dep = len(category)-1
        sql = f'SELECT id FROM category WHERE g_name = {repr(category[0])} and name = {repr(category[dep])} and ' \
              f'g_layer = {dep} '
        try:
            with db.cursor() as cursor:
                cursor.execute(sql)
                f = cursor.fetchone()
                if f is None:
                    print('해당 카테고리가 없습니다.')
                    return f
        except Exception as ex:
            print('category id 를 찾는 중에')
            print(ex)
        finally:
            db.close()
        return f[0]

    def update_data(self, table_name, m_col, m_val, wh_col, wh_val):
        db = pymysql.connect(host='localhost', port=3306, user='kha', passwd='1234', db=self.db_name, charset='utf8')

        # category 가 cate_name 인 것의 col 을 val 로 바꾼다
        sql = f'UPDATE {table_name} SET {m_col} = {repr(m_val)} WHERE {wh_col} = {repr(wh_val)};'
        # print(sql)

        try:
            with db.cursor() as cursor:
                cursor.execute(sql)
            db.commit()
            print(table_name + '에서 update data 완료')
        except Exception as ex:
            print(table_name + '을 update 하는 도중', end='...')
            print(ex)
        finally:
            db.close()
        return

    # index 최신화 (필요 없음)
    def reindex(self, table_name):
        db = pymysql.connect(host='localhost', port=3306, user='kha', passwd='1234', db=self.db_name, charset='utf8')

        sql = f'alter table {table_name} auto_increment = 1; set @cnt = 0; update product set id = ' \
              f'@cnt:= @cnt+1; '
        # print(sql)
        return
