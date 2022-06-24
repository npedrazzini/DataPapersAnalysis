# Overall changes in metrics growth/decrease rates over time
# Not reliable, too little data: use bigger datasets to show that metrics tend to decrease with time hence the need for normalization!

import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import functools as ft
import numpy as np

dateoflastdf = '2022-06-04' # change to date of last export

researchfile = pd.read_csv('./outputs/final_outputs/research_papers/{}-final-research_papers-johd.csv'.format(dateoflastdf),
                            usecols=["DOI",
                                    "Times cited",
                                    "Recent citations",
                                    "Altmetric",
                                    "Publication Date (online)"])
datasetfile = pd.read_csv('./outputs/final_outputs/johd/{}-final-datasets-johd.csv'.format(dateoflastdf),
                            usecols=["DOI",
                                    "date",
                                    "views",
                                    "unique-views",
                                    "downloads",
                                    "unique-downloads"])
datapaperfile = pd.read_csv('./outputs/final_outputs/johd/{}-final-datapapers-johd.csv'.format(dateoflastdf),
                            usecols=["DOI",
                                    "date",
                                    "downloads",
                                    "views",
                                    "tweets",
                                    "data_collection_date",
                                    "Times cited",
                                    "Recent citations",
                                    "Altmetric"])
rdjfile = pd.read_csv('./outputs/final_outputs/rdj/{}-final-datapapers-rdj.csv'.format(dateoflastdf),
                            usecols=["DOI",
                                    "Publication Date (online)",
                                    "downloads",
                                    "views",
                                    "data_collection_date",
                                    "Times cited",
                                    "Recent citations",
                                    "Altmetric"]) 
researchfile_rdj = pd.read_csv('./outputs/final_outputs/research_papers/{}-final-research_papers-rdj.csv'.format(dateoflastdf),
                            usecols=["DOI",
                                    "Publication Date (online)",
                                    "Times cited",
                                    "Recent citations",
                                    "Altmetric",
                                    "Publication Date (online)"])

researchfile = researchfile.rename(columns={"Publication Date (online)": "date", "Times cited": "tot_citations","Recent citations": "rec_citations", "Altmetric": "altmetric"})
datasetfile = datasetfile.rename(columns={"date": "date","views": "views","unique-views": "unique-views", "downloads": "downloads", "unique-downloads": "unique-downloads"})
datapaperfile = datapaperfile.rename(columns={"date": "date","views": "views", "downloads": "downloads","tweets": "tweets", "Times cited": "tot_citations","Recent citations": "rec_citations", "Altmetric": "altmetric"})
rdjfile = rdjfile.rename(columns={"Publication Date (online)": "date","downloads": "downloads", "views": "views","Times cited": "tot_citations","Recent citations": "rec_citations", "Altmetric": "altmetric"})
researchfile_rdj = researchfile_rdj.rename(columns={"Publication Date (online)": "date","Times cited": "tot_citations","Recent citations": "rec_citations", "Altmetric": "altmetric"})


date_format = "%Y-%m-%d"

data_collection_date = dateoflastdf

#REMOVE OUTLIERS
# Uncomment if you want to remove outliers

# q1, q3= np.percentile(sorted(researchfile['tot_citations']),[25,75])
# iqr = q3 - q1
# lower_bound = q1 -(1.5 * iqr) 
# upper_bound = q3 +(1.5 * iqr)
# researchfile  = researchfile.loc[(researchfile['tot_citations'] <= upper_bound) & (researchfile['tot_citations'] >= lower_bound)] 

# q1, q3= np.percentile(sorted(researchfile['altmetric']),[25,75])
# iqr = q3 - q1
# lower_bound = q1 -(1.5 * iqr) 
# upper_bound = q3 +(1.5 * iqr)
# researchfile  = researchfile.loc[(researchfile['altmetric'] <= upper_bound) & (researchfile['altmetric'] >= lower_bound)] 

