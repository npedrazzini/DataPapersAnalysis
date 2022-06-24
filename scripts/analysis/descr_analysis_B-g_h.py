# Differences in publication dates: 
# a. how long after depositing a dataset is a data paper published?
# b. which one are published first, data papers or research papers?

import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import functools as ft
import statistics

dateoflastdf = '2022-06-04' # change to date of last export

researchfile = pd.read_csv('./outputs/final_outputs/research_papers/{}-final-research_papers-johd.csv'.format(dateoflastdf),
                            usecols=["DOI",
                                    "Publication Date (online)"])
datasetfile = pd.read_csv('./outputs/final_outputs/johd/{}-final-datasets-johd.csv'.format(dateoflastdf),
                            usecols=["DOI",
                                    "date"])
datapaperfile = pd.read_csv('./outputs/final_outputs/johd/{}-final-datasets-johd.csv'.format(dateoflastdf),
                            usecols=["DOI",
                                    "date"])
rdjfile = pd.read_csv('./outputs/final_outputs/rdj/{}-final-datapapers-rdj.csv'.format(dateoflastdf),
                            usecols=["DOI",
                                    "date",
                                    "Publication Date (online)"])
researchfile_rdj = pd.read_csv('./outputs/final_outputs/research_papers/{}-final-research_papers-rdj.csv'.format(dateoflastdf),
                            usecols=["DOI",
                                    "Publication Date (online)"])

researchfile = researchfile.rename(columns={"Publication Date (online)": "date_research"})
datasetfile = datasetfile.rename(columns={"date": "date_dataset"})
datapaperfile = datapaperfile.rename(columns={"date": "date_datapaper"})
rdjdf = rdjfile.rename(columns={"date": "date_dataset_rdj","Publication Date (online)": "date_datapaper_rdj"})
researchfile_rdj = researchfile_rdj.rename(columns={"Publication Date (online)": "date_research_rdj"})

date_format = "%Y-%m-%d"

dfs = [researchfile,datasetfile,datapaperfile]

df = ft.reduce(lambda left, right: pd.merge(left, right, on='DOI'), dfs)

df = df[df['date_dataset'].notna()]
df = df[df['date_datapaper'].notna()]

df['date_dataset'] = [datetime.strptime(str(x), date_format) for x in df['date_dataset']]
df['date_datapaper'] = [datetime.strptime(str(x), date_format) for x in df['date_datapaper']]
# df['date_research'] = [datetime.strptime(str(x), date_format) for x in df['date_research']]

df['diff_dataset_datapaper'] = df['date_datapaper'] - df['date_dataset']
df['diff_dataset_datapaper'] = [x.days for x in df['diff_dataset_datapaper']]

# Difference in days between publication date of dataset and publication date of data paper

# bins = [1,7,30,60,90,120,150,180,max(df['diff_dataset_datapaper'])]

plt.hist(df['diff_dataset_datapaper'],bins=len(df['diff_dataset_datapaper']),color='c',edgecolor='k')
m = statistics.mean(df['diff_dataset_datapaper'])
sd = statistics.stdev(df['diff_dataset_datapaper'])
plt.axvline(m,color='k',linestyle='dashed')
plt.axvline(m + sd,color='y',linestyle='dashed')
plt.axvline(m - sd,color='y',linestyle='dashed')
plt.axvline(m + sd*2,color='y',linestyle='dashed')
plt.axvline(m - sd*2,color='y',linestyle='dashed')

plt.title('JOHD: Days between dataset and datapaper publication')
plt.xlabel('Days (Mean: {})'.format(m))
plt.ylabel('Counts')
plt.grid(axis='y', alpha=0.75)

plt.show()


# Difference in days between publication date of research paper and publication date of data paper

# bins = [1,7,30,60,90,120,150,180,max(df['diff_dataset_datapaper'])]

df = df[df['date_research'].notna()]
df['date_research'] = [datetime.strptime(str(x), date_format) for x in df['date_research']]
df['diff_research_datapaper'] = df['date_research'] - df['date_dataset']
df['diff_research_datapaper'] = [x.days for x in df['diff_research_datapaper']]

plt.hist(df['diff_research_datapaper'],bins=len(df['diff_research_datapaper']),color='c',edgecolor='k')
m = statistics.mean(df['diff_research_datapaper'])
sd = statistics.stdev(df['diff_research_datapaper'])
plt.axvline(m,color='k',linestyle='dashed')
plt.axvline(m + sd,color='y',linestyle='dashed')
plt.axvline(m - sd,color='y',linestyle='dashed')
plt.axvline(m + sd*2,color='y',linestyle='dashed')
plt.axvline(m - sd*2,color='y',linestyle='dashed')

plt.title('JOHD: Days between research paper and data paper publication')
plt.xlabel('Days (Mean: {})'.format(m))
plt.ylabel('Counts')
plt.grid(axis='y', alpha=0.75)

