import pandas as pd
from datetime import datetime

date = str(datetime.today().strftime('%Y-%m-%d'))
#date = '2022-04-04'

# Assumes that all file names start with timestamp in the format YYYY-MM-DD (today's date)
johdin = pd.read_csv('./outputs/scraper_outputs/johd/{}-scraper-datapapers-johd.csv'.format(date))
dimensionscols = ["DOI","Times cited","Recent citations","FOR (ANZSRC) Categories","Altmetric"]
dimin = pd.read_csv('./dimensions_exports/johd_rdj/{}-dimensions_export.csv'.format(date),usecols=dimensionscols)

johdout = johdin.merge(dimin,how='left')

johdout.to_csv('./outputs/final_outputs/johd/{}-final-datapapers-johd.csv'.format(date),index=False)
