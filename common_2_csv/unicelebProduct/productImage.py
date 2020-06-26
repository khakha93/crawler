from product.productImage import ProductImage as Pi
from settings import fileNDirectory
import re


def save_2_file(di, img_src, img_type):
    print(f'image({img_src}) save to file and DB')

    # <$$$> jpg - png 자주 바꿈
    extension = 'jpg'

    file_path = di + '/'
    file_name = f'{img_type}.{extension}'
    abs_path = file_path + file_name

    # 이미지 파일도 저장
    fileNDirectory.img_url_2_file(img_src, abs_path)
    return img_type


class ProductImage(Pi):
    def get_img_src(self):
        # key image src
        src = self.html.find('div', {'class': 'thumbnail'}).div.img['src']
        self.img_src_s.append('https:' + src)
        return

    def save_image(self, product_id):
        print('Save images')

        # 폴더 만들기 <$$$> 이 부분 조작하면 된다
        di = f'./image/{self.site_id}/{product_id}'
        fileNDirectory.make_directory(di)

        self.get_img_src()

        img_types = []
        # 이미지 파일 저장 & csv 파일로 이동
        for src in self.img_src_s:
            img_type = re.compile('(big)|(medium)|(small)|(tiny)').search(src).group()
            img_types.append(img_type)
            save_2_file(di, src, img_type)
        return img_types


