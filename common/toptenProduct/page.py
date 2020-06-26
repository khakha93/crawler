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
        xpath = '//*[@id="div_id_paging"]/ul/li[12]/a'
        self.ch.click_by_xpath(xpath)
        return
    pass