# q1, q3= np.percentile(sorted(researchfile_rdj['tot_citations']),[25,75])
# iqr = q3 - q1
# lower_bound = q1 -(1.5 * iqr) 
# upper_bound = q3 +(1.5 * iqr)
# researchfile_rdj  = researchfile_rdj.loc[(researchfile_rdj['tot_citations'] <= upper_bound) & (researchfile_rdj['tot_citations'] >= lower_bound)] 

# q1, q3= np.percentile(sorted(researchfile_rdj['altmetric']),[25,75])
# iqr = q3 - q1
# lower_bound = q1 -(1.5 * iqr) 
# upper_bound = q3 +(1.5 * iqr)
# researchfile_rdj  = researchfile_rdj.loc[(researchfile_rdj['altmetric'] <= upper_bound) & (researchfile_rdj['altmetric'] >= lower_bound)] 

# q1, q3= np.percentile(sorted(rdjfile['tot_citations']),[25,75])
# iqr = q3 - q1
# lower_bound = q1 -(1.5 * iqr) 
# upper_bound = q3 +(1.5 * iqr)
# rdjfile  = rdjfile.loc[(rdjfile['tot_citations'] <= upper_bound) & (rdjfile['tot_citations'] >= lower_bound)] 

# q1, q3= np.percentile(sorted(rdjfile['altmetric']),[25,75])
# iqr = q3 - q1
# lower_bound = q1 -(1.5 * iqr) 
# upper_bound = q3 +(1.5 * iqr)
# rdjfile  = rdjfile.loc[(rdjfile['altmetric'] <= upper_bound) & (rdjfile['altmetric'] >= lower_bound)] 

# q1, q3= np.percentile(sorted(rdjfile['views']),[25,75])
# iqr = q3 - q1
# lower_bound = q1 -(1.5 * iqr) 
# upper_bound = q3 +(1.5 * iqr)
# rdjfile  = rdjfile.loc[(rdjfile['views'] <= upper_bound) & (rdjfile['views'] >= lower_bound)] 

# q1, q3= np.percentile(sorted(rdjfile['downloads']),[25,75])
# iqr = q3 - q1
# lower_bound = q1 -(1.5 * iqr) 
# upper_bound = q3 +(1.5 * iqr)
# rdjfile  = rdjfile.loc[(rdjfile['downloads'] <= upper_bound) & (rdjfile['downloads'] >= lower_bound)] 

# q1, q3= np.percentile(sorted(datasetfile['downloads']),[25,75])
# iqr = q3 - q1
# lower_bound = q1 -(1.5 * iqr) 
# upper_bound = q3 +(1.5 * iqr)
# datasetfile  = datasetfile.loc[(datasetfile['downloads'] <= upper_bound) & (datasetfile['downloads'] >= lower_bound)] 

# q1, q3= np.percentile(sorted(datasetfile['views']),[25,75])
# iqr = q3 - q1
# lower_bound = q1 -(1.5 * iqr) 
# upper_bound = q3 +(1.5 * iqr)
# datasetfile  = datasetfile.loc[(datasetfile['views'] <= upper_bound) & (datasetfile['views'] >= lower_bound)] 

# q1, q3= np.percentile(sorted(datapaperfile['tot_citations']),[25,75])
# iqr = q3 - q1
# lower_bound = q1 -(1.5 * iqr) 
# upper_bound = q3 +(1.5 * iqr)
# datapaperfile  = datapaperfile.loc[(datapaperfile['tot_citations'] <= upper_bound) & (datapaperfile['tot_citations'] >= lower_bound)] 

# q1, q3= np.percentile(sorted(datapaperfile['altmetric']),[25,75])
# iqr = q3 - q1
# lower_bound = q1 -(1.5 * iqr) 
# upper_bound = q3 +(1.5 * iqr)
# datapaperfile  = datapaperfile.loc[(datapaperfile['altmetric'] <= upper_bound) & (datapaperfile['altmetric'] >= lower_bound)] 

# q1, q3= np.percentile(sorted(datapaperfile['views']),[25,75])
# iqr = q3 - q1
# lower_bound = q1 -(1.5 * iqr) 
# upper_bound = q3 +(1.5 * iqr)
# datapaperfile  = datapaperfile.loc[(datapaperfile['views'] <= upper_bound) & (datapaperfile['views'] >= lower_bound)] 

