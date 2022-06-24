import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import pandas as pd

todaysdate = str(datetime.today().strftime('%Y-%m-%d'))
#todaysdate = '2022-06-04'

rdjdois = pd.read_csv('./curated_inputs/datasets_datapapers-links-rdj.csv')['DOI']

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

with open('./outputs/scraper_outputs/rdj/{}-scraper-datapapers-rdj.csv'.format(todaysdate), 'w') as csv_crawler:
    csv_output = csv.writer(csv_crawler)
    csv_output.writerow(['DOI','downloads','views','data_collection_date'])

    for rdjdoi in rdjdois:
        URL = 'https://doi.org/' + rdjdoi

        page = requests.get(URL,headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")

        results = soup.find("table", class_="metrics-table")
        allmetrics = results.find_all('tr')
        viewssection = allmetrics[2]
        downssection = allmetrics[3]
        views = viewssection.find('td').text
        print(views)
        articles = results.find_all("li", class_="article-block")
        downloads = downssection.find('td').text
        print(downloads)
        csv_output.writerow([rdjdoi,downloads,views,todaysdate])