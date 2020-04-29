#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 13:26:56 2020

@author: jidekickpush
"""

import requests as r
import pandas as pd
from bs4 import BeautifulSoup as bs
import time

def collect_data(url):
    collect_df=pd.DataFrame()
    for i in range(2):
        url=f'https://www.la-spa.fr/adopter-animaux?field_esp_ce_value=All&page={1+i}'
        html = r.get(url).content
        append_str = 'https://www.la-spa.fr/adopter-animaux'
        soup = bs(html, "lxml");

        animals=soup.select('div h3 a[href]')
        links=[l['href'] for l in animals]
        all_links=[append_str + link if link.startswith('/') else link for link in links ]

        animal_dict = {'all_links': all_links} 
        df=pd.DataFrame(animal_dict)
        collect_df=collect_df.append(df)
        time.sleep(2)

    print('Process complete')
    print('We found :',len(collect_df),'results')
    return collect_df
df=collect_data('https://spa-notifadoption.herokuapp.com/refuges')


def scrapped_df(all_links):
    data_df=pd.DataFrame()

    for links in all_links:
        url=links
        html = r.get(url).content
        soup = bs(html, "lxml")
        dict_animal=dict()

        n=soup.select('div.field-label:contains("Nom")+div')
        Name=[name.text for name in n]
        dict_animal['Name']=Name
        
        ra=soup.select('div.field-label:contains("Race")+div')
        Race=[race.text for race in ra]
        dict_animal['Race / Apparence']=Race
        
        sp=soup.select('div.field-label:contains("Espèce")+div')
        Specy=[specy.text for specy in sp]
        dict_animal['Specy']=Specy
        
        s=soup.select('div.field-label:contains("Sexe")+div')
        Sex=[sexe.text for sexe in s]
        dict_animal['Sex']=Sex
        
        b=soup.select('div.field-label:contains("Date Naissance")+div')
        Birthday=[birthday.text for birthday in b]
        dict_animal['Birthday']=Birthday
        
        desc=soup.select('div.field-items p')
        Description=[des.text for des in desc]
        dict_animal['Description']='\n'.join(Description)

        adress=soup.select('.addr')
        dict_animal['refuge_adress']=[refuge_adress.text.strip()[5:] for refuge_adress in adress]
        dict_animal['refuge_number']=[refuge_number.text.strip()[:2] for refuge_number in adress]

        contacts=soup.select('.contacts')
        dict_animal['contact_mail']=[contact_num.text.split()[0] for contact_num in contacts]
        dict_animal['contact_num']=[contact_num.text.split()[1] for contact_num in contacts]
        
        
        
        data_animal_df=pd.DataFrame.from_dict(dict_animal)
        data_df=data_df.append(data_animal_df)
        print(data_df)
    return data_df
data_df=scrapped_df(df.all_links)


 
#collect_data('https://www.la-spa.fr/adopter-animaux')      
#if __name__=='__main__':
#    df=collect_data('https://spa-notifadoption.herokuapp.com/refuges')
#    data_df=scrapped_df(df.all_links) 
   