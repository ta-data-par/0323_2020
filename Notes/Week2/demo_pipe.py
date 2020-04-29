# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 12:18:25 2020

@author: eldii
"""

# Problem Definition:
## Deduce TOP-10 Manufacturers by Fuel Efficiency for given year
import pandas as pd
year=int(input('Enter the year: '))

def acquisition():
    df=pd.read_csv('C:\\Users\\eldii/Documents/vehicles.csv')
    return df

def wrangle(df):
    global year
    filtered=df[df.Year==year]
    return filtered

def analyze(df):
    grouped=df.groupby('Make')['Combined MPG'].agg('mean').reset_index()
    final=grouped.sort_values('Combined MPG', ascending=False).head(10)
    return final

def viz(df):
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set()
    global year
    fig,ax=plt.subplots(figsize=(15,8))
    barchart=sns.barplot(data=df, x='Make',y='Combined MPG')
    plt.title("Top 10 Manufacturers by Fuel Efficiency in", year)
    return barchart

def save_viz(plot):
    fig=plot.get_figure()
    global year
    fig.savefig("Top 10 Manufacturers by Fuel Efficiency in",year,".png")
    
    
if __name__=='__main__':
    data=acquisition()
    filtered=wrangle(data)
    results=analyze(filtered)
    barchart=viz(results)
    save_viz(barchart)