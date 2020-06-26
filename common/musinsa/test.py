# import database
import re
# import os
# import requests as rq
# from bs4 import BeautifulSoup as bs
# import database
# import urllib
# import time
import page
# import browser

# products that have same code
# r_url = 'https://store.musinsa.com/app/product/detail/837741/0'
# b_url = 'https://store.musinsa.com/app/product/detail/837739/0'
#
# code = 'AX08'
# --------------------------------------------------------------

l = page.ListPage('https://store.musinsa.com/app/items/lists/001001')
n = l.get_total_product()
print(n-27000-934)