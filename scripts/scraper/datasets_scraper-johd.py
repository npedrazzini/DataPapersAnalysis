import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import re

todaysdate = str(datetime.today().strftime('%Y-%m-%d'))

datasets = './curated_inputs/datasets_datapapers-links-johd.csv'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

with open(datasets) as incsv, open('./outputs/scraper_outputs/johd/{}-scraper-datasets-johd.csv'.format(todaysdate),'w') as csv_crawler:
    datasetlist = csv.DictReader(incsv,delimiter=',')
    csv_output = csv.writer(csv_crawler)
    csv_output.writerow(['DOI','reponame','repourl','views','unique-views','downloads','unique-downloads','date'])
    for line in datasetlist:
        doi = line['DOI']
        reponame = line['reponame']
        repourl = line['repourl']
        date = line['pub-date']
        if reponame == 'Zenodo':
            page = requests.get(repourl,headers=headers)
            soup = BeautifulSoup(page.content, "html.parser")
            stats1 = soup.find("div", {'class': 'row stats-box'})
            stats2 = stats1.find("div", id="collapse-stats")
            results = stats2.find_all("td")
            for result in results:
                if result.text.strip() == 'Views':
                    totalviews = (result.parent.find_all('td'))[1].text
                    totalviews = ''.join(totalviews.split(','))
                    print(totalviews)
                elif result.text.strip() == 'Downloads':
                    totaldownloads = (result.parent.find_all('td'))[1].text
                    totaldownloads = ''.join(totaldownloads.split(','))
                    print(totaldownloads)
                elif result.text.strip() == 'Unique views':
                    uniqueviews = (result.parent.find_all('td'))[1].text
                    uniqueviews = ''.join(uniqueviews.split(','))
                    print(uniqueviews)
                elif result.text.strip() == 'Unique downloads':
                    uniquedown = (result.parent.find_all('td'))[1].text
                    uniquedown = ''.join(uniquedown.split(','))
                    print(uniquedown)
            csv_output.writerow([doi,reponame,repourl,totalviews,uniqueviews,totaldownloads,uniquedown,date])
        elif reponame == 'Figshare':
            try:
                print(repourl)
                repoid = repourl.split('/')[4].split('.')[2]
                print(repoid)
                viewspage = requests.get('https://stats.figshare.com/total/views/article/{}'.format(repoid),headers=headers)
                soup = BeautifulSoup(viewspage.content, "html.parser")
                totalviews = soup.text.split(':')[1].strip().split('}')[0]
                totalviews = ''.join(totalviews.split(','))
                print(totalviews)
                uniqueviews = 'NA'
                downpage = requests.get('https://stats.figshare.com/total/downloads/article/{}'.format(repoid),headers=headers)
                soup = BeautifulSoup(downpage.content, "html.parser")
                totaldownloads = soup.text.split(':')[1].strip().split('}')[0]
                totaldownloads = ''.join(totaldownloads.split(','))
                print(totaldownloads)
                uniquedown = 'NA'
                csv_output.writerow([doi,reponame,repourl,totalviews,uniqueviews,totaldownloads,uniquedown,date])
            except IndexError:
                totalviews = 'NA'
                uniqueviews = 'NA'
                totaldownloads = 'NA'
                uniquedown = 'NA'
                csv_output.writerow([doi,reponame,repourl,totalviews,uniqueviews,totaldownloads,uniquedown,date])
        elif reponame == 'Figshare-Inst':
            repoid = repourl.split('/')[6]
            print(repoid)
            instit = repourl.split('/')[2].split('.')[0]
            viewspage = requests.get('https://stats.figshare.com/{}/total/views/article/{}'.format(instit,repoid),headers=headers)
            soup = BeautifulSoup(viewspage.content, "html.parser")
            totalviews = soup.text.split(':')[1].strip().split('}')[0]
            totalviews = ''.join(totalviews.split(','))
            print(totalviews)
            uniqueviews = 'NA'
            downpage = requests.get('https://stats.figshare.com/{}/total/downloads/article/{}'.format(instit,repoid),headers=headers)
            soup = BeautifulSoup(downpage.content, "html.parser")
            totaldownloads = soup.text.split(':')[1].strip().split('}')[0]
            totaldownloads = ''.join(totaldownloads.split(','))
            print(totaldownloads)
            uniquedown = 'NA'
            csv_output.writerow([doi,reponame,repourl,totalviews,uniqueviews,totaldownloads,uniquedown,date])
        elif reponame == 'DataShare':
            page = requests.get(repourl + '/statistics',headers=headers)
            soup = BeautifulSoup(page.content, "html.parser")
            totalvisits = soup.find_all('h3')
            for h3 in totalvisits:
                if h3.text == 'Total Visits':
                    totalviews = h3.parent.find_all('td')[1].text
                    totalviews = ''.join(totalviews.split(','))
                    print(totalviews)
            uniqueviews = 'NA'
            totaldownloads = 'NA'
            uniquedown = 'NA'
            csv_output.writerow([doi,reponame,repourl,totalviews,uniqueviews,totaldownloads,uniquedown,date])
        elif reponame == 'Dataverse':
            page = requests.get(repourl,headers=headers)
            soup = BeautifulSoup(page.content, "html.parser")
            totalvisits = soup.find('div', id="metrics-body").text.strip()
            totalvisits = re.sub('\n', ' ', totalvisits)
            totalvisits = re.sub(' +', ' ', totalvisits)
            totalvisits = totalvisits.split(' ')
            print('Total visits: ' + str(totalvisits))
            if 'Views' in totalvisits:
                ind = totalvisits.index('Views')
                totalviews = totalvisits[ind-1]
                totalviews = ''.join(totalviews.split(','))
            else:
                totalviews = 'NA'
            print(totalviews)
            if 'Downloads' in totalvisits:
                ind = totalvisits.index('Downloads')
                totaldownloads = totalvisits[ind-1]
                totaldownloads = ''.join(totaldownloads.split(','))
            else:
                totaldownloads = 'NA'
            print(totaldownloads)
            uniqueviews = 'NA'
            uniquedown = 'NA'
            csv_output.writerow([doi,reponame,repourl,totalviews,uniqueviews,totaldownloads,uniquedown,date])
        else:
            totalviews = 'NA'
            uniqueviews = 'NA'
            totaldownloads = 'NA'
            uniquedown = 'NA'
            csv_output.writerow([doi,reponame,repourl,totalviews,uniqueviews,totaldownloads,uniquedown,date])