# q1, q3= np.percentile(sorted(datapaperfile['downloads']),[25,75])
# iqr = q3 - q1
# lower_bound = q1 -(1.5 * iqr) 
# upper_bound = q3 +(1.5 * iqr)
# datapaperfile  = datapaperfile.loc[(datapaperfile['downloads'] <= upper_bound) & (datapaperfile['downloads'] >= lower_bound)] 


#DATASETS
datasetfile = datasetfile[datasetfile['date'].notna()]
datasetfile['date'] = [datetime.strptime(str(x), date_format) for x in datasetfile['date']]
data_collection_date= datetime.strptime(data_collection_date, date_format)
datasetfile['days_since_publication'] = (data_collection_date - datasetfile['date'])
datasetfile['days_since_publication'] = [x.days for x in datasetfile['days_since_publication']]
datasetfile['downloads'] = datasetfile['downloads']/datasetfile['days_since_publication']
datasetfile['views'] = datasetfile['views']/datasetfile['days_since_publication']

# Create dataframe with daily averages and remove outliers
days_since_publication = datasetfile['days_since_publication'].unique()
views = []
downloads = []
for day in days_since_publication:
    mean_views = datasetfile['views'][datasetfile['days_since_publication'] == day].mean()
    mean_downloads = datasetfile['downloads'][datasetfile['days_since_publication'] == day].mean()
    views.append(mean_views)
    downloads.append(mean_downloads)
df_means = pd.DataFrame({'days_since_publication': days_since_publication, \
    'mean_views': views, 'mean_downloads': downloads})

# Create dataframe with 90-day averages
interval = 90           # Set the length of the interval period in days
max_days = df_means['days_since_publication'].max()
periods = np.array(range(1,(round(max_days/interval)+2)))*interval
p_views = []
p_downloads = []
df_p = df_means         # Create a copy that we could work with

for period in periods:
    mean_p_views = df_p['mean_views'][df_p['days_since_publication'] <= period].mean()
    mean_p_downloads = df_p['mean_downloads'][df_p['days_since_publication'] <= period].mean()
    indices = df_p.index[df_p['days_since_publication'] <= period].tolist()
    p_views.append(mean_p_views)
    p_downloads.append(mean_p_downloads)
    df_p = df_p.drop(indices)
df_means_period_dataset = pd.DataFrame({'less_than_n_days_since_publication': periods, \
    'monthly_mean_views': p_views, 'monthly_mean_downloads': p_downloads})
df_means_period_dataset = df_means_period_dataset.sort_values(by='less_than_n_days_since_publication', ascending=False)

# Reducing to years to be consistent with the other plots
df_means_period_dataset['less_than_n_days_since_publication'] = [x/365 for x in df_means_period_dataset['less_than_n_days_since_publication']]


#DATAPAPERs_JOHD
datapaperfile = datapaperfile[datapaperfile['date'].notna()]
datapaperfile['date'] = [datetime.strptime(str(x), date_format) for x in datapaperfile['date']]
datapaperfile['data_collection_date'] = [datetime.strptime(x, date_format) for x in datapaperfile['data_collection_date']]
datapaperfile['days_since_publication'] = (datapaperfile['data_collection_date'] - datapaperfile['date'])
datapaperfile['days_since_publication'] = [x.days for x in datapaperfile['days_since_publication']]
datapaperfile['downloads'] = datapaperfile['downloads']/datapaperfile['days_since_publication']
datapaperfile['views'] = datapaperfile['views']/datapaperfile['days_since_publication']
datapaperfile['tweets'] = datapaperfile['tweets']/datapaperfile['days_since_publication']
datapaperfile['tot_citations'] = datapaperfile['tot_citations']/datapaperfile['days_since_publication']
datapaperfile['altmetric'] = datapaperfile['altmetric']/datapaperfile['days_since_publication']

