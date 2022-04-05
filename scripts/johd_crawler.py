import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

base_URL = "https://openhumanitiesdata.metajnl.com/articles/"
URL = base_URL + '?f=1&f=2&order=date_published&app=100'

page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

results = soup.find("div", class_="article-list")
articles = results.find_all("li", class_="article-block")

todaysdate = str(datetime.today().strftime('%Y-%m-%d'))

with open('./crawler_outputs/{}-crawler_data.csv'.format(todaysdate), 'w') as csv_crawler:
    csv_output = csv.writer(csv_crawler)
    csv_output.writerow(['DOI','article_title','article_type','authors','date','downloads','views','tweets','data_collection_date'])

    for article in articles:
        articlehref = article.find_all("a", class_="fa fa-eye", href=True)
        for a in articlehref:
            article_prefix = str(a['href']).split('/')[2]
            article_id = str(a['href']).split('/')[3]
            print(article_prefix)
            print(article_id)
        doi = article_prefix + '/' + article_id
        article_title = article.find("h5").text.strip()
        print('Processing ' + str(article_title))
        article_type = (article.find("span", class_="main-color-text")).text.strip()
        authors = ' '.join(str((article.find("p", class_="article-author")).text).split())
        date = (article.find("p", class_="article-date")).text.strip()
        date = datetime.strptime(date,'%d %b %Y')
        date = date.strftime('%Y-%m-%d')
        print(date)
        newURL = base_URL +  article_prefix + '/' + article_id + '/'
        print(newURL)
        page = requests.get(newURL)
        soup2 = BeautifulSoup(page.content, "html.parser")
        stats = soup2.find("div", class_="article-stats")
        articlehref2 = stats.find_all("a")
        socmed =	{
            "Twitter": "0",
            "Downloads": "0",
            "Views": "0"}
        for stat in articlehref2:
            label = (stat.find('div', class_='stat-label')).text.strip()
            number = (stat.find('div', class_='stat-number')).text.strip()
            socmed[label] = number
        tweets = str(socmed.get('Twitter'))
        print(tweets)
        downloads = str(socmed.get('Downloads'))
        print(downloads)
        views = str(socmed.get('Views'))
        print(views)
        csv_output.writerow([doi,article_title,article_type,authors,date,downloads,views,tweets,todaysdate])