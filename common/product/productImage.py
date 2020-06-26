from browser import chrome
from page import ExtendedPage
from settings import fileNDirectory


class ProductImage(ExtendedPage):

    def __init__(self, url, ch: chrome.Chrome, category):
        super().__init__(url, ch, category)
        self.img_src_s = []
        return

    def save_n_2_db(self, di, img_src, product_id):
        print(f'image({img_src}) save to file and DB')

        # image table 과 image_mapping table 에 넣을 column 들
        img_col = ['product_id', 'img_src', 'file_path', 'file_name', 'extension']
        # <$$$> jpg - png 자주 바꿈
        extension = 'jpg'

        file_path = di + '/'
        img_order = self.db.is_duplication('image', 'product_id', product_id)+1
        file_name = f'{str(img_order).zfill(3)}.{extension}'
        abs_path = file_path + file_name
        img_val = [product_id, img_src, file_path, file_name, extension]

        # DB 에 집어 넣어. 유니크키 중복나면 알아서 안 들어가니깐
        self.db.insert_sub_data('image', img_col, img_val)
        # 이미지 파일도 저장
        if fileNDirectory.img_url_2_file(img_src, abs_path) == -1:
            # http 에러가 난 경우 -> 에러테이블에 표시
            self.fill_err_product('image_error', self.url, product_id=product_id, etc=f'src: {img_src}')
        return 0

    # 상품페이지의 상품 이미지들을 파일로 저장하고 DB에 기록하는 전체 과정
    def save_image(self, product_id):
        print('Save images')
        ret = 0
        # 폴더 만들기
        di = f'./image/{self.site_id}/{product_id}'
        fileNDirectory.make_directory(di)

        self.get_img_src()

        # 이미지 파일 저장
        for src in self.img_src_s:
            if self.save_n_2_db(di, src, product_id) == -1:
                ret = -1
        return ret

    # 상품페이지 내에 있는, 상품 이미지들의 src를 모은다.
    def get_img_src(self):
        raise NotImplementedError

