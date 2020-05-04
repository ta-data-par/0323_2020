#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 21:43:53 2020

@author: jidekickpush
"""

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By 
from selenium.common.exceptions import TimeoutException

#from selenium.webdriver.chrome.options import Options
#opts = Options()
#opts.add_argument({""})


#global Values
url = 'https://www.startupranking.com/top/0/2'


def get_data(url_pattern,numiter):
    driver= webdriver.Chrome('/Users/jidekickpush/Downloads/chromedriver')
    # url = 'https://www.nseindia.com/live_market/dynaContent/live_watch/equities_stock_watch.htm'
    # with requests.Session() as session:
    #     session.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    
    
    list_urls=[]
    for p in range(1,numiter+1):
        driver.get(url_pattern+str(p))
        delay = 50 # seconds
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'search_location_state')))
            print ("Page is ready!")
            soup = BeautifulSoup(driver.page_source,"lxml")
            tabs=soup.find_all('table',{'class':'rank_table'})[0]
            rows=tabs.find_all('tr')
            urls_on_the_page=[i.select('a')[0].get('href') for i in rows]
            urls_on_the_page.pop(0)
            list_urls.append(urls_on_the_page)
           
        except TimeoutException:
            print ("Loading took too much time!")
    driver.close()    
    return list_urls

los=get_data(url[:-1],2)
import itertools

los2=(list(itertools.chain.from_iterable(los)))

url_scrapping=pd.DataFrame({'col':los2})
url_scrapping.to_csv('url_scraping.csv',index=False)


