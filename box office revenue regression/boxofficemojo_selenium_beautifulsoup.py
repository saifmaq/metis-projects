from __future__ import print_function, division
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import numpy as np
import requests
import pickle
from bs4 import BeautifulSoup
import re

chromedriver = "/Applications/chromedriver" 
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver) 

def mojo_movie_scraper(url):
    ''' A function that parses an individual movie page from 
        BoxOfficeMojo.com and extracts relevant data'''
    driver.get(url)
    try:
        title = driver.find_element_by_xpath('//*[@id="body"]/table[2]/tbody/tr/td/table[1]/tbody/tr/td[2]/font/b')
        title = title.text
    except:
        title = np.NaN
        print(url)
    
    try:
        release_date = driver.find_element_by_xpath('//*[@id="body"]/table[2]/tbody/tr/td/table[1]/tbody/tr/td[2]/table/tbody/tr/td/center/table/tbody/tr[2]/td[2]/b/nobr')
        release_date = release_date.text
    except: 
        release_date = np.NaN
        print(url)
    
    try:
        runtime = driver.find_element_by_xpath('//*[@id="body"]/table[2]/tbody/tr/td/table[1]/tbody/tr/td[2]/table/tbody/tr/td/center/table/tbody/tr[3]/td[2]/b')
        runtime = runtime.text.replace('.','')
    except:
        runtime = np.NaN
        print(url)
    
    try:
        opening_weekend = driver.find_element_by_xpath('//*[@id="body"]/table[2]/tbody/tr/td/table[2]/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr/td[1]/div[2]/div[2]/table/tbody/tr[1]/td[2]')
        opening_weekend = opening_weekend.text.replace(',', '').replace('$','').replace(' ','')
        try:
            int(opening_weekend)
        except:
            opening_weekend = driver.find_element_by_xpath('//*[@id="body"]/table[2]/tbody/tr/td/table[2]/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr/td[1]/div[2]/div[2]/table[3]/tbody/tr[1]/td[2]')
            opening_weekend = opening_weekend.text.replace(',', '').replace('$','').replace(' ','')
    except:
        opening_weekend = np.NaN
        print(url)
    
    try:
        ow_as_percentage_of_total = driver.find_element_by_xpath('//*[@id="body"]/table[2]/tbody/tr/td/table[2]/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr/td[1]/div[2]/div[2]/table/tbody/tr[3]/td[2]')
        ow_as_percentage_of_total = ow_as_percentage_of_total.text.replace(' ','').replace('%','')
    except:
        ow_as_percentage_of_total = np.NaN
        print(url)
    try:
        domestic_total_gross = driver.find_element_by_xpath('//*[@id="body"]/table[2]/tbody/tr/td/table[1]/tbody/tr/td[2]/table/tbody/tr/td/center/table/tbody/tr[1]/td/font/b')
        domestic_total_gross = domestic_total_gross.text.replace(',', '').replace('$','').replace(' ','')
    except:
        domestic_total_gross = np.NaN
        print(url)
    
    try:
        yearly_rank = driver.find_element_by_xpath('//*[@id="body"]/table[2]/tbody/tr/td/table[2]/tbody/tr[2]/td/table/tbody/tr/td[1]/div[3]/div[2]/table/tbody/tr[3]/td[2]/font')
        yearly_rank = yearly_rank.text.replace(',','')
    except:
        yearly_rank = np.NaN
        print(url)

    try:
        all_time_rank = driver.find_element_by_xpath('//*[@id="body"]/table[2]/tbody/tr/td/table[2]/tbody/tr[2]/td/table/tbody/tr/td[1]/div[3]/div[2]/table/tbody/tr[2]/td[2]/font')
        all_time_rank = all_time_rank.text.replace(',','')
    except:
        all_time_rank = np.NaN
        print(url)


    try:
        genre = driver.find_element_by_xpath('//*[@id="body"]/table[2]/tbody/tr/td/table[1]/tbody/tr/td[2]/table/tbody/tr/td/center/table/tbody/tr[3]/td[1]/b')
        genre = genre.text
    except:
        genre = np.NaN
        print(url)

    try:
        rating = driver.find_element_by_xpath('//*[@id="body"]/table[2]/tbody/tr/td/table[1]/tbody/tr/td[2]/table/tbody/tr/td/center/table/tbody/tr[4]/td[1]')
        rating = rating.text
        rating = rating[12:].strip()
    except:
        rating = np.NaN
        print(url)
    

    movie_dict = dict(zip(headers, [title, 
                                    release_date, 
                                    runtime, 
                                    opening_weekend,
                                    opening_weekend_percentage,
                                    domestic_total_gross,
                                    genre,
                                    rating]))

    movie_data.append(movie_dict)

movie_data = []

headers = ['movie title', 'release date', 'runtime', 'opening weekend gross',
           'opening weekend percentage', 'domestic total gross','genre','rating']


movie_pages = []
content_list = []
charts = []

chart_url = 'https://www.boxofficemojo.com/yearly/'

#to scrape a list of charts that contain direct movie links on boxofficemojo: 
soup = BeautifulSoup(requests.get(chart_url).text, "lxml")
for link in soup.findAll('a', attrs={'href': re.compile("chart")}):
    charts.append(link.get('href'))

#to scrape each chart collected above for direct movie links:
def movie_list_scraper(chart, url):
    url = url.format(chart)
    soup = BeautifulSoup(requests.get(url).text, "lxml")
    for link in soup.findAll('a', attrs={'href': re.compile("yearly")}):
        content_list.append(link.get('href'))

def movie_page_scraper(chart, url):
    url = url.format(chart)
    soup = BeautifulSoup(requests.get(url).text, "lxml")
    for link in soup.findAll('a', attrs={'href': re.compile("movie")}):
        movie_pages.append(link.get('href')) 
    
#remove non-links, remove 2018 data 
charts = charts[4:-2]

url = 'https://www.boxofficemojo.com/yearly/{}'

for chart in charts:
    movie_page_scraper(chart, url)
    movie_list_scraper(chart, url)


#remove duplicate values
content_list = list(set(content_list))
movie_pages = list(set(movie_pages))

for content in content_list:
    movie_page_scraper(content, url)

movie_pages = list(set(movie_pages))

with open('movie_pages_list.pkl', 'wb') as picklefile:
    pickle.dump(movie_pages, picklefile)

direct_movie_urls = []
for page in movie_pages:
    urls.append('https://www.boxofficemojo.com/{}'.format(page))

for url in urls:
    mojo_movie_scraper(url)

moviedf = pd.DataFrame(movie_data)

with open('mojo_movies.pkl', 'wb') as picklefile:
    pickle.dump(moviedf, picklefile)



    



    

