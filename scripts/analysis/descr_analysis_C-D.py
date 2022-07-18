# Overall changes in metrics growth/decrease rates over time

import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np

dateoflastdf = '2022-07-04' # change to date of last export

datapaperfile = pd.read_csv('./outputs/final_outputs/johd/{}-final-datapapers-johd.csv'.format(dateoflastdf),
                            usecols=["DOI",
                                    "date",
                                    "downloads",
                                    "views",
                                    "data_collection_date",
                                    "Times cited",
                                    "Recent citations",
                                    "Altmetric"])
datasetfile = pd.read_csv('./outputs/final_outputs/johd/{}-final-datasets-johd.csv'.format(dateoflastdf),
                            usecols=["DOI",
                                    "date",
                                    "views",
                                    "unique-views",
                                    "downloads",
                                    "unique-downloads"])
researchfile = pd.read_csv('./outputs/final_outputs/research_papers/{}-final-research_papers-johd.csv'.format(dateoflastdf),
                            usecols=["DOI",
                                    "Times cited",
                                    "Recent citations",
                                    "Altmetric",
                                    "Publication Date (online)"])
rdjfile = pd.read_csv('./outputs/final_outputs/rdj/{}-final-datapapers-rdj.csv'.format(dateoflastdf),
                            usecols=["DOI",
                                    "date",
                                    "downloads",
                                    "views",
                                    "data_collection_date",
                                    "Times cited",
                                    "Recent citations",
                                    "Altmetric"])
rdjdatasetfile = pd.read_csv('./outputs/final_outputs/rdj/{}-final-datasets-rdj.csv'.format(dateoflastdf),
                            usecols=["DOI",
                                    "date",
                                    "views",
                                    "unique-views",
                                    "downloads",
                                    "unique-downloads"])
researchfile_rdj = pd.read_csv('./outputs/final_outputs/research_papers/{}-final-research_papers-rdj.csv'.format(dateoflastdf),
                            usecols=["DOI",
                                    "Publication Date (online)",
                                    "Times cited",
                                    "Recent citations",
                                    "Altmetric",
                                    "Publication Date (online)"])

datapaperfile = datapaperfile.rename(columns={"date": "date_datapaper","views": "views_datapaper", "downloads": "downloads_datapaper", "Times cited": "tot_citations_datapaper","Recent citations": "rec_citations_datapaper", "Altmetric": "altmetric_datapaper"})
datasetfile = datasetfile.rename(columns={"date": "date_dataset","views": "views_dataset","unique-views": "unique-views_dataset", "downloads": "downloads_dataset", "unique-downloads": "unique-downloads_dataset"})
researchfile = researchfile.rename(columns={"Publication Date (online)": "date_research","Times cited": "tot_citations_research","Recent citations": "rec_citations_research", "Altmetric": "altmetric_research"})
rdjfile = rdjfile.rename(columns={"Publication Date (online)": "date_datapaper","downloads": "downloads_datapaper", "views": "views_datapaper","Times cited": "tot_citations_datapaper","Recent citations": "rec_citations_datapaper", "Altmetric": "altmetric_datapaper"})
rdjdatasetfile = rdjdatasetfile.rename(columns={"date": "date_dataset","views": "views_dataset","unique-views": "unique-views_dataset", "downloads": "downloads_dataset", "unique-downloads": "unique-downloads_dataset"})
researchfile_rdj = researchfile_rdj.rename(columns={"Publication Date (online)": "date_research","Times cited": "tot_citations_research","Recent citations": "rec_citations_research", "Altmetric": "altmetric_research"})

datapaperfileall = pd.concat([datapaperfile,rdjfile])
datasetfileall = pd.concat([datasetfile,rdjdatasetfile])
researchfileall = pd.concat([researchfile,researchfile_rdj])

date_format = "%Y-%m-%d"

data_collection_date = dateoflastdf
#DATAPAPERs
## CITATIONS
datapaperfile = datapaperfileall[['tot_citations_datapaper','date_datapaper','data_collection_date']]
datapaperfile = datapaperfile[datapaperfile['tot_citations_datapaper'].notna()]
q1, q3= np.percentile(sorted(datapaperfile['tot_citations_datapaper']),[25,75])
iqr = q3 - q1
lower_bound = q1 -(1.5 * iqr) 
upper_bound = q3 +(1.5 * iqr)

