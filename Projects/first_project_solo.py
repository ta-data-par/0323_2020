# Problem Definition:
## Deduce TOP-10 Manufacturers by Fuel Efficiency for given year
"""import pandas as pd
year=int(input('Enter the year: '))
​
def acquisition():
    df=pd.read_csv('/Users/jidekickpush/Documents/GitHub/0323_2020DATAPAR/Labs/vehicles/vehicles.csv')
    return df
​
def wrangle(df):
    global year
    filtered=df[df.Year==year]
    return filtered
​
def analyze(df):
    grouped=df.groupby('Make')['Combined MPG'].agg('mean').reset_index()
    final=grouped.sort_values('Combined MPG', ascending=False).head(10)
    return final
​
def viz(df):
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set()
    global year
    fig,ax=plt.subplots(figsize=(15,8))
    barchart=sns.barplot(data=df, x='Make',y='Combined MPG')
    plt.title("Top 10 Manufacturers by Fuel Efficiency in", year)
    return barchart
​
def save_viz(plot):
    fig=plot.get_figure()
    global year
    fig.savefig("Top 10 Manufacturers by Fuel Efficiency in",year,".png")
    
    
if __name__=='__main__':
    data=acquisition()
    filtered=wrangle(data)
    results=analyze(filtered)
    barchart=viz(results)
    save_viz(barchart)"""
    
    

import pandas as pd
import numpy as np
import re

year=2016

def acquisition():
    df=pd.read_csv('/Users/jidekickpush/Documents/GitHub/0323_2020DATAPAR/Labs/module_1/Pipelines-Project/Data/GSAF5.csv', encoding ='cp1252')
    return df

def data_cleaning(df):
    #From the table overview, we can see the following statements:
    #* columns 'unnamed: 22' and 'unnamed: 23' are not referenced in the description of the dataset and doesn't contain any (relevant) information.
    #* columns 'Case Number.1' and 'Case Number.2'are duplicates of 'Case Number'
    #* columns 'date' cannot be nomalised cause of the differents syntaxes but the information can be extract from column 'Case Number'
    #=> Proceed to drop those columns
    null_cols = df.isnull().sum()
    null_cols
    null_cols[null_cols > 0]
    df=df.drop(['Unnamed: 22','Unnamed: 23','Case Number.1','Case Number.2','Date'], axis=1)
    
    # Some names of the columns aren't clean or clear enough. Below the list of columns renamed
    #* Sex: remove a blank space at the end.
    df.rename(columns={'Sex ':'Sex', 'Country':'Place'}, inplace = True)
    
    
    #Among the total 5900 events registered, only 137 happened before 1700.
    #To evaluate only statistically relevant data, events registered before 1700 will not be considered
    df=df[df['Year']>1700]
    
    #Let's fix 'Sex' column: Typo found on 2 entrances.
    #For 'Place': We've reduced the list of countries from the original set of 196 categories, to 174.
    #=>For that purpose we have used both regular expressions and manual replacement.
    df.replace({'Sex':{'M ':'M'}}, inplace=True)
    
    #remove end ?
    #remove start/end blank spaces
    #remove 2nd country after /
    #df.columnname.str.replace('word','newword')
    df.replace(regex={
    r'\?':'', 
    r'\s\/\s[A-Z\s]+': '', 
    r'\s$':'', r'^\s':''
    }, inplace=True)
    
    #On 'Place' column, manually fixed some duplicates
    df.replace({'Place': { 'UNITED ARAB EMIRATES (UAE)':'UNITED ARAB EMIRATES', 
    'Fiji':'FIJI', 'ST. MAARTIN':'ST. MARTIN', 
    'Seychelles':'SEYCHELLES', 
    'Sierra Leone':'SIERRA LEONE', 
    'St Helena': 'ST HELENA', 
    'ENGLAND': 'UNITED KINGDOM', 
    'SCOTLAND': 'UNITED KINGDOM'}
    }, inplace=True)
    
    #Normalizing column Activity
    #Reduce from the original 1418 unique values on Activity to 5: 'Surfing', 'Swimming', 'Fishing', 'Diving' & 'Others'.
    df.rename(columns={'Activity':'unActivity'}, inplace=True)
    df_activity = df['unActivity']
    activity = []
    for a in df_activity:
        if re.search(r'Surf[\w\s\,]+|surf[\w\s\,]+|[\w\s\,]+surf[\w\s\,]+', str(a)):
            a = 'Surfing'
        elif re.search(r'Fish[\w\s\,]+|fish[\w\s\,]+|[\w\s\,]+fish[\w\s\,]+', str(a)):
            a = 'Fishing'
        elif re.search(r'Spear[\w\s\,]+|spear[\w\s\,]+|[\w\s\,]+spear[\w\s\,]+', str(a)):
            a = 'Fishing'
        elif re.search(r'Swim[\w\s\,]+|swim[\w\s\,]+|[\w\s\,]+swim[\w\s\,]+', str(a)):
            a = 'Swimming'
        elif re.search(r'Div[\w\s\,]+|div[\w\s\,]+|[\w\s\,]+div[\w\s\,]+', str(a)):
            a = 'Diving'
        else: a = 'Others'
        activity.append(a)
    df['Activity'] = activity
    df = df.drop(['unActivity'], axis=1)
    
    
    #Create a new column for dates, getting the information from the column 'Case Number'
    df['Date']=df['Case Number']
    df['Date'].replace(regex = {r'.[A-Za-z]$':''}, inplace = True)
    
    #Create a new column for the month, extracting it from the 'Case Number' column
    #* check if percentage of unrelevant dates : month missing in the data
    #=> drop the rows without specified month
    df['Month']=[m[5:7] for m in df['Case Number']]
    
    #Percentage of month not specified in the df is less than 10%, we decided to do not keep them:
    # Get 'Months' of indexes for which column month has value 00
    indexNames = df[ df['Month'] == '00' ].index
    # Delete these row indexes from dataFrame
    df.drop(indexNames , inplace=True)
    
    #Normalizing the hour, keeping only the values that correspond to a 24h value
    #df['Time'] = df['Time'].replace(regex = {r'\s[\w\-\d\/\()]+|\-[\w\-\d\/]+|j$|^\>|^\<':'', r'h':':'})
    #hour = []
    #time = df['Time']
    #for h in time:
     #   if re.search(r'\d{2}\:\d{2}', str(h)) == None:
    #        h = 'Unknown'
    #        hour.append(h)
    #df['Hour'] = hour
    
    #Change column types
    #Change the column Fatal (Y/N) to a boolean, normalizing all the entries to True or False.
    #The few unknown values have been trated as non fatal.
    df.rename(columns={ 'Fatal (Y/N)' : 'Fatal'}, inplace=True)
    df = df.replace({'Fatal': { 'N' : '0', 'Y' : '1', 'n' : '0', 'y' : '1', 'UNKNOWN' : '0', 'F' : '0', '#VALUE!' : '0'}})
    df['Fatal'].astype(bool)
    return df

