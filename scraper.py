from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv


def infinite_scrolling():
    SCROLL_PAUSE_TIME = 1

    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")
    
    while True:
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
    
        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

#opening page with selenium
test_url = 'https://play.google.com/store/apps/category/GAME'
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
chromedriver = 'C:\Program Files (x86)\chromedriver.exe' #path to chromedriver
browser = webdriver.Chrome(chromedriver, options=option)
browser.get(test_url)
infinite_scrolling()
html_source = browser.page_source
soup=BeautifulSoup(html_source, "html.parser")


#GETTING GAMES FROM RECOMMENDED, POPULAR, BEST - things found in test_url
database_list = []
links_to_categories = soup.find_all('div', {'class','W9yFB'})
#add some other categories V
links_to_categories.append("https://play.google.com/store/apps/collection/cluster?clp=0g4cChoKFHRvcHNlbGxpbmdfZnJlZV9HQU1FEAcYAw%3D%3D:S:ANO1ljJ_Y5U&gsr=Ch_SDhwKGgoUdG9wc2VsbGluZ19mcmVlX0dBTUUQBxgD:S:ANO1ljL4b8c")
for category in links_to_categories:
    link_to_category = 'https://play.google.com'+category.find('a')['href']
    browser.get(link_to_category)
    infinite_scrolling()
    html_source = browser.page_source
    soup=BeautifulSoup(html_source, "html.parser")
    links_to_games = soup.find_all('div', {'class','b8cIId ReQCgd Q9MA7b'})
    for game in links_to_games:
        link_to_game = 'https://play.google.com'+game.find('a')['href']
        browser.get(link_to_game)
        html_source = browser.page_source
        soup=BeautifulSoup(html_source, "html.parser")
        #SCRAPING GAME PAGE
        #title >> author - [0], category - [1] 
        author_category_name = soup.find_all('span', {'class','T32cc UAO9ie'})
        title = soup.find_all('h1', {'class','AHFaub'})
        try:
            num_of_ratings = soup.find_all('span', {'class','AYi5wd TBRnV'})
            num_of_ratings = num_of_ratings[0].get_text().replace("&nbsp;", "").replace("\xa0", "")
        except:
            num_of_ratings = 0
        description = soup.find_all('div', {'class', 'DWPxHb'})
        try:
            pegi = soup.find_all('div', {'class','KmO8jd'})
        except:
            pegi = 0
        price = soup.find_all('div', {'class', 'hfWwZc'})
        try:
            price = price[0].find('span').get_text()
        except:
            price = "n/a"
        try: 
            stars = soup.find_all('div', {'class', 'dNLKff'})
            stars = stars[0].find('div')
            #stars = "Ocena w gwiazdkach: x,x na 5"
            stars = stars.find('div')['aria-label']
            # getting only rating from stars
            stars = stars[-8:-5].replace(",", ".")
        except:
            stars = 0
        print(stars)
        database_list.append([title[0].get_text(), 
            author_category_name[0].get_text(), 
            author_category_name[1].get_text(), 
            int(num_of_ratings), 
            price, 
            float(stars),
            description[0].get_text().replace('<br>', ' '), 
            int(pegi[0].get_text().replace('PEGI ', ''))])


# CREATING CSV
header = ['title','firm','genre','num_of_reviews', 'price', 'stars', 'description_lenght','PEGI']
for item in database_list:
    # change description to description lenght
    item[-2] = len(item[-2])
with open('short_game.csv','w', encoding="UTF8", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for item in database_list:
        writer.writerow(item)