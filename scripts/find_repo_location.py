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
datasets = []

with open('./crawler_outputs/{}-repositories.csv'.format(todaysdate), 'w') as csv_crawler:
    csv_output = csv.writer(csv_crawler)
    csv_output.writerow(['DOI','repo'])

    for article in articles:
        articlehref = article.find_all("a", class_="fa fa-eye", href=True)
        for a in articlehref:
            article_prefix = str(a['href']).split('/')[2]
            article_id = str(a['href']).split('/')[3]
        doi = article_prefix + '/' + article_id
        article_title = article.find("h5").text.strip()
        print('Processing ' + str(article_title))
        article_type = (article.find("span", class_="main-color-text")).text.strip()
        authors = ' '.join(str((article.find("p", class_="article-author")).text).split())
        date = (article.find("p", class_="article-date")).text.strip()
        date = datetime.strptime(date,'%d %b %Y')
        date = date.strftime('%Y-%m-%d')
        newURL = base_URL +  article_prefix + '/' + article_id + '/'
        page = requests.get(newURL)
        soup2 = BeautifulSoup(page.content, "html.parser")
        if article_type == 'Data Papers':
            results = soup2.findAll("h3")
            count = 0
            for result in results:
                if result.text == 'Repository location':
                    if result.parent.find('a',href=True) is not None:
                        print(result)
                        count += 1
                        csv_output.writerow([doi, (result.parent.find('a',href=True).text)])
                if result.text == 'Repository name' and count < 1:
                    if result.parent.find('a',href=True) is not None:
                        csv_output.writerow([doi, (result.parent.find('a',href=True).text)])
        else:
            csv_output.writerow([doi,'NA'])