# Create dataframe with daily averages and remove outliers
days_since_publication = datapaperfile['days_since_publication'].unique()
views = []
downloads = []
tot_citations = []
altmetric = []
tweets = []
for day in days_since_publication:
    mean_views = datapaperfile['views'][datapaperfile['days_since_publication'] == day].mean()
    mean_downloads = datapaperfile['downloads'][datapaperfile['days_since_publication'] == day].mean()
    mean_tweets = datapaperfile['tweets'][datapaperfile['days_since_publication'] == day].mean()
    mean_citations = datapaperfile['tot_citations'][datapaperfile['days_since_publication'] == day].mean()
    mean_altmetric = datapaperfile['altmetric'][datapaperfile['days_since_publication'] == day].mean()
    views.append(mean_views)
    downloads.append(mean_downloads)
    tot_citations.append(mean_citations)
    tweets.append(mean_tweets)
    altmetric.append(mean_altmetric)
df_means = pd.DataFrame({'days_since_publication': days_since_publication, \
    'mean_views': views, 'mean_downloads': downloads, \
    'mean_citations': tot_citations, 'mean_tweets': tweets, \
    'mean_altmetric': altmetric})

# Create dataframe with 90-day averages
interval = 90           # Set the length of the interval period in days
max_days = df_means['days_since_publication'].max()
periods = np.array(range(1,(round(max_days/interval)+2)))*interval
p_views = []
p_downloads = []
p_citations = []
p_tweets = []
p_altmetric = []
df_p = df_means         # Create a copy that we could work with

for period in periods:
    mean_p_views = df_p['mean_views'][df_p['days_since_publication'] <= period].mean()
    mean_p_downloads = df_p['mean_downloads'][df_p['days_since_publication'] <= period].mean()
    mean_p_citations = df_p['mean_citations'][df_p['days_since_publication'] <= period].mean()
    mean_p_altmetric = df_p['mean_altmetric'][df_p['days_since_publication'] <= period].mean()
    mean_p_tweets = df_p['mean_tweets'][df_p['days_since_publication'] <= period].mean()
    indices = df_p.index[df_p['days_since_publication'] <= period].tolist()
    p_views.append(mean_p_views)
    p_downloads.append(mean_p_downloads)
    p_citations.append(mean_p_citations)
    p_tweets.append(mean_p_tweets)
    p_altmetric.append(mean_p_altmetric)
    df_p = df_p.drop(indices)
df_means_period_datapaper = pd.DataFrame({'less_than_n_days_since_publication': periods, \
    'monthly_mean_views': p_views, 'monthly_mean_downloads': p_downloads, \
    'monthly_mean_citations': p_citations, 'monthly_mean_altmetric': p_altmetric, 'monthly_mean_tweets': p_tweets})
df_means_period_datapaper = df_means_period_datapaper.sort_values(by='less_than_n_days_since_publication', ascending=False)

# Reducing to years to be consistent with the other plots
df_means_period_datapaper['less_than_n_days_since_publication'] = [x/365 for x in df_means_period_datapaper['less_than_n_days_since_publication']]

print(df_means_period_datapaper['monthly_mean_citations'])


#DATAPAPERs_rdj
rdjfile = rdjfile[rdjfile['date'].notna()]
rdjfile['date'] = [datetime.strptime(str(x), date_format) for x in rdjfile['date']]
rdjfile['data_collection_date'] = [datetime.strptime(x, date_format) for x in rdjfile['data_collection_date']]
rdjfile['days_since_publication'] = (rdjfile['data_collection_date'] - rdjfile['date'])
rdjfile['days_since_publication'] = [x.days for x in rdjfile['days_since_publication']]
rdjfile['downloads'] = rdjfile['downloads']/rdjfile['days_since_publication']
rdjfile['views'] = rdjfile['views']/rdjfile['days_since_publication']
rdjfile['tot_citations'] = rdjfile['tot_citations']/rdjfile['days_since_publication']
rdjfile['altmetric'] = rdjfile['altmetric']/rdjfile['days_since_publication']

