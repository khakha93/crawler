import pymysql
import shutil
import os


# table_list = ['img_mapping', 'img', 'tags_mapping', 'tags', 'size_info', 'product', 'history', 'category', 'site',
# 'check_t']

# db 비우기
def clear_db():
    table_list = ['img_mapping', 'img', 'tags_mapping', 'tags', 'size_info', 'product', 'err_product', 'history', 'category', 'site',
                  'check_t']
    db = pymysql.connect(host='localhost', port=3306, user='kha', passwd='1234', db='crawling_musinsa', charset='utf8')
    try:
        del_sql = 'DELETE FROM {};'
        ar_sql1 = 'ALTER table {} AUTO_INCREMENT = 1;'
        ar_sql2 = 'SET @cnt = 0;'
        ar_sql3 = 'UPDATE {} SET id = @cnt:= @cnt+1;'

        with db.cursor() as cursor:
            for t in table_list:
                # delete all data in each table
                cursor.execute(del_sql.format(t))
            for t in table_list:
                # arrange index of id
                cursor.execute(ar_sql1.format(t))
                cursor.execute(ar_sql2)
                cursor.execute(ar_sql3.format(t))
        db.commit()
    finally:
        db.close()
    return


def remove_img():
    # 이미지 폴더 및 파일 제거
    path = 'image'
    if os.path.isdir(path):
        shutil.rmtree(path)
    return


clear_db()
remove_img()
