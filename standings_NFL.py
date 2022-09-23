# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 12:08:25 2022

@author: paulm
"""

# Exercise for the online course : 
# "Web Scraping in Python With BeautifulSoup & Selenium 2022"

# EX 2 : Scrap data from a Table (NFL Standings 2022 regular season)

#-------------------------------------------------------------------

##### setup 
import requests
from bs4 import BeautifulSoup 
import pandas as pd

url = 'https://www.nfl.com/standings/league/2019/REG'

page = requests.get(url)
#print(page)


##### get HTML code
soup = BeautifulSoup(page.text, 'lxml')
#print(soup)


##### get nested HTML (only the table)
table = soup.find('div', class_='d3-o-table--horizontal-scroll')
#print(table)


##### get columns names
headers = []
for th in table.find_all('th'):
    header = th.text
    headers.append(header)
#print(headers)


##### create dataframe
df = pd.DataFrame(columns = headers)
for tr in table.find_all('tr')[1:]: # not getting headers again 
    raw_data = tr.find_all('td') # extract row data
    row = [el.text for el in raw_data] # extract each value for each column
    idx = len(df) # row index
    df.loc[idx] = row

print(df)

df.to_csv(r"C:\Users\paulm\OneDrive\Documents\WebScraping\NFL_2k19_standings.csv")