datapaperfile  = datapaperfile.loc[(datapaperfile['tot_citations_datapaper'] <= upper_bound) & (datapaperfile['tot_citations_datapaper'] >= lower_bound)] 
datapaperfile = datapaperfile[datapaperfile['date_datapaper'].notna()]
datapaperfile['date_datapaper'] = [datetime.strptime(str(x), date_format) for x in datapaperfile['date_datapaper']]
datapaperfile['data_collection_date'] = [datetime.strptime(x, date_format) for x in datapaperfile['data_collection_date']]
datapaperfile['days_since_publication'] = (datapaperfile['data_collection_date'] - datapaperfile['date_datapaper'])
datapaperfile['days_since_publication'] = [x.days for x in datapaperfile['days_since_publication']]
datapaperfile['tot_citations_datapaper'] = datapaperfile['tot_citations_datapaper']/datapaperfile['days_since_publication']
days_since_publication = datapaperfile['days_since_publication'].unique()
tot_citations_datapaper = []
for day in days_since_publication:
    mean_citations_datapaper = datapaperfile['tot_citations_datapaper'][datapaperfile['days_since_publication'] == day].mean()
    tot_citations_datapaper.append(mean_citations_datapaper)
df_means = pd.DataFrame({'days_since_publication': days_since_publication, 'mean_citations_datapaper': tot_citations_datapaper})
# Create dataframe with 90-day averages
interval = 90          # Set the length of the interval period in days
max_days = df_means['days_since_publication'].max()
periods = np.array(range(1,(round(max_days/interval)+2)))*interval
p_citations_datapaper = []
df_p = df_means         # Create a copy that we could work with
for period in periods:
    mean_p_citations_datapaper = df_p['mean_citations_datapaper'][df_p['days_since_publication'] <= period].mean()
    indices = df_p.index[df_p['days_since_publication'] <= period].tolist()
    p_citations_datapaper.append(mean_p_citations_datapaper)
    df_p = df_p.drop(indices)
df_means_period_datapaper = pd.DataFrame({'less_than_n_days_since_publication': periods, 'monthly_mean_citations_datapaper': p_citations_datapaper})
df_means_period_datapaper = df_means_period_datapaper.sort_values(by='less_than_n_days_since_publication', ascending=False)
# Reducing to years to be consistent with the other plots
df_means_period_datapaper['less_than_n_days_since_publication'] = [x/365 for x in df_means_period_datapaper['less_than_n_days_since_publication']]
#PLOT IT
x = list(df_means_period_datapaper['less_than_n_days_since_publication'])
y = list(df_means_period_datapaper['monthly_mean_citations_datapaper'])
plt.scatter(x,y)
#plt.plot(x,y)
# plt.title('Data paper age vs. number of citations')
plt.xlabel('Age of data paper (years)')
plt.ylabel('(Age-normalised) citations')
plt.savefig("./outputs/figures/figure9-dev-cit-dp.jpeg",dpi=300)

plt.show()


## ALTMETRIC
datapaperfile = datapaperfileall[['altmetric_datapaper','date_datapaper','data_collection_date']]
datapaperfile = datapaperfile[datapaperfile['altmetric_datapaper'].notna()]
q1, q3= np.percentile(sorted(datapaperfile['altmetric_datapaper']),[25,75])
iqr = q3 - q1
lower_bound = q1 -(1.5 * iqr) 
upper_bound = q3 +(1.5 * iqr)
datapaperfile  = datapaperfile.loc[(datapaperfile['altmetric_datapaper'] <= upper_bound) & (datapaperfile['altmetric_datapaper'] >= lower_bound)] 

datapaperfile = datapaperfile[datapaperfile['date_datapaper'].notna()]
datapaperfile['date_datapaper'] = [datetime.strptime(str(x), date_format) for x in datapaperfile['date_datapaper']]
datapaperfile['data_collection_date'] = [datetime.strptime(x, date_format) for x in datapaperfile['data_collection_date']]
datapaperfile['days_since_publication'] = (datapaperfile['data_collection_date'] - datapaperfile['date_datapaper'])
datapaperfile['days_since_publication'] = [x.days for x in datapaperfile['days_since_publication']]
datapaperfile['altmetric_datapaper'] = datapaperfile['altmetric_datapaper']/datapaperfile['days_since_publication']
days_since_publication = datapaperfile['days_since_publication'].unique()
altmetric_datapaper = []
for day in days_since_publication:
    mean_altmetric_datapaper = datapaperfile['altmetric_datapaper'][datapaperfile['days_since_publication'] == day].mean()
    altmetric_datapaper.append(mean_altmetric_datapaper)
