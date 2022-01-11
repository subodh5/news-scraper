from bs4 import BeautifulSoup
import requests
import re
import csv

#functions
def extract_news(link):
    text=' '
    response=requests.get(link)
    soup=BeautifulSoup(response.content,'lxml')
    try:
        para_container=soup.find('div',class_="ok18-single-post-content-wrap")

    except AttributeError: 
        return ''

    else:
        for paragraph in para_container.find_all('p'):
            text+=paragraph.text   
        return text

#write to csv file
def writeToCSV(text):
    with open("C:\\Users\\subodh\\Desktop\\python\\scrap\\onlinekhabar\\okhabar9.csv", 'a', encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='|', quotechar='`', quoting=csv.QUOTE_ALL, lineterminator='\n')
        csvwriter.writerow(text)

    
# regular expression is defined to extract category
def findCategory(link):
    category=[]
    response=requests.get(link)
    soup=BeautifulSoup(response.content,'lxml')


    try:
        article=soup.find('article').get('class')

    #if category is not found, return empty list
    except AttributeError:      
        return category

    else:
        for element in article:
            if (re.findall('^category-', element)):
                category.append(element)
                return category



for i in range(50,0,-1):

    #onlinekhabar.com/'year'/'month'/page/'number'
    print(i)
    http="https://www.onlinekhabar.com/2021/12/page/" + str(i)

    response=requests.get(http)
    soup=BeautifulSoup(response.content,'lxml')
    news=soup.find_all("div",class_="span-4")

    for each_news in news:
        full_news=[]
        link=each_news.find('a',href=True).get('href')

        title=each_news.find("h2",class_="ok-news-title-txt").text
        category=findCategory(link)
        main_content=extract_news(link)


        if(category and title and main_content): 
            full_news.append(category)
            full_news.append(title)
            full_news.append(main_content)

            writeToCSV(full_news)
        # writeToFile(full_news)
