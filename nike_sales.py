# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 19:10:28 2022

@author: paulm
"""

##### REPLACE UNION LA #####
##### NIKE WEBSITE : sales infinite page


##### Setup
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import openpyxl

driver = webdriver.Chrome(r"path to your chromedriver.exe")

url = 'https://www.nike.com/fr/w/hommes-promotions-chaussures-3yaepznik1zy7ok'

driver.get(url)
time.sleep(3)

##### close cookies pop up 
try : 
    driver.find_element_by_xpath('//*[@id="gen-nav-commerce-header-v2"]/div[1]/div/div[2]/div/div[3]/div[1]/div[1]/button').click()
except:
    print("TimeOut (over 3sec)")
    pass
    
##### infinite scrolling to grab all the HTML 
last_height = driver.execute_script('return document.body.scrollHeight') # initial height 
while True:
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)') # scrolling all the page
    time.sleep(3)
    new_height = driver.execute_script('return document.body.scrollHeight') # new height (env x2)
    if new_height == last_height: # si la taille de la page n'augmente plus : fin du scroll
        break
    last_height = new_height # sinon on actualise la nouvelle hauteur et on continue 

##### get all HTML
soup = BeautifulSoup(driver.page_source, 'lxml')

##### get all products HTML  
products = soup.find_all('div', class_='product-card__body')

##### get data from each product and save it in a pandas DataFrame
dataframe = pd.DataFrame({'Link':[], 'Name':[], 'Subtitle':[], 'Price':[], 'Sale Price':[]})
for product in products:
    try:
        link = product.find('a', class_='product-card__link-overlay').get('href')
        name = product.find('div', class_='product-card__title').text
        subtitle = product.find('div', class_='product-card__subtitle').text
        temp_text = product.find('div', class_='product-card__price').text
        splitted_temp_text = temp_text.split(u"\N{euro sign}")
        price = splitted_temp_text[1]
        sale_price = splitted_temp_text[0]
        
        dataframe = dataframe.append({'Link':link, 'Name':name, 'Subtitle':subtitle, 'Price':price, 'Sale Price':sale_price}, ignore_index = True)
    except:
        print("\n/!\ erreur recuperation data")
        pass
 
    
# close the web page
driver.close()

# save the DataFrame in a csv file
dataframe.to_csv(r"path to your saved filed : nike_shoes_sales_men.csv")
 

print(f"\nDONE at {time.strftime('%X %x')}")
    
    