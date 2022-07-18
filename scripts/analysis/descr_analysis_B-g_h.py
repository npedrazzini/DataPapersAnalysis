# Differences in publication dates: 
# a. how long after depositing a dataset is a data paper published?
# b. which one are published first, data papers or research papers?

import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import functools as ft
import statistics
from scipy import stats

dateoflastdf = '2022-07-04' # change to date of last export


datapaperfile = pd.read_csv('./outputs/final_outputs/johd/{}-final-datapapers-johd.csv'.format(dateoflastdf),
                            usecols=["DOI",
                                    "date"])
datasetfile = pd.read_csv('./outputs/final_outputs/johd/{}-final-datasets-johd.csv'.format(dateoflastdf),
                            usecols=["DOI",
                                    "date"])
researchfile = pd.read_csv('./outputs/final_outputs/research_papers/{}-final-research_papers-johd.csv'.format(dateoflastdf),
                            usecols=["DOI",
                                    "Publication Date (online)"])
rdjfile = pd.read_csv('./outputs/final_outputs/rdj/{}-final-datapapers-rdj.csv'.format(dateoflastdf),
                            usecols=["DOI",
                                    "date"])
rdjdatasetfile = pd.read_csv('./outputs/final_outputs/rdj/{}-final-datasets-rdj.csv'.format(dateoflastdf),
                            usecols=["DOI",
                                    "date",
                                    "views",
                                    "unique-views",
                                    "downloads",
                                    "unique-downloads"])
researchfile_rdj = pd.read_csv('./outputs/final_outputs/research_papers/{}-final-research_papers-rdj.csv'.format(dateoflastdf),
                            usecols=["DOI",
                                    "Publication Date (online)"])

#Rename relevant columns for ease
datapaperfile = datapaperfile.rename(columns={"date": "date_datapaper"})
datasetfile = datasetfile.rename(columns={"date": "date_dataset"})
researchfile = researchfile.rename(columns={"Publication Date (online)": "date_research"})
rdjfile = rdjfile.rename(columns={"date": "date_datapaper"})
rdjdatasetfile = rdjdatasetfile.rename(columns={"date": "date_dataset"})
researchfile_rdj = researchfile_rdj.rename(columns={"Publication Date (online)": "date_research"})

#Define date format
date_format = "%Y-%m-%d"

#Merge relevant dfs, remove NAs, calculate diff in days
datasetsdfs = pd.concat([datasetfile,rdjdatasetfile])
datasetsdfs.to_csv('datasetsdfs.csv')
datapaperdfs = pd.concat([datapaperfile,rdjfile])
datapaperdfs.to_csv('datapaperdfs.csv')
print(len(datasetsdfs))
print(len(datapaperdfs))
datapapers_datasets_dfs = [datasetsdfs,datapaperdfs]
datapapers_datasets_df = ft.reduce(lambda left, right: pd.merge(left, right, on='DOI'), datapapers_datasets_dfs)
datapapers_datasets_df.to_csv('datapapers_datasets_df.csv')
print(len(datapapers_datasets_df))
datapapers_datasets_df = datapapers_datasets_df[datapapers_datasets_df['date_dataset'].notna()]
datapapers_datasets_df = datapapers_datasets_df[datapapers_datasets_df['date_datapaper'].notna()]
print(len(datapapers_datasets_df))
datapapers_datasets_df['date_dataset'] = [datetime.strptime(str(x), date_format) for x in datapapers_datasets_df['date_dataset']]
datapapers_datasets_df['date_datapaper'] = [datetime.strptime(str(x), date_format) for x in datapapers_datasets_df['date_datapaper']]
datapapers_datasets_df['diff_dataset_datapaper'] = datapapers_datasets_df['date_datapaper'] - datapapers_datasets_df['date_dataset']
datapapers_datasets_df['diff_dataset_datapaper'] = [x.days for x in datapapers_datasets_df['diff_dataset_datapaper']]

