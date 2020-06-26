from page import CategoryPage as OriginalCp
import re
# from settings.myError import NoFunctionError


class CategoryPage(OriginalCp):

    def move_n_th_page(self, n):
        print(f'\nMove to next page! (from: {self.url})')
        search_syn = re.compile('&page=\\d+')
        if search_syn.search(self.url) is None:
            new_url = self.url + f'&page={n}'
        else:
            new_url = search_syn.sub(f'&page={n}', self.url)
        self.move(new_url)
        return

    def move_next_page(self, now_page):
        self.move_n_th_page(now_page+1)
    pass

