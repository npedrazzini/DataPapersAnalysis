import pandas as pd
from datetime import datetime

date = str(datetime.today().strftime('%Y-%m-%d'))
# date = '2022-06-04'
# Assumes that all file names start with timestamp in the format YYYY-MM-DD (today's date)
johdin = pd.read_csv('./curated_inputs/research_datapapers-links-johd.csv')
dimensionscols = ["DOI","Publication Date (online)","Times cited","Recent citations","FOR (ANZSRC) Categories","Altmetric"]
dimin = pd.read_csv('./dimensions_exports/research_papers/{}-dimensions_export-research_papers-johd.csv'.format(date),usecols=dimensionscols)

johdout = johdin.merge(dimin,how='left')
johdout.to_csv('./outputs/final_outputs/research_papers/{}-research_papers-final-johd.csv'.format(date),index=False)


rdjin = pd.read_csv('./curated_inputs/research_datapapers-links-rdj.csv')
dimensionscols = ["DOI","Publication Date (online)","Times cited","Recent citations","FOR (ANZSRC) Categories","Altmetric"]
dimin = pd.read_csv('./dimensions_exports/research_papers/{}-dimensions_export-research_papers-rdj.csv'.format(date),usecols=dimensionscols)

rdjout = rdjin.merge(dimin,how='left')
rdjout.to_csv('./outputs/final_outputs/research_papers/{}-research_papers-final-rdj.csv'.format(date),index=False)
