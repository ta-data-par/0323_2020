#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 09:15:52 2020

@author: jidekickpush
"""
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By 
from selenium.common.exceptions import TimeoutException
import re
import time

#global Values
url = 'https://www.startupranking.com/top/0/2'
url_pattern=url[:-1]
url_pattern2=url[:-8]
numiter=2 #number of page to scrap

def scrap_home_page(url_pattern,numiter):
    
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
            list_urls.extend(urls_on_the_page)
           
        except TimeoutException:
            print ("Loading took too much time!")
    time.sleep(5)
    return list_urls
time.sleep(5)

def scrap_startup_page(url_pattern,url_companie):
    driver= webdriver.Chrome('/Users/jidekickpush/Downloads/chromedriver')        
    df_companie=pd.DataFrame()
    for p in url_companie:
        driver.get(url_pattern2+str(p))
        delay = 50 # seconds
        c_dict=dict()
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'sm-search-button')))
            print ("Page is ready!")
            soup=BeautifulSoup(driver.page_source,"lxml")
            
        
            #description = soup.select('div.su-info p')[0].text.strip()
            #c_dict['description']=description
            
            name=soup.select('div.su-info h2 a')[0].text
            c_dict['name']=name
            
            # founded date
            tabb = soup.select('div.su-info p.su-loc')
            if len(tabb)==0: 
                founded_date = ''
            else:
                founded_date =  tabb[0].text.strip()
            c_dict['founded_date']=founded_date
            
            # category_list
            cat = soup.select('div.su-tags.group ul li')
            category_list =[i.text for i in cat]
            category_string=[','.join(category_list)]
            c_dict['category_list']=category_string
            time.sleeo(5)
            
            driver.get(url_pattern2+'/startup'+str(p)+'/funding-rounds')
            try:
                WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'sm-search-button')))
                print ("Page is ready!")
                soup=BeautifulSoup(driver.page_source,"lxml")
                tabs2 = soup.select('.ranks')[0]
                rows2=tabs2.find_all('tr')
                
                
                #NEED TO BE FIX
                if len(rows2)<=1 :
                    c_dict['Total_funding_amount']=0
                else:
                    list_funding_amount = [i.select('span')[0].text for i in rows2]
                    list_funding_amount = list(filter(lambda a: a != 'Undisclosed amount', list_funding_amount))
                    funding_amount_dolar = [int(re.search(r'[0-9]+',i.replace(',','')).group(0)) for i in list_funding_amount]
                    Total_funding_amount = sum(funding_amount_dolar)
                    c_dict['Total_funding_amount']=Total_funding_amount
            except TimeoutException:
                print ("Loading took too much time!")
            
            time.sleep()

            c_df=pd.DataFrame.from_dict(c_dict)            
            df_companie=df_companie.append(c_df)

        except TimeoutException:
            print ("Loading took too much time!")
        time.sleep(5)
    driver.close()    
    return df_companie


if __name__=='__main__':
    list_url=scrap_home_page(url_pattern,numiter)
    df_companie=scrap_startup_page(url_pattern2,list_url)