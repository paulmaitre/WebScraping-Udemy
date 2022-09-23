# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 11:46:24 2022

@author: paulm
"""
##### AUTOMATING PYTHON SCRIPTS #####

##### Set up
# imports 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import WebDriverWait 
from bs4 import BeautifulSoup
import pandas as pd
import time 

# to get execution time
t0 = time.time()


###### Target job name
JOB = "Data Scientist"


###### number of offers to get max
NB_PAGES = 20 


##### Indeed web page
# login web page
chromeOptions = Options()
chromeOptions.add_argument("--kiosk")
driver = webdriver.Chrome(r"path to your \chromedriver.exe", chrome_options=chromeOptions) #Would like chrome to start in fullscreen
url = 'https://fr.indeed.com'
driver.get(url)
time.sleep(3)



##### Wait 10s (max) for web bar to load 
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="text-input-what"]')))

##### do the search
# job
search = driver.find_element_by_xpath('//*[@id="text-input-what"]')
search.send_keys(JOB)
search.send_keys(Keys.ENTER)
time.sleep(3)

# lets get data 
cpt_pages = 1
dataframe = pd.DataFrame({'Link':[''], 'Job Title':[''], 'Company':[''], 'Location':[''],'Salary':[''], 'Date':['']})
while True:
    # limit the nbr of pages scrapped
    if cpt_pages > NB_PAGES:
        break
    
    ##### grab HTML
    soup = BeautifulSoup(driver.page_source, 'lxml')
    ##### nested HTML
    nested_soup = soup.find('ul', class_='jobsearch-ResultsList css-0')
    
    ##### get data into a dataframe 
    
    
    postings = nested_soup.find_all('div', class_='job_seen_beacon')
    for post in postings:
        # get link
        try:
            link = post.find('a').get('href')
            full_link = url + link
            #print(f"\nfull_link = {full_link}")
        except:
            #print("\nno link\n")
            link = 'null'
        
        # get title
        try:
            title = post.find('a').text
            #print(f"\ntitle = {title}")
        except:
            #print("\nno title")
            title = 'null'
        
        # get company
        try:
            company = post.find('span', class_='companyName').text
            #print(f"\ncompany = {company}")
        except:
            #print("\nno company")
            company = 'null'
        
        # get salary
        try:
            salary = post.find('div', class_='metadata salary-snippet-container').text
            #print(f"\salary = {salary}")
        except:
            #print("\nno salary")
            salary = 'null'
    
        # get date
        try:
            date_list = post.find('span', class_='date').text.split() # get date 
            # put date in a shorter format
            date = date_list[-4]
            for word in date_list[-3:]:
                date = date+' '+word
            print(f"\ndate = {date}")
        except:
            #print("\nno date")
            date = 'null'
    
        # get location
        try:
            location = post.find('div', class_='companyLocation').text
            #print(f"\nlocation = {location}")
        except:
            #print("\nno location")
            location = 'null'
        
            
        dataframe = dataframe.append({'Link':full_link,
                                      'Job Title':title,
                                      'Company':company,
                                      'Location':location,
                                      'Salary':salary,
                                      'Date':date}, ignore_index = True)
    
    try: 
        # click on next page
        next_page = soup.find('a', {'aria-label':'Suivant'}).get('href')
        #print(f"\nnext page = {next_page}")
        full_next_page = url+next_page
        #print(f"\nlink next page = {full_next_page}")
        driver.get(full_next_page)
        print(f"page number {cpt_pages}")
        cpt_pages += 1
       
    except: 
        print("\nNo more pages.")
        print(f"\nNumber of pages scrapped = {cpt_pages}.")
        break
 
##### put data into a csv file
dataframe = dataframe[1:]
dataframe.to_csv(r"path to your \offers.csv")

##### ENDING
# close web page
driver.close()
driver.quit()
# to get execution time
tf = time.time()
# execution time
delta = tf-t0
##### end of the web scraping script
print("\nDONE at",time.strftime('%X %x'),"in", delta,"seconds.\n")
print("\nCode by Paul Maitre")



