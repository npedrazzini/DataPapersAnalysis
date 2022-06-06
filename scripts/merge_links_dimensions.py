import pandas as pd
from datetime import datetime

date = str(datetime.today().strftime('%Y-%m-%d'))
#date = '2022-04-04'
# Assumes that all file names start with timestamp in the format YYYY-MM-DD (today's date)
johdin = pd.read_csv('/Users/npedrazzini/Desktop/johd_crawler/manual_inputs/research_data_papers-links.csv')
dimensionscols = ["DOI","Times cited","Recent citations","FOR (ANZSRC) Categories","Altmetric"]
dimin = pd.read_csv('/Users/npedrazzini/Desktop/johd_crawler/dimensions_exports/research_papers/{}-dimensions_export-research_papers.csv'.format(date),usecols=dimensionscols)

johdout = johdin.merge(dimin,how='left')
johdout.to_csv('./final_outputs/research_papers/{}-johd_metrics.csv'.format(date),index=False)