df_means = pd.DataFrame({'days_since_publication': days_since_publication, 'mean_altmetric_datapaper': altmetric_datapaper})
# Create dataframe with 90-day averages
interval = 90          # Set the length of the interval period in days
max_days = df_means['days_since_publication'].max()
periods = np.array(range(1,(round(max_days/interval)+2)))*interval
p_altmetric_datapaper = []
df_p = df_means         # Create a copy that we could work with
for period in periods:
    mean_p_altmetric_datapaper = df_p['mean_altmetric_datapaper'][df_p['days_since_publication'] <= period].mean()
    indices = df_p.index[df_p['days_since_publication'] <= period].tolist()
    p_altmetric_datapaper.append(mean_p_altmetric_datapaper)
    df_p = df_p.drop(indices)
df_means_period_datapaper = pd.DataFrame({'less_than_n_days_since_publication': periods, 'monthly_mean_altmetric_datapaper': p_altmetric_datapaper})
df_means_period_datapaper = df_means_period_datapaper.sort_values(by='less_than_n_days_since_publication', ascending=False)
# Reducing to years to be consistent with the other plots
df_means_period_datapaper['less_than_n_days_since_publication'] = [x/365 for x in df_means_period_datapaper['less_than_n_days_since_publication']]
#PLOT IT
x = list(df_means_period_datapaper['less_than_n_days_since_publication'])
y = list(df_means_period_datapaper['monthly_mean_altmetric_datapaper'])
plt.scatter(x,y)
#plt.plot(x,y)
# plt.title('Data paper age vs. number of altmetric')
plt.xlabel('Age of data paper (years)')
plt.ylabel('(Age-normalised) Altmetric score')
plt.savefig("./outputs/figures/figure11-dev-alt-dp.jpeg",dpi=300)

plt.show()

##VIEWS AND DOWNL
datapaperfile = datapaperfileall[['downloads_datapaper','views_datapaper','date_datapaper','data_collection_date']]
datapaperfile = datapaperfile[datapaperfile['downloads_datapaper'].notna()]
q1, q3= np.percentile(sorted(datapaperfile['downloads_datapaper']),[25,75])
iqr = q3 - q1
lower_bound = q1 -(1.5 * iqr) 
upper_bound = q3 +(1.5 * iqr)
datapaperfile  = datapaperfile.loc[(datapaperfile['downloads_datapaper'] <= upper_bound) & (datapaperfile['downloads_datapaper'] >= lower_bound)] 
datapaperfile = datapaperfile[datapaperfile['views_datapaper'].notna()]
q1, q3= np.percentile(sorted(datapaperfile['views_datapaper']),[25,75])
iqr = q3 - q1
lower_bound = q1 -(1.5 * iqr) 
upper_bound = q3 +(1.5 * iqr)
datapaperfile  = datapaperfile.loc[(datapaperfile['views_datapaper'] <= upper_bound) & (datapaperfile['views_datapaper'] >= lower_bound)] 
datapaperfile = datapaperfile[datapaperfile['date_datapaper'].notna()]
datapaperfile['date_datapaper'] = [datetime.strptime(str(x), date_format) for x in datapaperfile['date_datapaper']]
data_collection_date= datetime.strptime(data_collection_date, date_format)
datapaperfile['days_since_publication'] = (data_collection_date - datapaperfile['date_datapaper'])
datapaperfile['days_since_publication'] = [x.days for x in datapaperfile['days_since_publication']]
datapaperfile['downloads_datapaper'] = datapaperfile['downloads_datapaper']/datapaperfile['days_since_publication']
datapaperfile['views_datapaper'] = datapaperfile['views_datapaper']/datapaperfile['days_since_publication']
days_since_publication = datapaperfile['days_since_publication'].unique()
views_datapaper = []
downloads_datapaper = []
for day in days_since_publication:
    mean_views_datapaper = datapaperfile['views_datapaper'][datapaperfile['days_since_publication'] == day].mean()
    mean_downloads_datapaper = datapaperfile['downloads_datapaper'][datapaperfile['days_since_publication'] == day].mean()
    views_datapaper.append(mean_views_datapaper)
    downloads_datapaper.append(mean_downloads_datapaper)
