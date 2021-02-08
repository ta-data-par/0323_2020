#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 02:58:30 2020

@author: jidekickpush
"""
""" What is the relation between shark attacks, seasons and human activity? 
      - Seasonality of the attacks
      - Human activity vs shark attack
      - Activity vs fatal shark attack"""
  
import pandas as pd
import re
import matplotlib.pyplot as plt



#year=2005
year=int(input('Enter the year: '))

def acquisition():
    df=pd.read_csv('/Users/jidekickpush/Documents/GitHub/0323_2020DATAPAR/Labs/module_1/Pipelines-Project/Data/GSAF5.csv', encoding ='cp1252')
    return df

def data_cleaning(df):
    null_cols = df.isnull().sum()
    null_cols
    null_cols[null_cols > 0]
    
    df=df.drop(['Unnamed: 22','Unnamed: 23','Case Number.1','Case Number.2','Date','Type','Name', 'Sex ','Age','Injury','Time','Species ','Investigator or Source','pdf','href formula', 'href'], axis=1)
    
    df.rename(columns={'original order':'Id','Country':'Place'}, inplace = True)
    
    df=df[df['Year']>1900]
    
    df.replace(regex={
    r'\?':'', 
    r'\s\/\s[A-Z\s]+': '', 
    r'\s$':'', r'^\s':''
    }, inplace=True)
    
    df['Activity'] = df['Activity'].fillna('Not_Identified')
    
    df.rename(columns={'Activity':'unActivity'}, inplace=True)
    df_activity = df['unActivity']
    activity = []
    for a in df_activity:
        if re.search(r'Not_y[\w\s\,]+|Not_[\w\s\,]+|[\w\s\,]+Not_[\w\s\,]+', str(a)):
            a = 'Not_Identified'
        elif re.search(r'Surf[\w\s\,]+|surf[\w\s\,]+|[\w\s\,]+surf[\w\s\,]+', str(a)):
            a = 'Surfing'
        elif re.search(r'Board[\w\s\,]+|board[\w\s\,]+|[\w\s\,]+board[\w\s\,]+', str(a)):
            a = 'Surfing'
        elif re.search(r'Fish[\w\s\,]+|fish[\w\s\,]+|[\w\s\,]+fish[\w\s\,]+', str(a)):
            a = 'Fishing'
        elif re.search(r'Spear[\w\s\,]+|spear[\w\s\,]+|[\w\s\,]+spear[\w\s\,]+', str(a)):
            a = 'Fishing'
        elif re.search(r'Swim[\w\s\,]+|swim[\w\s\,]+|[\w\s\,]+swim[\w\s\,]+', str(a)):
            a = 'Swimming'
        elif re.search(r'Bath[\w\s\,]+|bath[\w\s\,]+|[\w\s\,]+bath[\w\s\,]+', str(a)):
            a = 'Bathing'
        elif re.search(r'Wadi[\w\s\,]+|wadi[\w\s\,]+|[\w\s\,]+wadi[\w\s\,]+', str(a)):
            a = 'Bathing'
        elif re.search(r'Snor[\w\s\,]+|snor[\w\s\,]+|[\w\s\,]+snor[\w\s\,]+', str(a)):
            a = 'Snorkeling'
        elif re.search(r'Div[\w\s\,]+|div[\w\s\,]+|[\w\s\,]+div[\w\s\,]+', str(a)):
            a = 'Diving'
        elif re.search(r'Boat[\w\s\,]+|boat[\w\s\,]+|[\w\s\,]+boat[\w\s\,]+', str(a)):
            a = 'Boating'
        elif re.search(r'Sail[\w\s\,]+|sail[\w\s\,]+|[\w\s\,]+sail[\w\s\,]+', str(a)):
            a = 'Boating'
        elif re.search(r'Crui[\w\s\,]+|crui[\w\s\,]+|[\w\s\,]+crui[\w\s\,]+', str(a)):
            a = 'Boating'
        else: a = 'Others'
        activity.append(a)
    df['Activity'] = activity
    df = df.drop(['unActivity'], axis=1)
    
    df['Date']=df['Case Number']
    df['Date'].replace(regex = {r'.[A-Za-z]$':''}, inplace = True)
    
    df['Month']=[m[5:7] for m in df['Case Number']]
    df['Month'].astype(int)
    # Get 'Months' of indexes for which column month has value 00
    indexMonth = df[ df['Month'] == '00' ].index
 
    # Delete these row indexes from dataFrame
    df.drop(indexMonth , inplace=True)
    
    df.rename(columns={ 'Fatal (Y/N)' : 'Fatal'}, inplace=True)
    df = df.replace({'Fatal': { 'N' : '0', 'Y' : '1', 'n' : '0', 'y' : '1', 'UNKNOWN' : '0', 'F' : '0', '#VALUE!' : '0'}})
    df['Fatal'].astype(bool)
    
    df = df[['Id','Date', 'Year', 'Month', 'Place', 'Area','Location', 'Activity', 'Fatal']]
    return df

def binning(df):
    season_labels=['Winter','Spring','Summer','Fall']
    cutoffs= ['00','04','07','10','12']
    bins = pd.cut(df['Month'], cutoffs, labels=season_labels)
    df['Season']=bins
    return df

def filter_by_year(df):
    global year
    filtered=df[df.Year==year]
    return filtered

"""Seasonality of the attacks"""

def seasonality_attacks(df):
    seasonality = df.pivot_table(index=['Season'], values=['Date'], aggfunc= len,fill_value=0)
    seasonality = seasonality.rename(columns= {'Date':'Count'})
    seasonality['Ratio'] = seasonality['Count'] * 100 / seasonality['Count'].sum()
    seasonality = seasonality.round({'Ratio':2})
    df_view1 = seasonality.T
    display(df_view1)
    return df

def viz_seasonality_attacks(df):
    global year
    barchart=df.groupby('Season')['Season']\
        .value_counts()\
        .unstack(level=0)\
        .plot.bar(stacked=False)
    plt.title(f"Season vs shark attack during the {year}")
    plt.show()    
    return barchart

"""Human activity vs shark attack"""
    
def activity_season(df):
    activity_season = df.pivot_table(index=['Activity', 'Season'], values=['Date'], aggfunc= len, fill_value=0) 
    activity_season = activity_season.rename(columns= {'Date' : 'Count'})
    activity_season['Ratio'] = activity_season['Count'] * 100 / activity_season['Count'].sum() 
    activity_season = activity_season.round({'Ratio' : 2})
    activity_season.sort_values(by=['Activity','Ratio'], ascending=False, inplace=True)
    df_view2 = activity_season.T
    display(df_view2)
    return df

def viz_activity_season(df):
    global year
    barchart=df.groupby('Season')['Activity']\
        .value_counts()\
        .unstack(level=0)\
        .plot.bar(stacked=False)
    plt.title(f"Human activity vs shark attack during the {year}")
    plt.show()
    return barchart
"""Activity vs fatal shark attack"""

def activity_fatal(df):
    fatal_activity = df.pivot_table(index=['Activity', 'Fatal'], values=['Date'], aggfunc= len, fill_value=0) 
    fatal_activity = fatal_activity.rename(columns= {'Date' : 'Count'})
    fatal_activity['Ratio'] = fatal_activity['Count'] * 100 / fatal_activity['Count'].sum() 
    fatal_activity = fatal_activity.round({'Ratio' : 2})
    df_view3 = fatal_activity.T
    display (df_view3)
    return df

def viz_activity_fatal(df):
    global year
    barchart=df.groupby('Activity')['Fatal']\
        .value_counts()\
        .unstack(level=1)\
        .plot.bar(stacked=False)
    plt.title(f"Activity vs fatal shark attack during the {year}")
    plt.show()
    return barchart



if __name__=='__main__':
    data_raw=acquisition()
    data_cleaned=data_cleaning(data_raw)
    data_binning=binning(data_cleaned)
    data_filtered=filter_by_year(data_binning)
    data_seasonality = seasonality_attacks(data_filtered)
    data_viz_seasonality_attacks = viz_seasonality_attacks(data_filtered)
    data_activity_season = activity_season(data_filtered)
    data_viz_activity_season = viz_activity_season(data_filtered)
    data_sactivity_fatal = activity_fatal(data_filtered)
    data_viz_activity_fatal = viz_activity_fatal(data_filtered)
    
    #save_fig = viz_activity_season(barchart)
    
    
    
    
    
    
    
    
    