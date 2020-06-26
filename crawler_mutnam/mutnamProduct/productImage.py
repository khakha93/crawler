from product.productImage import ProductImage as Pi


class ProductImage(Pi):
    def get_img_src(self):
        # key image src
        src = self.html.find('div', {'class': 'keyImg'}).div.img['src']
        self.img_src_s.append('https:' + src)

        # extra image src
        try:
            extra_imgs = self.html.find('div', {'class': 'detail_info_area'}).center.find_all('img')
        except AttributeError:
            extra_imgs = self.html.find('div', {'class': 'detail_info_area'}).div.find_all('img')
        for ei in extra_imgs:
            self.img_src_s.append('https:' + '//mutnam.com' + ei['src'])

        return