df_means = pd.DataFrame({'days_since_publication': days_since_publication, \
    'mean_views_datapaper': views_datapaper, 'mean_downloads_datapaper': downloads_datapaper})
# Create dataframe with 90-day averages
interval = 90          # Set the length of the interval period in days
max_days = df_means['days_since_publication'].max()
periods = np.array(range(1,(round(max_days/interval)+2)))*interval
p_views_datapaper = []
p_downloads_datapaper = []
df_p = df_means         # Create a copy that we could work with
for period in periods:
    mean_p_views_datapaper = df_p['mean_views_datapaper'][df_p['days_since_publication'] <= period].mean()
    mean_p_downloads_datapaper = df_p['mean_downloads_datapaper'][df_p['days_since_publication'] <= period].mean()
    indices = df_p.index[df_p['days_since_publication'] <= period].tolist()
    p_views_datapaper.append(mean_p_views_datapaper)
    p_downloads_datapaper.append(mean_p_downloads_datapaper)
    df_p = df_p.drop(indices)
df_means_period_datapaper = pd.DataFrame({'less_than_n_days_since_publication': periods, \
    'monthly_mean_views_datapaper': p_views_datapaper, 'monthly_mean_downloads_datapaper': p_downloads_datapaper})
df_means_period_datapaper = df_means_period_datapaper.sort_values(by='less_than_n_days_since_publication', ascending=False)
# Reducing to years to be consistent with the other plots
df_means_period_datapaper['less_than_n_days_since_publication'] = [x/365 for x in df_means_period_datapaper['less_than_n_days_since_publication']]
#PLOT IT
x = np.array(df_means_period_datapaper['less_than_n_days_since_publication'])
y = np.array(df_means_period_datapaper['monthly_mean_views_datapaper'])
plt.scatter(x,y,c='red',label='Views')
# Downlaods
x = np.array(df_means_period_datapaper['less_than_n_days_since_publication'])
y = np.array(df_means_period_datapaper['monthly_mean_downloads_datapaper'])
plt.scatter(x,y,c='yellow',label='Downloads')
plt.legend()
plt.xlabel('Age of data paper (years)')
plt.ylabel('(Age-normalised) downloads')
plt.grid(axis='y', alpha=0.75)
# plt.title('Data papers: views/downloads')
plt.savefig("./outputs/figures/figureB2-dev-down-views-dp.jpeg",dpi=300)

plt.show()


#DATASETS
## VIEWS AND DOWNL
datasetfile = datasetfileall[['downloads_dataset','views_dataset','date_dataset']]
datasetfile = datasetfile[datasetfile['downloads_dataset'].notna()]
q1, q3= np.percentile(sorted(datasetfile['downloads_dataset']),[25,75])
iqr = q3 - q1
lower_bound = q1 -(1.5 * iqr) 
upper_bound = q3 +(1.5 * iqr)
datasetfile  = datasetfile.loc[(datasetfile['downloads_dataset'] <= upper_bound) & (datasetfile['downloads_dataset'] >= lower_bound)] 
datasetfile = datasetfile[datasetfile['views_dataset'].notna()]
q1, q3= np.percentile(sorted(datasetfile['views_dataset']),[25,75])
iqr = q3 - q1
lower_bound = q1 -(1.5 * iqr) 
upper_bound = q3 +(1.5 * iqr)
datasetfile  = datasetfile.loc[(datasetfile['views_dataset'] <= upper_bound) & (datasetfile['views_dataset'] >= lower_bound)] 
datasetfile = datasetfile[datasetfile['date_dataset'].notna()]
datasetfile['date_dataset'] = [datetime.strptime(str(x), date_format) for x in datasetfile['date_dataset']]
data_collection_date= datetime.strptime(dateoflastdf, date_format)
datasetfile['days_since_publication'] = (data_collection_date - datasetfile['date_dataset'])
datasetfile['days_since_publication'] = [x.days for x in datasetfile['days_since_publication']]
datasetfile['downloads_dataset'] = datasetfile['downloads_dataset']/datasetfile['days_since_publication']
datasetfile['views_dataset'] = datasetfile['views_dataset']/datasetfile['days_since_publication']
days_since_publication = datasetfile['days_since_publication'].unique()
views_dataset = []
downloads_dataset = []
for day in days_since_publication:
    mean_views_dataset = datasetfile['views_dataset'][datasetfile['days_since_publication'] == day].mean()
    mean_downloads_dataset = datasetfile['downloads_dataset'][datasetfile['days_since_publication'] == day].mean()
    views_dataset.append(mean_views_dataset)
    downloads_dataset.append(mean_downloads_dataset)
