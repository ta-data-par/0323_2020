#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 08:41:15 2020

@author: jidekickpush
"""

import requests as r
from bs4 import BeautifulSoup as bs
import time

my_url='https://www.startupranking.com/top/0/1'
#opening connection, grabbing the page
uClient = r.get(my_url).content
time.sleep(5)
page_html = uClient

#html parsing
page_soup = bs(page_html,'lxml');

#grab each name + links
ext_name = page_soup.select('a')
print(ext_name)
