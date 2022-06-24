import pandas as pd
from datetime import datetime

date = str(datetime.today().strftime('%Y-%m-%d'))
# date = '2022-06-04'
# Assumes that all file names start with timestamp in the format YYYY-MM-DD (today's date)
rdjin1 = pd.read_csv('./curated_inputs/datasets_datapapers-links-rdj.csv')
rdjin2 = pd.read_csv('./outputs/scraper_outputs/rdj/{}-scraper-datapapers-rdj.csv'.format(date))

rdjout1 = rdjin1.merge(rdjin2,how='left')

dimensionscols = ["DOI","Publication Date (online)","Times cited","Recent citations","FOR (ANZSRC) Categories","Altmetric"]
dimin = pd.read_csv('./dimensions_exports/johd_rdj/{}-dimensions_export.csv'.format(date),usecols=dimensionscols)

rdjout2 = rdjout1.merge(dimin,how='left')

rdjout2.to_csv('./outputs/final_outputs/rdj/{}-final-datapapers-rdj.csv'.format(date),index=False)
