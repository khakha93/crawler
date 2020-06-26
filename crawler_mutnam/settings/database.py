import pymysql
from pymysql import IntegrityError
import re


class DataBase(object):
    def __init__(self, db_name):
        self.db_name = db_name
        return

    def connect_db(self):
        db = pymysql.connect(host='localhost', port=3306, user='crawler', passwd='ironman3419', db=self.db_name, charset='utf8')
        return db

    def etc_command(self, sql):
        db = self.connect_db()
        print(sql)
        try:
            with db.cursor() as cursor:
                cursor.execute(sql)
                f = cursor.fetchall()
            db.commit()
        finally:
            db.close()
        return f

    # 중복된 데이터의 개수를 리턴
    def is_duplication(self, table_name, col, val):
        sql = f'SELECT * FROM {self.db_name}.{table_name} where {col} = {repr(val)};'
        f = self.etc_command(sql)
        return len(f)

    def get_data(self, table_name, need_col, col, val):
        sql = f'SELECT {need_col} FROM {table_name} WHERE {col} = {repr(val)};'
        f = self.etc_command(sql)
        if len(f) == 0:
            return None
        return f[0][0]

    def update_data(self, table_name, m_col, m_val, wh_col, wh_val):
        if m_val is None:
            m_val = 'null'
        else:
            m_val = repr(m_val)
        # category 가 cate_name 인 것의 col 을 val 로 바꾼다
        sql = f'UPDATE {table_name} SET {m_col} = {m_val} WHERE {wh_col} = {repr(wh_val)};'
        self.etc_command(sql)
        return

    def insert_sub_data(self, table_name, columns, values):
        db = self.connect_db()

        # col, val 을 sql문에 넣기위해 스트링으로 만들어준다
        col_str = re.compile('\'').sub('', repr(tuple(columns)))
        val_str = re.compile("'NULL'").sub("NULL", repr(tuple(values)))
        if len(columns) == 1:
            col_str = re.compile(',(?=\\))').sub('', col_str)
            val_str = re.compile(',(?=\\))').sub('', val_str)

        sql = f'INSERT INTO {table_name} {col_str} VALUES {val_str};'
        sql2 = 'SELECT LAST_INSERT_ID();'
        print(sql)

        try:
            with db.cursor() as cursor:
                cursor.execute(sql)
                cursor.execute(sql2)
                f = cursor.fetchone()
            db.commit()
        except IntegrityError:  # code 가 같은 경우 : 코드를 유니크키 설정해놓으면 이런 에러가 난다
            print(f'{table_name}으로 insert: 유니크키 중복 or 외래키 검사 실패')
            return -1
        finally:
            db.close()
        return f[0]