def filter_by_year(df):
    global year
    filtered=df[df.Year==year]
    return filtered

def display_seasonality_attacks(df):
    #Binning the data by season on a new column
    season_labels=['Winter','Spring','Summer','Fall']
    cutoffs= ['01','04','07','10','12']
    bins = pd.cut(df['Month'], cutoffs, labels = season_labels)
    df['Season']=bins

    #Ratio of attacks per person
    seasonality = df.pivot_table(index=['Season'], values=['Date'], aggfunc= len,fill_value=0)
    seasonality = seasonality.rename(columns= {'Date':'Count'})
    seasonality['Ratio'] = seasonality['Count'] * 100 / seasonality['Count'].sum()
    seasonality = seasonality.round({'Ratio':2})
    #display(seasonality)
    return seasonality

def activity_season(df):
    activity_season = df.pivot_table(index=['Activity', 'Season'], values=['Date'], aggfunc= len, fill_value=0) 
    activity_season = activity_season.rename(columns= {'Date' : 'Count'})
    activity_season['Ratio'] = activity_season['Count'] * 100 / activity_season['Count'].sum() 
    activity_season = activity_season.round({'Ratio' : 2})
    activity_season.sort_values(by=['Activity','Ratio'], ascending=False, inplace=True)
    print(activity_season)
    return activity_season



#def viz(df):  
    #import matplotlib.pyplot as plt
    #import seaborn as sns
    #sns.set()
    #global year
   # fig,ax=plt.subplots(figsize=(15,8))
    #barchart=sns.barplot(data=df, x='Activity',y='Count')
    #plt.title("Attack per season during the year")
    #return barchart

if __name__=='__main__':
    data_raw=acquisition()
    data_cleaned=data_cleaning(data_raw)
    data_filtered=filter_by_year(data_cleaned)
    #final_table = data_filtered[['Date', 'Year', 'Month', 'Place', 'Area','Location', 'Activity', 'Sex', 'Fatal']]
    #display(final_table.head(10))
    data_seasonality = display_seasonality_attacks(data_filtered)
    display(data_seasonality)
    data_activity_season = activity_season(data_filtered)
    #data_viz = viz(data_activity_season)
    