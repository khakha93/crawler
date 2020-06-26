# from selenium.webdriver.common.keys import Keys
from selenium import webdriver as wb
# import time


class Chrome(object):
    # def __init__(self):
    #     path = "C:/Users/jjkha/Downloads/chromedriver.exe"
    #     self.driver = wb.Chrome(path)

    def __init__(self, url):
        path = "/home/hero/utils/chromedriver"
        self.driver = wb.Chrome(path)
        self.driver.get(url)

    def move(self, url):
        self.driver.get(url)

    # 이건 고민 좀 더 해봐야할 듯
    def next_list(self, i):
        self.driver.execute_script('listSwitchPage(document.f1, \'%i\')' % i, False)