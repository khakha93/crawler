from page import CategoryPage as OriginalCp
import re


class CategoryPage(OriginalCp):

    def move_n_th_page(self, n):
        print(f'\nMove to next page! (from: {self.url})')
        search_syn = re.compile('&page=\\d+')
        if search_syn.search(self.url) is None:
            new_url = self.url + f'&page={n}'
        else:
            new_url = search_syn.sub(f'&page={n}', self.url)
        self.ch.move(new_url)
        return

    def move_next_page(self, now_page):
        self.ch.click_by_xpath('/html/body/div[4]/div/div/div[6]/a[3]')
        return
    pass