df_means = pd.DataFrame({'days_since_publication': days_since_publication, \
    'mean_views_dataset': views_dataset, 'mean_downloads_dataset': downloads_dataset})
# Create dataframe with 90-day averages
interval = 90          # Set the length of the interval period in days
max_days = df_means['days_since_publication'].max()
periods = np.array(range(1,(round(max_days/interval)+2)))*interval
p_views_dataset = []
p_downloads_dataset = []
df_p = df_means         # Create a copy that we could work with
for period in periods:
    mean_p_views_dataset = df_p['mean_views_dataset'][df_p['days_since_publication'] <= period].mean()
    mean_p_downloads_dataset = df_p['mean_downloads_dataset'][df_p['days_since_publication'] <= period].mean()
    indices = df_p.index[df_p['days_since_publication'] <= period].tolist()
    p_views_dataset.append(mean_p_views_dataset)
    p_downloads_dataset.append(mean_p_downloads_dataset)
    df_p = df_p.drop(indices)
df_means_period_dataset = pd.DataFrame({'less_than_n_days_since_publication': periods, \
    'monthly_mean_views_dataset': p_views_dataset, 'monthly_mean_downloads_dataset': p_downloads_dataset})
df_means_period_dataset = df_means_period_dataset.sort_values(by='less_than_n_days_since_publication', ascending=False)
# Reducing to years to be consistent with the other plots
df_means_period_dataset['less_than_n_days_since_publication'] = [x/365 for x in df_means_period_dataset['less_than_n_days_since_publication']]
#PLOT IT
x = np.array(df_means_period_dataset['less_than_n_days_since_publication'])
y = np.array(df_means_period_dataset['monthly_mean_views_dataset'])
plt.scatter(x,y,c='red',label='Views')
# Downlaods
x = np.array(df_means_period_dataset['less_than_n_days_since_publication'])
y = np.array(df_means_period_dataset['monthly_mean_downloads_dataset'])
plt.scatter(x,y,c='yellow',label='Downloads')
plt.legend()
plt.xlabel('Age of dataset (years)')
plt.ylabel('(Age-normalised) downloads')
plt.grid(axis='y', alpha=0.75)
# plt.title('Dataset: views/downloads')
plt.savefig("./outputs/figures/figureB8-dev-down-views-ds.jpeg",dpi=300)

plt.show()

#RESEARCH PAPERS
## CITATIONS
researchfile = researchfileall[['tot_citations_research','date_research']]
researchfile = researchfile[researchfile['tot_citations_research'].notna()]
q1, q3= np.percentile(sorted(researchfile['tot_citations_research']),[25,75])
iqr = q3 - q1
lower_bound = q1 -(1.5 * iqr) 
upper_bound = q3 +(1.5 * iqr)

researchfile  = researchfile.loc[(researchfile['tot_citations_research'] <= upper_bound) & (researchfile['tot_citations_research'] >= lower_bound)] 
researchfile = researchfile[researchfile['date_research'].notna()]
researchfile['date_research'] = [datetime.strptime(str(x), date_format) for x in researchfile['date_research']]
data_collection_date = datetime.strptime(dateoflastdf, date_format)
researchfile['days_since_publication'] = (data_collection_date - researchfile['date_research'])
researchfile['days_since_publication'] = [x.days for x in researchfile['days_since_publication']]
researchfile['tot_citations_research'] = researchfile['tot_citations_research']/researchfile['days_since_publication']
days_since_publication = researchfile['days_since_publication'].unique()
tot_citations_research = []
for day in days_since_publication:
    mean_citations_research = researchfile['tot_citations_research'][researchfile['days_since_publication'] == day].mean()
    tot_citations_research.append(mean_citations_research)