# Create dataframe with daily averages and remove outliers
days_since_publication = rdjfile['days_since_publication'].unique()
views = []
downloads = []
tot_citations = []
altmetric = []
for day in days_since_publication:
    mean_views = rdjfile['views'][rdjfile['days_since_publication'] == day].mean()
    mean_downloads = rdjfile['downloads'][rdjfile['days_since_publication'] == day].mean()
    mean_citations = rdjfile['tot_citations'][rdjfile['days_since_publication'] == day].mean()
    mean_altmetric = rdjfile['altmetric'][rdjfile['days_since_publication'] == day].mean()
    views.append(mean_views)
    downloads.append(mean_downloads)
    tot_citations.append(mean_citations)
    altmetric.append(mean_altmetric)
df_means = pd.DataFrame({'days_since_publication': days_since_publication, \
    'mean_views': views, 'mean_downloads': downloads, \
    'mean_citations': tot_citations, \
    'mean_altmetric': altmetric})

# Create dataframe with 90-day averages
interval = 90           # Set the length of the interval period in days
max_days = df_means['days_since_publication'].max()
periods = np.array(range(1,(round(max_days/interval)+2)))*interval
p_views = []
p_downloads = []
p_citations = []
p_altmetric = []
df_p = df_means         # Create a copy that we could work with

for period in periods:
    mean_p_views = df_p['mean_views'][df_p['days_since_publication'] <= period].mean()
    mean_p_downloads = df_p['mean_downloads'][df_p['days_since_publication'] <= period].mean()
    mean_p_citations = df_p['mean_citations'][df_p['days_since_publication'] <= period].mean()
    mean_p_altmetric = df_p['mean_altmetric'][df_p['days_since_publication'] <= period].mean()
    indices = df_p.index[df_p['days_since_publication'] <= period].tolist()
    p_views.append(mean_p_views)
    p_downloads.append(mean_p_downloads)
    p_citations.append(mean_p_citations)
    p_altmetric.append(mean_p_altmetric)
    df_p = df_p.drop(indices)
df_means_period_datapaper_rdj = pd.DataFrame({'less_than_n_days_since_publication': periods, \
    'monthly_mean_views': p_views, 'monthly_mean_downloads': p_downloads, \
    'monthly_mean_citations': p_citations, 'monthly_mean_altmetric': p_altmetric})
df_means_period_datapaper_rdj = df_means_period_datapaper_rdj.sort_values(by='less_than_n_days_since_publication', ascending=False)

# Reducing to years to be consistent with the other plots
df_means_period_datapaper_rdj['less_than_n_days_since_publication'] = [x/365 for x in df_means_period_datapaper_rdj['less_than_n_days_since_publication']]


#RESEARCH PAPERS_JOHD
researchfile = researchfile[researchfile['date'].notna()]
researchfile['date'] = [datetime.strptime(str(x), date_format) for x in researchfile['date']]
researchfile['days_since_publication'] = (data_collection_date - researchfile['date'])
researchfile['days_since_publication'] = [x.days for x in researchfile['days_since_publication']]
researchfile['tot_citations'] = researchfile['tot_citations']/researchfile['days_since_publication']
researchfile['altmetric'] = researchfile['altmetric']/researchfile['days_since_publication']

# Create dataframe with daily averages and remove outliers
days_since_publication = researchfile['days_since_publication'].unique()
tot_citations = []
altmetric = []
for day in days_since_publication:
    mean_citations = researchfile['tot_citations'][researchfile['days_since_publication'] == day].mean()
    mean_altmetric = researchfile['altmetric'][researchfile['days_since_publication'] == day].mean()
    tot_citations.append(mean_citations)
    altmetric.append(mean_altmetric)
df_means = pd.DataFrame({'days_since_publication': days_since_publication, \
    'mean_citations': tot_citations, \
    'mean_altmetric': altmetric})

# Create dataframe with 90-day averages
interval = 90           # Set the length of the interval period in days
max_days = df_means['days_since_publication'].max()
periods = np.array(range(1,(round(max_days/interval)+2)))*interval
p_citations = []
p_altmetric = []
df_p = df_means         # Create a copy that we could work with

for period in periods:
    mean_p_citations = df_p['mean_citations'][df_p['days_since_publication'] <= period].mean()
    mean_p_altmetric = df_p['mean_altmetric'][df_p['days_since_publication'] <= period].mean()
    indices = df_p.index[df_p['days_since_publication'] <= period].tolist()
    p_citations.append(mean_p_citations)
    p_altmetric.append(mean_p_altmetric)
    df_p = df_p.drop(indices)
