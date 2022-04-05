import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

todaysdate = str(datetime.today().strftime('%Y-%m-%d'))

datasets = './manual_inputs/manual-datasets.csv'

with open(datasets) as incsv, open('./final_outputs/{}-datasets-metrics.csv'.format(todaysdate),'w') as csv_crawler:
    datasetlist = csv.DictReader(incsv,delimiter=',')
    csv_output = csv.writer(csv_crawler)
    csv_output.writerow(['DOI','repo-name','repourl','views','unique-views','downloads','unique-downloads'])
    for line in datasetlist:
        doi = line['DOI']
        reponame = line['repo']
        repourl = line['repo-url']
        if reponame == 'Zenodo':
            page = requests.get(repourl)
            soup = BeautifulSoup(page.content, "html.parser")
            stats1 = soup.find("div", {'class': 'row stats-box'})
            stats2 = stats1.find("div", id="collapse-stats")
            results = stats2.find_all("td")
            for result in results:
                if result.text.strip() == 'Views':
                    totalviews = (result.parent.find_all('td'))[1].text
                    print(totalviews)
                elif result.text.strip() == 'Downloads':
                    totaldownloads = (result.parent.find_all('td'))[1].text
                    print(totaldownloads)
                elif result.text.strip() == 'Unique views':
                    uniqueviews = (result.parent.find_all('td'))[1].text
                    print(uniqueviews)
                elif result.text.strip() == 'Unique downloads':
                    uniquedown = (result.parent.find_all('td'))[1].text
                    print(uniquedown)
            csv_output.writerow([doi,reponame,repourl,totalviews,uniqueviews,totaldownloads,uniquedown])
        elif reponame == 'Figshare':
            repoid = repourl.split('/')[4].split('.')[2]
            print(repoid)
            viewspage = requests.get('https://stats.figshare.com/total/views/article/{}'.format(repoid))
            soup = BeautifulSoup(viewspage.content, "html.parser")
            totalviews = soup.text.split(':')[1].strip().split('}')[0]
            print(totalviews)
            uniqueviews = 'NA'
            downpage = requests.get('https://stats.figshare.com/total/downloads/article/{}'.format(repoid))
            soup = BeautifulSoup(downpage.content, "html.parser")
            totaldownloads = soup.text.split(':')[1].strip().split('}')[0]
            print(totaldownloads)
            uniquedown = 'NA'
            csv_output.writerow([doi,reponame,repourl,totalviews,uniqueviews,totaldownloads,uniquedown])
        elif reponame == 'Figshare-Inst':
            repoid = repourl.split('/')[6]
            print(repoid)
            instit = repourl.split('/')[2].split('.')[0]
            viewspage = requests.get('https://stats.figshare.com/{}/total/views/article/{}'.format(instit,repoid))
            soup = BeautifulSoup(viewspage.content, "html.parser")
            totalviews = soup.text.split(':')[1].strip().split('}')[0]
            print(totalviews)
            uniqueviews = 'NA'
            downpage = requests.get('https://stats.figshare.com/{}/total/downloads/article/{}'.format(instit,repoid))
            soup = BeautifulSoup(downpage.content, "html.parser")
            totaldownloads = soup.text.split(':')[1].strip().split('}')[0]
            print(totaldownloads)
            uniquedown = 'NA'
            csv_output.writerow([doi,reponame,repourl,totalviews,uniqueviews,totaldownloads,uniquedown])
        elif reponame == 'DataShare':
            page = requests.get(repourl + '/statistics')
            soup = BeautifulSoup(page.content, "html.parser")
            totalvisits = soup.find_all('h3')
            for h3 in totalvisits:
                if h3.text == 'Total Visits':
                    totalviews = h3.parent.find_all('td')[1].text
                    print(totalviews)
            uniqueviews = 'NA'
            totaldownloads = 'NA'
            uniquedown = 'NA'
            csv_output.writerow([doi,reponame,repourl,totalviews,uniqueviews,totaldownloads,uniquedown])
        elif reponame == 'Dataverse':
            page = requests.get(repourl)
            soup = BeautifulSoup(page.content, "html.parser")
            totalvisits = soup.find_all('div', id="metrics-heading")
            for div in totalvisits:
                if div.text.strip() == 'Dataset Metrics':
                    totalviews = div.parent.find('div', {'class': 'metrics-count-block'}).text.strip().split(' ')[0]
                    print(totalviews)
            uniqueviews = 'NA'
            totaldownloads = 'NA'
            uniquedown = 'NA'
            csv_output.writerow([doi,reponame,repourl,totalviews,uniqueviews,totaldownloads,uniquedown])
        else:
            totalviews = 'NA'
            uniqueviews = 'NA'
            totaldownloads = 'NA'
            uniquedown = 'NA'
            csv_output.writerow([doi,reponame,repourl,totalviews,uniqueviews,totaldownloads,uniquedown])