df_means = pd.DataFrame({'days_since_publication': days_since_publication, 'mean_citations_research': tot_citations_research})
# Create dataframe with 90-day averages
interval = 90          # Set the length of the interval period in days
max_days = df_means['days_since_publication'].max()
periods = np.array(range(1,(round(max_days/interval)+2)))*interval
p_citations_research = []
df_p = df_means         # Create a copy that we could work with
for period in periods:
    mean_p_citations_research = df_p['mean_citations_research'][df_p['days_since_publication'] <= period].mean()
    indices = df_p.index[df_p['days_since_publication'] <= period].tolist()
    p_citations_research.append(mean_p_citations_research)
    df_p = df_p.drop(indices)
df_means_period_research = pd.DataFrame({'less_than_n_days_since_publication': periods, 'monthly_mean_citations_research': p_citations_research})
df_means_period_research = df_means_period_research.sort_values(by='less_than_n_days_since_publication', ascending=False)
# Reducing to years to be consistent with the other plots
df_means_period_research['less_than_n_days_since_publication'] = [x/365 for x in df_means_period_research['less_than_n_days_since_publication']]
#PLOT IT
x = list(df_means_period_research['less_than_n_days_since_publication'])
y = list(df_means_period_research['monthly_mean_citations_research'])
plt.scatter(x,y)
#plt.plot(x,y)
# plt.title('Data paper age vs. number of citations')
plt.xlabel('Age of research paper (years)')
plt.ylabel('Age-normalised citations')
# plt.ylabel('Citations')
plt.savefig("./outputs/figures/figureB4-dev-cit-rp.jpeg",dpi=300)

plt.show()


## ALTMETRIC
researchfile = researchfileall[['altmetric_research','date_research']]
researchfile = researchfile[researchfile['altmetric_research'].notna()]
q1, q3= np.percentile(sorted(researchfile['altmetric_research']),[25,75])
iqr = q3 - q1
lower_bound = q1 -(1.5 * iqr) 
upper_bound = q3 +(1.5 * iqr)
researchfile  = researchfile.loc[(researchfile['altmetric_research'] <= upper_bound) & (researchfile['altmetric_research'] >= lower_bound)] 

researchfile = researchfile[researchfile['date_research'].notna()]
researchfile['date_research'] = [datetime.strptime(str(x), date_format) for x in researchfile['date_research']]
data_collection_date = datetime.strptime(dateoflastdf, date_format)
researchfile['days_since_publication'] = (data_collection_date - researchfile['date_research'])
researchfile['days_since_publication'] = [x.days for x in researchfile['days_since_publication']]
researchfile['altmetric_research'] = researchfile['altmetric_research']/researchfile['days_since_publication']
days_since_publication = researchfile['days_since_publication'].unique()
altmetric_research = []
for day in days_since_publication:
    mean_altmetric_research = researchfile['altmetric_research'][researchfile['days_since_publication'] == day].mean()
    altmetric_research.append(mean_altmetric_research)
df_means = pd.DataFrame({'days_since_publication': days_since_publication, 'mean_altmetric_research': altmetric_research})
# Create dataframe with 90-day averages
interval = 90          # Set the length of the interval period in days
max_days = df_means['days_since_publication'].max()
periods = np.array(range(1,(round(max_days/interval)+2)))*interval
p_altmetric_research = []
df_p = df_means         # Create a copy that we could work with
for period in periods:
    mean_p_altmetric_research = df_p['mean_altmetric_research'][df_p['days_since_publication'] <= period].mean()
    indices = df_p.index[df_p['days_since_publication'] <= period].tolist()
    p_altmetric_research.append(mean_p_altmetric_research)
    df_p = df_p.drop(indices)
df_means_period_research = pd.DataFrame({'less_than_n_days_since_publication': periods, 'monthly_mean_altmetric_research': p_altmetric_research})
df_means_period_research = df_means_period_research.sort_values(by='less_than_n_days_since_publication', ascending=False)
# Reducing to years to be consistent with the other plots
df_means_period_research['less_than_n_days_since_publication'] = [x/365 for x in df_means_period_research['less_than_n_days_since_publication']]
#PLOT IT
x = list(df_means_period_research['less_than_n_days_since_publication'])
y = list(df_means_period_research['monthly_mean_altmetric_research'])
plt.scatter(x,y)
#plt.plot(x,y)
# plt.title('Data paper age vs. number of altmetric')
plt.xlabel('Age of research paper (years)')
plt.ylabel('Age-normalised Altmetric score')
# plt.ylabel('Altmetric')
plt.savefig("./outputs/figures/figureB6-alt-rp.jpeg",dpi=300)

plt.show()