df_means_period_research = pd.DataFrame({'less_than_n_days_since_publication': periods, \
    'monthly_mean_citations': p_citations, 'monthly_mean_altmetric': p_altmetric})
df_means_period_research = df_means_period_research.sort_values(by='less_than_n_days_since_publication', ascending=False)

# Reducing to years to be consistent with the other plots
df_means_period_research['less_than_n_days_since_publication'] = [x/365 for x in df_means_period_research['less_than_n_days_since_publication']]




#RESEARCH PAPERS_rdj
researchfile_rdj = researchfile_rdj[researchfile_rdj['date'].notna()]
researchfile_rdj['date'] = [datetime.strptime(str(x), date_format) for x in researchfile_rdj['date']]
researchfile_rdj['days_since_publication'] = (data_collection_date - researchfile_rdj['date'])
researchfile_rdj['days_since_publication'] = [x.days for x in researchfile_rdj['days_since_publication']]
researchfile_rdj['tot_citations'] = researchfile_rdj['tot_citations']/researchfile_rdj['days_since_publication']
researchfile_rdj['altmetric'] = researchfile_rdj['altmetric']/researchfile_rdj['days_since_publication']

# Create dataframe with daily averages and remove outliers
days_since_publication = researchfile_rdj['days_since_publication'].unique()
tot_citations = []
altmetric = []
for day in days_since_publication:
    mean_citations = researchfile_rdj['tot_citations'][researchfile_rdj['days_since_publication'] == day].mean()
    mean_altmetric = researchfile_rdj['altmetric'][researchfile_rdj['days_since_publication'] == day].mean()
    tot_citations.append(mean_citations)
    altmetric.append(mean_altmetric)
df_means = pd.DataFrame({'days_since_publication': days_since_publication, \
    'mean_citations': tot_citations, \
    'mean_altmetric': altmetric})

# Create dataframe with 90-day averages
interval = 90           # Set the length of the interval period in days
max_days = df_means['days_since_publication'].max()
periods = np.array(range(1,(round(max_days/interval)+2)))*interval
p_citations = []
p_altmetric = []
df_p = df_means         # Create a copy that we could work with

for period in periods:
    mean_p_citations = df_p['mean_citations'][df_p['days_since_publication'] <= period].mean()
    mean_p_altmetric = df_p['mean_altmetric'][df_p['days_since_publication'] <= period].mean()
    indices = df_p.index[df_p['days_since_publication'] <= period].tolist()
    p_citations.append(mean_p_citations)
    p_altmetric.append(mean_p_altmetric)
    df_p = df_p.drop(indices)
df_means_period_research_rdj = pd.DataFrame({'less_than_n_days_since_publication': periods, \
    'monthly_mean_citations': p_citations, 'monthly_mean_altmetric': p_altmetric})
df_means_period_research_rdj = df_means_period_research_rdj.sort_values(by='less_than_n_days_since_publication', ascending=False)

# Reducing to years to be consistent with the other plots
df_means_period_research_rdj['less_than_n_days_since_publication'] = [x/365 for x in df_means_period_research_rdj['less_than_n_days_since_publication']]


# Plot dataset age since publication and downloads on y axis (JOHD ONLY)
# JOHD
x = list(df_means_period_dataset['less_than_n_days_since_publication'])
y = list(df_means_period_dataset['monthly_mean_downloads'])
plt.scatter(x,y)
#plt.plot(x,y)
plt.title('JOHD: Dataset age vs. number of downloads')
plt.xlabel('Dataset age (years)')
plt.ylabel('Downloads')
plt.show()


# Plot articles age since publication and citations on y axis (JOHD AND RDJ)
# JOHD
x = list(df_means_period_datapaper['less_than_n_days_since_publication'])
y = list(df_means_period_datapaper['monthly_mean_citations'])
plt.scatter(x,y)
#plt.plot(x,y)
plt.title('JOHD: Data paper age vs. number of citations')
plt.xlabel('Data paper age (years)')
plt.ylabel('Citations')
plt.show()


