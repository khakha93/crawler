from browser.chrome import Chrome
import re


class CircleXpath(object):

    def __init__(self, ch: Chrome, elements):
        self.ch = ch
        self.static = elements[0]
        self.dynamic = elements[1]
        self.suffix = elements[2]

        self.completed_xpath_s = []

        # index 부분을 없앤다 (processed_dynamic)
        processed_dynamic = re.compile('\\[\\d+\\]').sub('', self.dynamic)
        # tag 별로 쪼갠다 (tags_of_dynamic)
        self.tags_of_dynamic = re.split('/', processed_dynamic)
        self.num_tags = len(self.tags_of_dynamic)
        # completed_x_paths 를 채운다
        self.add_xpath(self.static, 1)
        return

    # 최하위 xpath 를 완성시키고 completed_x_paths 에 담는다
    def add_xpath(self, xpath, idx_tail):
        if idx_tail == self.num_tags:
            xpath = xpath + self.suffix
            self.completed_xpath_s.append(xpath)
            # print(xpath)
            return
        # tail 을 붙인다
        added_xpath = xpath + '/' + self.tags_of_dynamic[idx_tail]
        ch_num = len(self.ch.driver.find_elements_by_xpath(added_xpath))
        # ch_num = self.ch.count_these_xpath(added_xpath)
        if ch_num > 1:
            for idx in range(ch_num):
                d_added_xpath = added_xpath + f'[{idx + 1}]'
                # print(d_added_xpath)
                self.add_xpath(d_added_xpath, idx_tail + 1)
        else:
            # print(added_xpath)
            self.add_xpath(added_xpath, idx_tail + 1)
        return