#Merge relevant dfs, remove NAs, calculate diff in days
researchdfs = pd.concat([researchfile,researchfile_rdj])
datapaperdfs = pd.concat([datapaperfile,rdjfile])
datapapers_research_dfs = [researchdfs,datapaperdfs]
datapapers_research_df =  ft.reduce(lambda left, right: pd.merge(left, right, on='DOI'), datapapers_research_dfs)
datapapers_research_df = datapapers_research_df[datapapers_research_df['date_research'].notna()]
datapapers_research_df = datapapers_research_df[datapapers_research_df['date_datapaper'].notna()]
datapapers_research_df['date_research'] = [datetime.strptime(str(x), date_format) for x in datapapers_research_df['date_research']]
datapapers_research_df['date_datapaper'] = [datetime.strptime(str(x), date_format) for x in datapapers_research_df['date_datapaper']]
datapapers_research_df['diff_research_datapaper'] = datapapers_research_df['date_datapaper'] - datapapers_research_df['date_research']
datapapers_research_df['diff_research_datapaper'] = [x.days for x in datapapers_research_df['diff_research_datapaper']]

# Difference in days between publication date of dataset and publication date of data paper
# bins = [1,7,30,60,90,120,150,180,max(df['diff_dataset_datapaper'])]
dp_ds = list(datapapers_datasets_df['diff_dataset_datapaper'])
plt.hist(dp_ds,bins=len(dp_ds),color='c',edgecolor='k')
m = statistics.median(dp_ds)
sd = stats.median_abs_deviation(dp_ds)
plt.axvline(m,color='k',linestyle='dashed')
plt.text(m, 13.1, 'M', rotation = 90)
plt.axvline(m + sd,color='y',linestyle='dashed')
plt.text(m + sd, 12.8, '1MAD', rotation = 90)
plt.axvline(m - sd,color='y',linestyle='dashed')
plt.text(m - sd, 12.8, '-1MAD', rotation = 90)
plt.axvline(m + sd*2,color='y',linestyle='dashed')
plt.text(m + sd*2, 12.8, '2MAD', rotation = 90)
plt.axvline(m - sd*2,color='y',linestyle='dashed')
plt.text(m - sd*2, 12.8, '-2MAD', rotation = 90)

# plt.title('RDJ + JOHD: Days between data paper and dataset publication')
plt.xlabel('Days before (-n) or after (n) dataset publication (M: {}, MAD: {})'.format("%.0f" % m,"%.0f" % sd))
plt.ylabel('n data papers')
plt.grid(axis='y', alpha=0.75)
plt.ylim((0,15))
plt.savefig("./outputs/figures/figure6-diff-ds-dp.jpeg",dpi=300)
plt.show()



# Difference in days between publication date of research paper and publication date of data paper
# bins = [1,7,30,60,90,120,150,180,max(df['diff_dataset_datapaper'])]
dp_rp = list(datapapers_research_df['diff_research_datapaper'])
plt.hist(dp_rp,bins=len(dp_rp),color='c',edgecolor='k')
m = statistics.median(dp_rp)
sd = stats.median_abs_deviation(dp_rp)
plt.axvline(m,color='k',linestyle='dashed')
plt.text(m, 5.7, 'M', rotation = 90)
plt.axvline(m + sd,color='y',linestyle='dashed')
plt.text(m + sd, 5.4, '1MAD', rotation = 90)
plt.axvline(m - sd,color='y',linestyle='dashed')
plt.text(m - sd, 5.4, '-1MAD', rotation = 90)
plt.axvline(m + sd*2,color='y',linestyle='dashed')
plt.text(m + sd*2, 5.4, '2MAD', rotation = 90)
plt.axvline(m - sd*2,color='y',linestyle='dashed')
plt.text(m - sd*2, 5.4, '-2MAD', rotation = 90)

# plt.title('RDJ + JOHD: Days between data paper and dataset publication')
plt.xlabel('Days before (-n) or after (n) research paper publication (M: {}, MAD: {})'.format("%.0f" % m,"%.0f" % sd))
plt.ylabel('n of data papers')
plt.grid(axis='y', alpha=0.75)
plt.ylim((0,7))
plt.savefig("./outputs/figures/figure7-diff-rp-dp.jpeg",dpi=300)
plt.show()