#RDJ
x = list(df_means_period_datapaper_rdj['less_than_n_days_since_publication'])
y = list(df_means_period_datapaper_rdj['monthly_mean_citations'])
plt.scatter(x,y)
# #plt.plot(x,y)
plt.title('RDJ: Data paper age vs. number of citations')
plt.xlabel('Data paper age (years)')
plt.ylabel('Citations')
plt.show()


# JOHD+RDJ
newx = list(df_means_period_datapaper_rdj['less_than_n_days_since_publication']) + list(df_means_period_datapaper['less_than_n_days_since_publication'])
newy = list(df_means_period_datapaper_rdj['monthly_mean_citations']) + list(df_means_period_datapaper['monthly_mean_citations'])
plt.scatter(newx,newy)
# #plt.plot(x,y)
plt.title('JOHD + RDJ: Data paper age vs. number of citations')
plt.xlabel('Data paper age (years)')
plt.ylabel('Citations')
plt.show()

# Plot articles age since publication and altmetric on y axis (JOHD AND RDJ)

#JOHD
x = list(df_means_period_datapaper['less_than_n_days_since_publication'])
y = list(df_means_period_datapaper['monthly_mean_altmetric'])
plt.scatter(x,y)
#plt.plot(x,y)
plt.title('JOHD: Data paper age vs. Altmetric score')
plt.xlabel('Data paper age (years)')
plt.ylabel('Altmetric')
plt.show()


#RDJ
x = list(df_means_period_datapaper_rdj['less_than_n_days_since_publication'])
y = list(df_means_period_datapaper_rdj['monthly_mean_altmetric'])
plt.scatter(x,y)
#plt.plot(x,y)
plt.title('RDJ: Data paper age vs. Altmetric score')
plt.xlabel('Data paper age (years)')
plt.ylabel('Altmetric')
plt.show()

# JOHD+RDJ
newx = list(df_means_period_datapaper_rdj['less_than_n_days_since_publication']) + list(df_means_period_datapaper['less_than_n_days_since_publication'])
newy = list(df_means_period_datapaper_rdj['monthly_mean_altmetric']) + list(df_means_period_datapaper['monthly_mean_altmetric'])
plt.scatter(newx,newy)
#plt.plot(x,y)
plt.title('JOHD + RDJ: Data paper age vs. Altmetric score')
plt.xlabel('Data paper age (years)')
plt.ylabel('Altmetric')
plt.show()


# Plot articles age since publication and downloads of datapaper on y axis  (RDJ + JOHD)
#JOHD
x = list(df_means_period_datapaper['less_than_n_days_since_publication'])
y = list(df_means_period_datapaper['monthly_mean_downloads'])
plt.scatter(x,y)
#plt.plot(x,y)
plt.title('JOHD: Data paper age vs. Downloads')
plt.xlabel('Data paper age (years)')
plt.ylabel('Downloads')
plt.show()

#RDJ
x = list(df_means_period_datapaper_rdj['less_than_n_days_since_publication'])
y = list(df_means_period_datapaper_rdj['monthly_mean_downloads'])
plt.scatter(x,y)
#plt.plot(x,y)
plt.title('RDJ: Data paper age vs. Downloads')
plt.xlabel('Data paper age (years)')
plt.ylabel('Downloads')
plt.show()


# JOHD+RDJ
newx = list(df_means_period_datapaper_rdj['less_than_n_days_since_publication']) + list(df_means_period_datapaper['less_than_n_days_since_publication'])
newy = list(df_means_period_datapaper_rdj['monthly_mean_downloads']) + list(df_means_period_datapaper['monthly_mean_downloads'])
plt.scatter(newx,newy)
#plt.plot(x,y)
plt.title('JOHD + RDJ: Data paper age vs. Downloads')
plt.xlabel('Data paper age (years)')
plt.ylabel('Downloads')
plt.show()


