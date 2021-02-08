#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 21:16:45 2020

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


url_scrapped=pd.read_csv('/Users/jidekickpush/Documents/GitHub/0323_2020DATAPAR/Projects/url_scraping.csv')
los=url_scrapped.values.tolist()

url = 'https://www.startupranking.com/top/0/2'

def scrap_startup_page(url_pattern,url_companie):
    driver= webdriver.Chrome('/Users/jidekickpush/Downloads/chromedriver')        
    df_companie=pd.DataFrame()
    for p in url_companie:
        driver.get(url_pattern+p[0])
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
            
            driver.get(url_pattern+'/startup'+p[0]+'/funding-rounds')
            try:
                WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'sm-search-button')))
                print ("Page is ready!")
                soup=BeautifulSoup(driver.page_source,"lxml")
                tabs2 = soup.select('.ranks')[0]
                rows2=tabs2.find_all('tr')
                list_funding_amount = [i.select('span')[0].text for i in rows2]
                list_funding_amount = list(filter(lambda a: a != 'Undisclosed amount', list_funding_amount))
                funding_amount_dolar = [int(re.search(r'[0-9]+',i.replace(',','')).group(0)) for i in list_funding_amount]
                Total_funding_amount = sum(funding_amount_dolar)
                c_dict['Total_funding_amount']=Total_funding_amount
            except TimeoutException:
                print ("Loading took too much time!")
            

            c_df=pd.DataFrame.from_dict(c_dict)            
            df_companie=df_companie.append(c_df)

        except TimeoutException:
            print ("Loading took too much time!")
    driver.close()    
    return df_companie

lol=scrap_startup_page(url[:-8],los)

"""
def scrap_startup_page(url_pattern,url_companie):
    los=url_scrapped.values.tolist()
    driver= webdriver.Chrome('/Users/jidekickpush/Downloads/chromedriver')    
    df_companie=pd.DataFrame()
    for p in los[:30]:
        driver.get(url_pattern+str(p))
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
            
            driver.get(url_pattern+'/startup'+str(p)+'/funding-rounds')
            try:
                WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'sm-search-button')))
                print ("Page is ready!")
                soup=BeautifulSoup(driver.page_source,"lxml")
                tabs2 = soup.select('.ranks')[0]
                rows2=tabs2.find_all('tr')
                list_funding_amount = [i.select('span')[0].text for i in rows2]
                list_funding_amount = list(filter(lambda a: a != 'Undisclosed amount', list_funding_amount))
                funding_amount_dolar = [int(re.search(r'[0-9]+',i.replace(',','')).group(0)) for i in list_funding_amount]
                Total_funding_amount = sum(funding_amount_dolar)
                c_dict['Total_funding_amount']=Total_funding_amount
            except TimeoutException:
                print ("Loading took too much time!")
            

            c_df=pd.DataFrame.from_dict(c_dict)            
            df_companie=df_companie.append(c_df)

        except TimeoutException:
            print ("Loading took too much time!")
    driver.close()    
    return df_companie

lol=scrap_startup_page(url[:-8],url_scrapped)
"""
print(lol)