plt.show()


#RDJ

rdjdf = rdjdf[rdjdf['date_datapaper_rdj'].notna()]
rdjdf = rdjdf[rdjdf['date_dataset_rdj'].notna()]

rdjdf['date_datapaper_rdj'] = [datetime.strptime(str(x), date_format) for x in rdjdf['date_datapaper_rdj']]
rdjdf['date_dataset_rdj'] = [datetime.strptime(str(x), date_format) for x in rdjdf['date_dataset_rdj']]

rdjdf['diff_dataset_datapaper'] = rdjdf['date_datapaper_rdj'] - rdjdf['date_dataset_rdj']
rdjdf['diff_dataset_datapaper'] = [x.days for x in rdjdf['diff_dataset_datapaper']]

plt.hist(rdjdf['diff_dataset_datapaper'],bins=len(rdjdf['diff_dataset_datapaper']),color='c',edgecolor='k')
m = statistics.mean(rdjdf['diff_dataset_datapaper'])
sd = statistics.stdev(rdjdf['diff_dataset_datapaper'])
plt.axvline(m,color='k',linestyle='dashed')
plt.axvline(m + sd,color='y',linestyle='dashed')
plt.axvline(m - sd,color='y',linestyle='dashed')
plt.axvline(m + sd*2,color='y',linestyle='dashed')
plt.axvline(m - sd*2,color='y',linestyle='dashed')

plt.title('RDJ: Days between data paper and dataset publication')
plt.xlabel('Days (Mean: {})'.format(m))
plt.ylabel('Counts')
plt.grid(axis='y', alpha=0.75)

plt.show()

## RDJ research

dfs_rdj = [rdjdf,researchfile_rdj]

df_rdj = ft.reduce(lambda left, right: pd.merge(left, right, on='DOI'), dfs_rdj)

df_rdj = df_rdj[df_rdj['date_research_rdj'].notna()]
df_rdj['date_research_rdj'] = [datetime.strptime(str(x), date_format) for x in df_rdj['date_research_rdj']]
df_rdj['diff_research_datapaper'] = df_rdj['date_research_rdj'] - df_rdj['date_datapaper_rdj']
df_rdj['diff_research_datapaper'] = [x.days for x in df_rdj['diff_research_datapaper']]

plt.hist(df_rdj['diff_research_datapaper'],bins=len(df_rdj['diff_research_datapaper']),color='c',edgecolor='k')
m = statistics.mean(df_rdj['diff_research_datapaper'])
sd = statistics.stdev(df_rdj['diff_research_datapaper'])
plt.axvline(m,color='k',linestyle='dashed')
plt.axvline(m + sd,color='y',linestyle='dashed')
plt.axvline(m - sd,color='y',linestyle='dashed')
plt.axvline(m + sd*2,color='y',linestyle='dashed')
plt.axvline(m - sd*2,color='y',linestyle='dashed')

plt.title('RDJ: Days between research paper and data paper publication')
plt.xlabel('Days (Mean: {})'.format(m))
plt.ylabel('Counts')
plt.grid(axis='y', alpha=0.75)

plt.show()

#RDJ + JOHD
#research + datapaper
johdplusrdj = list(df['diff_research_datapaper']) + list(df_rdj['diff_research_datapaper'])

plt.hist(johdplusrdj,bins=len(johdplusrdj),color='c',edgecolor='k')
m = statistics.mean(johdplusrdj)
sd = statistics.stdev(johdplusrdj)
plt.axvline(m,color='k',linestyle='dashed')
plt.axvline(m + sd,color='y',linestyle='dashed')
plt.axvline(m - sd,color='y',linestyle='dashed')
plt.axvline(m + sd*2,color='y',linestyle='dashed')
plt.axvline(m - sd*2,color='y',linestyle='dashed')

plt.title('RDJ + JOHD: Days between research paper and data paper publication')
plt.xlabel('Days (Mean: {})'.format(m))
plt.ylabel('Counts')
plt.grid(axis='y', alpha=0.75)

plt.show()

#datapepers + datasets

johdplusrdj = list(df['diff_dataset_datapaper']) + list(rdjdf['diff_dataset_datapaper'])

plt.hist(johdplusrdj,bins=len(johdplusrdj),color='c',edgecolor='k')
m = statistics.mean(johdplusrdj)
sd = statistics.stdev(johdplusrdj)
plt.axvline(m,color='k',linestyle='dashed')
plt.axvline(m + sd,color='y',linestyle='dashed')
plt.axvline(m - sd,color='y',linestyle='dashed')
plt.axvline(m + sd*2,color='y',linestyle='dashed')
plt.axvline(m - sd*2,color='y',linestyle='dashed')

plt.title('RDJ + JOHD: Days between data paper and dataset publication')
plt.xlabel('Days (Mean: {})'.format(m))
plt.ylabel('Counts')
plt.grid(axis='y', alpha=0.75)

plt.show()