# Plot articles age since publication and views of datapaper on y axis (RDJ + JOHD)
#JOHD
x = list(df_means_period_datapaper['less_than_n_days_since_publication'])
y = list(df_means_period_datapaper['monthly_mean_views'])
plt.scatter(x,y)
#plt.plot(x,y)
plt.title('JOHD: Data paper age vs. views')
plt.xlabel('Data paper age (years)')
plt.ylabel('Views')
plt.show()

#RDJ
x = list(df_means_period_datapaper_rdj['less_than_n_days_since_publication'])
y = list(df_means_period_datapaper_rdj['monthly_mean_views'])
plt.scatter(x,y)
#plt.plot(x,y)
plt.title('RDJ: Data paper age vs. views')
plt.xlabel('Data paper age (years)')
plt.ylabel('Views')
plt.show()

# JOHD+RDJ
newx = list(df_means_period_datapaper_rdj['less_than_n_days_since_publication']) + list(df_means_period_datapaper['less_than_n_days_since_publication'])
newy = list(df_means_period_datapaper_rdj['monthly_mean_views']) + list(df_means_period_datapaper['monthly_mean_views'])
plt.scatter(newx,newy)
# #plt.plot(x,y)
plt.title('JOHD + RDJ: Data paper age vs. Views')
plt.xlabel('Data paper age (years)')
plt.ylabel('Views')
plt.show()


# Plot research articles age since publication and citations on y axis (RDJ + JOHD)
#JOHD
x = list(df_means_period_research['less_than_n_days_since_publication'])
y = list(df_means_period_research['monthly_mean_citations'])
plt.scatter(x,y)
# #plt.plot(x,y)
plt.title('Research papers age (assoc. w/ JOHD data papers) vs. citations of res papers')
plt.xlabel('Research paper age (years)')
plt.ylabel('Citations')
plt.show()

#RDJ
x = list(df_means_period_research_rdj['less_than_n_days_since_publication'])
y = list(df_means_period_research_rdj['monthly_mean_citations'])
plt.scatter(x,y)
#plt.plot(x,y)
plt.title('Research papers age (assoc. w/ RDJ data papers) vs. citations of res papers')
plt.xlabel('Research paper age (years)')
plt.ylabel('Citations')
plt.show()

# JOHD+RDJ
newx = list(df_means_period_research_rdj['less_than_n_days_since_publication']) + list(df_means_period_research['less_than_n_days_since_publication'])
newy = list(df_means_period_research_rdj['monthly_mean_citations']) + list(df_means_period_research['monthly_mean_citations'])
plt.scatter(newx,newy)
#plt.plot(x,y)
plt.title('Research papers age (assoc. w/ RDJ+JOHD data papers) vs. citations of res papers')
plt.xlabel('Research paper age (years)')
plt.ylabel('Citations')
plt.show()


# Plot research articles age since publication and Altmetric on y axis (RDJ + JOHD)
#JOHD
x = list(df_means_period_research['less_than_n_days_since_publication'])
y = list(df_means_period_research['monthly_mean_altmetric'])
plt.scatter(x,y)
# #plt.plot(x,y)
plt.title('Research papers age (assoc. w/ JOHD data papers) vs. altmetric of res papers')
plt.xlabel('Research paper age (years)')
plt.ylabel('Altmetric')
plt.show()

#RDJ
x = list(df_means_period_research_rdj['less_than_n_days_since_publication'])
y = list(df_means_period_research_rdj['monthly_mean_altmetric'])
plt.scatter(x,y)
#plt.plot(x,y)
plt.title('Research papers age (assoc. w/ RDJ data papers) vs. altmetric of res papers')
plt.xlabel('Research paper age (years)')
plt.ylabel('Altmetric')
plt.show()

# JOHD+RDJ
newx = list(df_means_period_research_rdj['less_than_n_days_since_publication']) + list(df_means_period_research['less_than_n_days_since_publication'])
newy = list(df_means_period_research_rdj['monthly_mean_altmetric']) + list(df_means_period_research['monthly_mean_altmetric'])
plt.scatter(newx,newy)
#plt.plot(x,y)
plt.title('Research papers age (assoc. w/ RDJ+JOHD data papers) vs. altmetric of res papers')
plt.xlabel('Research paper age (years)')
plt.ylabel('Altmetric')
plt.show()