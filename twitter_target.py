# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 06:20:05 2022

@author: paulm
"""

#----------- Script Python to scrap tweets from a target's twitter page -----------#

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

# number of tweets to get (depending numbers of tweets available)
NB_TWEETS = 1000

###### Target twitter account name (MUST BE PRECISE ENOUGH TO BE THE FIRST ONE DISPLAYED)
TARGET = "INSERT TARGET NAME" 

##### Connexion to your personnal account
# login web page
chromeOptions = Options()
chromeOptions.add_argument("--kiosk")
driver = webdriver.Chrome(r"path to your \chromedriver.exe", chrome_options=chromeOptions) # Would like chrome to start in fullscreen
driver.get('https://twitter.com/login')
time.sleep(3)


# login input
login = driver.find_element_by_xpath('//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
login.send_keys("INSERT YOUR EMAIL ADDRESS")
login.send_keys(Keys.ENTER)
time.sleep(3)

# sometimes ask for username input
try : 
    login_v2 = driver.find_element_by_xpath('//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input')
    login_v2.send_keys("INSERT YOUR USERNAME")
    button_1 = driver.find_element_by_xpath('//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div').click()
    time.sleep(3)
except:
    pass

# password input
password = driver.find_element_by_xpath('//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
password.send_keys("INSERT YOUR PASSWORD")
button_2 = driver.find_element_by_xpath('//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div').click()

##### Wait 10s (max) for web bar to load 
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input')))

##### do the search 
search = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input')
search.send_keys(TARGET)
search.send_keys(Keys.ENTER)
time.sleep(3)

##### clik on people section
people = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[3]/a/div').click()
time.sleep(3)

##### click on the profil
profil_link = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/section/div/div/div[1]/div/div/div/div/div[2]/div[1]/div[1]/div/div[1]/a/div/div[1]/span').click()
time.sleep(3)

##### get data about postings 
soup = BeautifulSoup(driver.page_source, 'lxml')
postings = soup.find_all('div', class_='css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0')
tweets = [] # list containing text of tweets of the current page
length = 0 
while True:
   for post in postings: # for each post of the posting into the current html 
       tweets.append(post.text) # get only text
   driver.execute_script('window.scrollTo(0, document.body.scrollHeight)') # scrolling down the page (part of the infinite page, can be define with a number precised in argument)
   time.sleep(2)
   soup = BeautifulSoup(driver.page_source, 'lxml') # get current html
   postings = soup.find_all('div', class_='css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0') # get current postings
   tweets_bis = list(set(tweets)) # drop duplicates tweets 
   if ((len(tweets_bis) > NB_TWEETS) or (len(tweets_bis)==length)): # stop when whe have enough (unique) tweets or when we can't add more tweets 
       if (len(tweets_bis)==length):
           print(f"\n/!\ WARNING : Il n'y a que {len(tweets_bis)-1} tweets disponibles.\n")
       break 
   length = len(tweets_bis)

##### example of getting specific tweets (about bots)
bot_tweets = []
for i in tweets_bis:
    if 'bot' in i:
        bot_tweets.append(i)
        
##### put data into a dataframe
dataframe = pd.DataFrame({'Tweet':[]}) # dataframe initialisation
dataframe['Tweet'] = tweets_bis # add data
dataframe = dataframe[1:] # delete firt empty row

##### save dataframe into a csv file 
dataframe.to_csv(r"INSERT PATH FOR CSV FILE\tweets.csv")

# close the web page
driver.close()
# to get execution time
tf = time.time()
# execution time
delta = tf-t0
##### end of the web scraping script
print("\nDONE at",time.strftime('%X %x'),"in", delta,"seconds.")
