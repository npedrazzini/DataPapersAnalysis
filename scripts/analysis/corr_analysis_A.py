#Are higher-impact data papers associated with higher-impact datasets/research papers?

import pandas as pd
from datetime import datetime
import functools as ft
from scipy.stats import spearmanr
import csv

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
                                    "date",
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

researchfile = researchfile.rename(columns={"Publication Date (online)": "date_research_johd","Times cited": "tot_citations_research_johd","Recent citations": "rec_citations_research_johd", "Altmetric": "altmetric_research_johd"})
datasetfile = datasetfile.rename(columns={"date": "date_dataset_johd","views": "views_dataset_johd","unique-views": "unique-views_dataset_johd", "downloads": "downloads_dataset_johd", "unique-downloads": "unique-downloads_dataset_johd"})
datapaperfile = datapaperfile.rename(columns={"date": "date_datapaper_johd","views": "views_datapaper_johd", "downloads": "downloads_datapaper_johd","tweets": "tweets_datapaper", "Times cited": "tot_citations_datapaper_johd","Recent citations": "rec_citations_datapaper_johd", "Altmetric": "altmetric_datapaper_johd"})
rdjdf = rdjfile.rename(columns={"date": "date_dataset_rdj","Publication Date (online)": "date_datapaper_rdj","downloads": "downloads_datapaper_rdj", "views": "views_datapaper_rdj","Times cited": "tot_citations_datapaper_rdj","Recent citations": "rec_citations_datapaper_rdj", "Altmetric": "altmetric_datapaper_rdj"})
researchfile_rdj = researchfile_rdj.rename(columns={"Publication Date (online)": "date_research_rdj","Times cited": "tot_citations_research_rdj","Recent citations": "rec_citations_research_rdj", "Altmetric": "altmetric_research_rdj"})


date_format = "%Y-%m-%d"

dfs = [researchfile,datasetfile,datapaperfile]
df = ft.reduce(lambda left, right: pd.merge(left, right, on='DOI'), dfs)
df['data_collection_date'] = [datetime.strptime(x, date_format) for x in df['data_collection_date']]
df = df[df['date_dataset_johd'].notna()]
df = df[df['date_datapaper_johd'].notna()]
df['date_dataset_johd'] = [datetime.strptime(str(x), date_format) for x in df['date_dataset_johd']]
df['date_datapaper_johd'] = [datetime.strptime(str(x), date_format) for x in df['date_datapaper_johd']]
df['days_since_pub_dataset'] = df['data_collection_date'] - df['date_dataset_johd']
df['days_since_pub_dataset'] = [x.days for x in df['days_since_pub_dataset']]
df['days_since_pub_datapaper'] = df['data_collection_date'] - df['date_datapaper_johd']
df['days_since_pub_datapaper'] = [x.days for x in df['days_since_pub_datapaper']]

df['views_dataset_johd'] = df['views_dataset_johd']/df['days_since_pub_dataset']
df['unique-views_dataset_johd'] = df['unique-views_dataset_johd']/df['days_since_pub_dataset']
df['downloads_dataset_johd'] = df['downloads_dataset_johd']/df['days_since_pub_dataset']
df['unique-downloads_dataset_johd'] = df['unique-downloads_dataset_johd']/df['days_since_pub_dataset']
df['downloads_datapaper_johd'] = df['downloads_datapaper_johd']/df['days_since_pub_datapaper']
df['views_datapaper_johd'] = df['views_datapaper_johd']/df['days_since_pub_datapaper']
df['tweets_datapaper'] = df['tweets_datapaper']/df['days_since_pub_datapaper']
df['tot_citations_datapaper_johd'] = df['tot_citations_datapaper_johd']/df['days_since_pub_datapaper']
df['rec_citations_datapaper_johd'] = df['rec_citations_datapaper_johd']/df['days_since_pub_datapaper']
df['altmetric_datapaper_johd'] = df['altmetric_datapaper_johd']/df['days_since_pub_datapaper']

dfs_rdj = [rdjdf,researchfile_rdj]
df_rdj = ft.reduce(lambda left, right: pd.merge(left, right, on='DOI'), dfs_rdj)
df_rdj['data_collection_date'] = [datetime.strptime(x, date_format) for x in df_rdj['data_collection_date']]
df_rdj = df_rdj[df_rdj['date_dataset_rdj'].notna()]
df_rdj = df_rdj[df_rdj['date_datapaper_rdj'].notna()]
df_rdj['date_dataset_rdj'] = [datetime.strptime(str(x), date_format) for x in df_rdj['date_dataset_rdj']]
df_rdj['date_datapaper_rdj'] = [datetime.strptime(str(x), date_format) for x in df_rdj['date_datapaper_rdj']]
mask = (df_rdj['date_datapaper_rdj'] > '2015-09-1')
df_rdj = df_rdj.loc[mask]
df_rdj['days_since_pub_dataset'] = df_rdj['data_collection_date'] - df_rdj['date_dataset_rdj']
df_rdj['days_since_pub_dataset'] = [x.days for x in df_rdj['days_since_pub_dataset']]
df_rdj['days_since_pub_datapaper'] = df_rdj['data_collection_date'] - df_rdj['date_datapaper_rdj']
df_rdj['days_since_pub_datapaper'] = [x.days for x in df_rdj['days_since_pub_datapaper']]

df_rdj['downloads_datapaper_rdj'] = df_rdj['downloads_datapaper_rdj']/df_rdj['days_since_pub_datapaper']
df_rdj['views_datapaper_rdj'] = df_rdj['views_datapaper_rdj']/df_rdj['days_since_pub_datapaper']
df_rdj['tot_citations_datapaper_rdj'] = df_rdj['tot_citations_datapaper_rdj']/df['days_since_pub_datapaper']
df_rdj['rec_citations_datapaper_rdj'] = df_rdj['rec_citations_datapaper_rdj']/df_rdj['days_since_pub_datapaper']
df_rdj['altmetric_datapaper_rdj'] = df_rdj['altmetric_datapaper_rdj']/df_rdj['days_since_pub_datapaper']


#Do citations/altmetric of data papers correlate with downloads of their datasets?
with open('./SSC.csv', 'w') as csvfile:
    ssc = csv.writer(csvfile)
    ssc.writerow(["variable1", "variable2", "rho", "p-value"])
    
    #Do citations/altmetric of data papers correlate with downloads of their datasets?

    #Altmetric-downloads
    df2 = df.dropna(subset=['altmetric_datapaper_johd'])
    df2 = df2.dropna(subset=['downloads_dataset_johd'])
    corr, p_value = spearmanr(df2['altmetric_datapaper_johd'], df2['downloads_dataset_johd'])
    ssc.writerow(['altmetric_datapaper_johd','downloads_dataset_johd',corr,p_value])

    #Citations-downloads
    df2 = df.dropna(subset=['tot_citations_datapaper_johd'])
    df2 = df2.dropna(subset=['downloads_dataset_johd'])
    corr, p_value = spearmanr(df2['tot_citations_datapaper_johd'], df2['downloads_dataset_johd'])
    ssc.writerow(['tot_citations_datapaper_johd','downloads_dataset_johd',corr,p_value])


    #Do citations/altmetric of data papers correlate with citations/altmetrics of their research papers?

    #Citations-citations
    df2 = df.dropna(subset=['tot_citations_research_johd'])
    df2 = df2.dropna(subset=['tot_citations_datapaper_johd'])
    df2 = df2.dropna(subset=['date_research_johd'])
    df2['date_research_johd'] = [datetime.strptime(str(x), date_format) for x in df2['date_research_johd']]
    df2['days_since_pub_research'] = df2['data_collection_date'] - df2['date_research_johd']
    df2['days_since_pub_research'] = [x.days for x in df2['days_since_pub_research']]
    df2['tot_citations_research_johd'] = df2['tot_citations_research_johd']/df2['days_since_pub_research']
    corr, p_value = spearmanr(df2['tot_citations_research_johd'], df2['tot_citations_datapaper_johd'])
    ssc.writerow(['tot_citations_research_johd','tot_citations_datapaper_johd',corr,p_value])

    #Citations-altmetric
    df2 = df.dropna(subset=['tot_citations_research_johd'])
    df2 = df2.dropna(subset=['altmetric_datapaper_johd'])
    df2 = df2.dropna(subset=['date_research_johd'])
    df2['date_research_johd'] = [datetime.strptime(str(x), date_format) for x in df2['date_research_johd']]
    df2['days_since_pub_research'] = df2['data_collection_date'] - df2['date_research_johd']
    df2['days_since_pub_research'] = [x.days for x in df2['days_since_pub_research']]
    df2['tot_citations_research_johd'] = df2['tot_citations_research_johd']/df2['days_since_pub_research']
    corr, p_value = spearmanr(df2['tot_citations_research_johd'], df2['altmetric_datapaper_johd'])
    ssc.writerow(['tot_citations_research_johd','altmetric_datapaper_johd',corr,p_value])

    #Citations-tweets
    df2 = df.dropna(subset=['tot_citations_research_johd'])
    df2 = df2.dropna(subset=['tweets_datapaper'])
    df2 = df2.dropna(subset=['date_research_johd'])
    df2['date_research_johd'] = [datetime.strptime(str(x), date_format) for x in df2['date_research_johd']]
    df2['days_since_pub_research'] = df2['data_collection_date'] - df2['date_research_johd']
    df2['days_since_pub_research'] = [x.days for x in df2['days_since_pub_research']]
    df2['tot_citations_research_johd'] = df2['tot_citations_research_johd']/df2['days_since_pub_research']
    corr, p_value = spearmanr(df2['tot_citations_research_johd'], df2['tweets_datapaper'])
    ssc.writerow(['tot_citations_research_johd','tweets_datapaper',corr,p_value])

    #Citations-views
    df2 = df.dropna(subset=['tot_citations_research_johd'])
    df2 = df2.dropna(subset=['views_datapaper_johd'])
    df2 = df2.dropna(subset=['date_research_johd'])
    df2['date_research_johd'] = [datetime.strptime(str(x), date_format) for x in df2['date_research_johd']]
    df2['days_since_pub_research'] = df2['data_collection_date'] - df2['date_research_johd']
    df2['days_since_pub_research'] = [x.days for x in df2['days_since_pub_research']]
    df2['tot_citations_research_johd'] = df2['tot_citations_research_johd']/df2['days_since_pub_research']
    corr, p_value = spearmanr(df2['tot_citations_research_johd'], df2['views_datapaper_johd'])
    ssc.writerow(['tot_citations_research_johd','views_datapaper_johd',corr,p_value])

    #Citations-downloads
    df2 = df.dropna(subset=['tot_citations_research_johd'])
    df2 = df2.dropna(subset=['downloads_datapaper_johd'])
    df2 = df2.dropna(subset=['date_research_johd'])
    df2['date_research_johd'] = [datetime.strptime(str(x), date_format) for x in df2['date_research_johd']]
    df2['days_since_pub_research'] = df2['data_collection_date'] - df2['date_research_johd']
    df2['days_since_pub_research'] = [x.days for x in df2['days_since_pub_research']]
    df2['tot_citations_research_johd'] = df2['tot_citations_research_johd']/df2['days_since_pub_research']
    corr, p_value = spearmanr(df2['tot_citations_research_johd'], df2['downloads_datapaper_johd'])
    ssc.writerow(['tot_citations_research_johd','downloads_datapaper_johd',corr,p_value])

    #Altmetric-citations
    df2 = df.dropna(subset=['altmetric_research_johd'])
    df2 = df2.dropna(subset=['tot_citations_datapaper_johd'])
    df2 = df2.dropna(subset=['date_research_johd'])
    df2['date_research_johd'] = [datetime.strptime(str(x), date_format) for x in df2['date_research_johd']]
    df2['days_since_pub_research'] = df2['data_collection_date'] - df2['date_research_johd']
    df2['days_since_pub_research'] = [x.days for x in df2['days_since_pub_research']]
    df2['altmetric_research_johd'] = df2['altmetric_research_johd']/df2['days_since_pub_research']
    corr, p_value = spearmanr(df2['altmetric_research_johd'], df2['tot_citations_datapaper_johd'])
    ssc.writerow(['altmetric_research_johd','tot_citations_datapaper_johd',corr,p_value])

    #Altmetric-altmetric
    df2 = df.dropna(subset=['altmetric_research_johd'])
    df2 = df2.dropna(subset=['altmetric_datapaper_johd'])
    df2 = df2.dropna(subset=['date_research_johd'])
    df2['date_research_johd'] = [datetime.strptime(str(x), date_format) for x in df2['date_research_johd']]
    df2['days_since_pub_research'] = df2['data_collection_date'] - df2['date_research_johd']
    df2['days_since_pub_research'] = [x.days for x in df2['days_since_pub_research']]
    df2['altmetric_research_johd'] = df2['altmetric_research_johd']/df2['days_since_pub_research']
    corr, p_value = spearmanr(df2['altmetric_research_johd'], df2['altmetric_datapaper_johd'])
    ssc.writerow(['altmetric_research_johd','altmetric_datapaper_johd',corr,p_value])

    #Altmetric-views
    df2 = df.dropna(subset=['altmetric_research_johd'])
    df2 = df2.dropna(subset=['views_datapaper_johd'])
    df2 = df2.dropna(subset=['date_research_johd'])
    df2['date_research_johd'] = [datetime.strptime(str(x), date_format) for x in df2['date_research_johd']]
    df2['days_since_pub_research'] = df2['data_collection_date'] - df2['date_research_johd']
    df2['days_since_pub_research'] = [x.days for x in df2['days_since_pub_research']]
    df2['altmetric_research_johd'] = df2['altmetric_research_johd']/df2['days_since_pub_research']
    corr, p_value = spearmanr(df2['altmetric_research_johd'], df2['views_datapaper_johd'])
    ssc.writerow(['altmetric_research_johd','views_datapaper_johd',corr,p_value])

    #Altmetric-downloads
    df2 = df.dropna(subset=['altmetric_research_johd'])
    df2 = df2.dropna(subset=['downloads_datapaper_johd'])
    df2 = df2.dropna(subset=['date_research_johd'])
    df2['date_research_johd'] = [datetime.strptime(str(x), date_format) for x in df2['date_research_johd']]
    df2['days_since_pub_research'] = df2['data_collection_date'] - df2['date_research_johd']
    df2['days_since_pub_research'] = [x.days for x in df2['days_since_pub_research']]
    df2['altmetric_research_johd'] = df2['altmetric_research_johd']/df2['days_since_pub_research']
    corr, p_value = spearmanr(df2['altmetric_research_johd'], df2['downloads_datapaper_johd'])
    ssc.writerow(['altmetric_research_johd','downloads_datapaper_johd',corr,p_value])

    #Altmetric-tweets
    df2 = df.dropna(subset=['altmetric_research_johd'])
    df2 = df2.dropna(subset=['tweets_datapaper'])
    df2 = df2.dropna(subset=['date_research_johd'])
    df2['date_research_johd'] = [datetime.strptime(str(x), date_format) for x in df2['date_research_johd']]
    df2['days_since_pub_research'] = df2['data_collection_date'] - df2['date_research_johd']
    df2['days_since_pub_research'] = [x.days for x in df2['days_since_pub_research']]
    df2['altmetric_research_johd'] = df2['altmetric_research_johd']/df2['days_since_pub_research']
    corr, p_value = spearmanr(df2['altmetric_research_johd'], df2['tweets_datapaper'])
    ssc.writerow(['altmetric_research_johd','tweets_datapaper',corr,p_value])

    # What about 'internal' cross-metric relations?
    #DATA PAPERS
    #Altmetric-citations
    df2 = df.dropna(subset=['altmetric_datapaper_johd'])
    df2 = df2.dropna(subset=['tot_citations_datapaper_johd'])
    corr, p_value = spearmanr(df2['altmetric_datapaper_johd'], df2['tot_citations_datapaper_johd'])
    ssc.writerow(['altmetric_datapaper_johd','tot_citations_datapaper_johd',corr,p_value])

    #Views-citations
    df2 = df.dropna(subset=['views_datapaper_johd'])
    df2 = df2.dropna(subset=['tot_citations_datapaper_johd'])
    corr, p_value = spearmanr(df2['views_datapaper_johd'], df2['tot_citations_datapaper_johd'])
    ssc.writerow(['views_datapaper_johd','tot_citations_datapaper_johd',corr,p_value])

    #Tweets-citations
    df2 = df.dropna(subset=['tweets_datapaper'])
    df2 = df2.dropna(subset=['tot_citations_datapaper_johd'])
    corr, p_value = spearmanr(df2['tweets_datapaper'], df2['tot_citations_datapaper_johd'])
    ssc.writerow(['tweets_datapaper','tot_citations_datapaper_johd',corr,p_value])

    #Altmetric-views
    df2 = df.dropna(subset=['altmetric_datapaper_johd'])
    df2 = df2.dropna(subset=['views_datapaper_johd'])
    corr, p_value = spearmanr(df2['altmetric_datapaper_johd'], df2['views_datapaper_johd'])
    ssc.writerow(['altmetric_datapaper_johd','views_datapaper_johd',corr,p_value])

    #Altmetric-downloads
    df2 = df.dropna(subset=['altmetric_datapaper_johd'])
    df2 = df2.dropna(subset=['downloads_datapaper_johd'])
    corr, p_value = spearmanr(df2['altmetric_datapaper_johd'], df2['downloads_datapaper_johd'])
    ssc.writerow(['altmetric_datapaper_johd','downloads_datapaper_johd',corr,p_value])

    #RESEARCH PAPERS
    #Altmetric-citations
    df2 = df.dropna(subset=['altmetric_research_johd'])
    df2 = df2.dropna(subset=['tot_citations_research_johd'])
    df2 = df2.dropna(subset=['date_research_johd'])
    df2['date_research_johd'] = [datetime.strptime(str(x), date_format) for x in df2['date_research_johd']]
    df2['days_since_pub_research'] = df2['data_collection_date'] - df2['date_research_johd']
    df2['days_since_pub_research'] = [x.days for x in df2['days_since_pub_research']]
    df2['altmetric_research_johd'] = df2['altmetric_research_johd']/df2['days_since_pub_research']
    df2['tot_citations_research_johd'] = df2['tot_citations_research_johd']/df2['days_since_pub_research']
    corr, p_value = spearmanr(df2['altmetric_research_johd'], df2['tot_citations_research_johd'])
    ssc.writerow(['altmetric_research_johd','tot_citations_research_johd',corr,p_value])

    #RESEARCH-DATASETS
    #Citations-downloads
    df2 = df.dropna(subset=['tot_citations_research_johd'])
    df2 = df2.dropna(subset=['downloads_dataset_johd'])
    df2 = df2.dropna(subset=['date_research_johd'])
    df2['date_research_johd'] = [datetime.strptime(str(x), date_format) for x in df2['date_research_johd']]
    df2['days_since_pub_research'] = df2['data_collection_date'] - df2['date_research_johd']
    df2['days_since_pub_research'] = [x.days for x in df2['days_since_pub_research']]
    df2['tot_citations_research_johd'] = df2['tot_citations_research_johd']/df2['days_since_pub_research']
    corr, p_value = spearmanr(df2['tot_citations_research_johd'], df2['downloads_dataset_johd'])
    ssc.writerow(['tot_citations_research_johd','downloads_dataset_johd',corr,p_value])

#     #RDJ RESEARCH - RDJ DATAPAPERS Not enough data, commented out
#     #Citations-citations
#     df_rdj2 = df_rdj.dropna(subset=['tot_citations_research_rdj'])
#     df_rdj2 = df_rdj2.dropna(subset=['tot_citations_datapaper_rdj'])
#     df_rdj2 = df_rdj2.dropna(subset=['date_research_rdj'])
#     print(df_rdj2['tot_citations_research_rdj'])
#     print(df_rdj2['tot_citations_datapaper_rdj'])
#     df_rdj2['date_research_rdj'] = [datetime.strptime(str(x), date_format) for x in df_rdj2['date_research_rdj']]
#     df_rdj2['days_since_pub_research'] = df_rdj2['data_collection_date'] - df_rdj2['date_research_rdj']
#     df_rdj2['days_since_pub_research'] = [x.days for x in df_rdj2['days_since_pub_research']]
#     df_rdj2['tot_citations_research_rdj'] = df_rdj2['tot_citations_research_rdj']/df_rdj2['days_since_pub_research']
#     corr, p_value = spearmanr(df_rdj2['tot_citations_research_rdj'], df_rdj2['tot_citations_datapaper_rdj'])
#     ssc.writerow(['tot_citations_research_rdj','tot_citations_datapaper_rdj',corr,p_value])

#     #Citations-altmetric
#     df_rdj2 = df_rdj.dropna(subset=['tot_citations_research_rdj'])
#     df_rdj2 = df_rdj2.dropna(subset=['altmetric_datapaper_rdj'])
#     df_rdj2 = df_rdj2.dropna(subset=['date_research_rdj'])
#     df_rdj2['date_research_rdj'] = [datetime.strptime(str(x), date_format) for x in df_rdj2['date_research_rdj']]
#     df_rdj2['days_since_pub_research'] = df_rdj2['data_collection_date'] - df_rdj2['date_research_rdj']
#     df_rdj2['days_since_pub_research'] = [x.days for x in df_rdj2['days_since_pub_research']]
#     df_rdj2['tot_citations_research_rdj'] = df_rdj2['tot_citations_research_rdj']/df_rdj2['days_since_pub_research']
#     corr, p_value = spearmanr(df_rdj2['tot_citations_research_rdj'], df_rdj2['altmetric_datapaper_rdj'])
#     ssc.writerow(['tot_citations_research_rdj','altmetric_datapaper_rdj',corr,p_value])

#     #Citations-views
#     df_rdj2 = df_rdj.dropna(subset=['tot_citations_research_rdj'])
#     df_rdj2 = df_rdj2.dropna(subset=['views_datapaper_rdj'])
#     df_rdj2 = df_rdj2.dropna(subset=['date_research_rdj'])
#     df_rdj2['date_research_rdj'] = [datetime.strptime(str(x), date_format) for x in df_rdj2['date_research_rdj']]
#     df_rdj2['days_since_pub_research'] = df_rdj2['data_collection_date'] - df_rdj2['date_research_rdj']
#     df_rdj2['days_since_pub_research'] = [x.days for x in df_rdj2['days_since_pub_research']]
#     df_rdj2['tot_citations_research_rdj'] = df_rdj2['tot_citations_research_rdj']/df_rdj2['days_since_pub_research']
#     corr, p_value = spearmanr(df_rdj2['tot_citations_research_rdj'], df_rdj2['views_datapaper_rdj'])
#     ssc.writerow(['tot_citations_research_rdj','views_datapaper_rdj',corr,p_value])

#     #Citations-downloads
#     df_rdj2 = df_rdj.dropna(subset=['tot_citations_research_rdj'])
#     df_rdj2 = df_rdj2.dropna(subset=['downloads_datapaper_rdj'])
#     df_rdj2 = df_rdj2.dropna(subset=['date_research_rdj'])
#     df_rdj2['date_research_rdj'] = [datetime.strptime(str(x), date_format) for x in df_rdj2['date_research_rdj']]
#     df_rdj2['days_since_pub_research'] = df_rdj2['data_collection_date'] - df_rdj2['date_research_rdj']
#     df_rdj2['days_since_pub_research'] = [x.days for x in df_rdj2['days_since_pub_research']]
#     df_rdj2['tot_citations_research_rdj'] = df_rdj2['tot_citations_research_rdj']/df_rdj2['days_since_pub_research']
#     corr, p_value = spearmanr(df_rdj2['tot_citations_research_rdj'], df_rdj2['downloads_datapaper_rdj'])
#     ssc.writerow(['tot_citations_research_rdj','downloads_datapaper_rdj',corr,p_value])

#     #Altmetric-citations
#     df_rdj2 = df_rdj.dropna(subset=['altmetric_research_rdj'])
#     df_rdj2 = df_rdj2.dropna(subset=['tot_citations_datapaper_rdj'])
#     df_rdj2 = df_rdj2.dropna(subset=['date_research_rdj'])
#     df_rdj2['date_research_rdj'] = [datetime.strptime(str(x), date_format) for x in df_rdj2['date_research_rdj']]
#     df_rdj2['days_since_pub_research'] = df_rdj2['data_collection_date'] - df_rdj2['date_research_rdj']
#     df_rdj2['days_since_pub_research'] = [x.days for x in df_rdj2['days_since_pub_research']]
#     df_rdj2['altmetric_research_rdj'] = df_rdj2['altmetric_research_rdj']/df_rdj2['days_since_pub_research']
#     corr, p_value = spearmanr(df_rdj2['altmetric_research_rdj'], df_rdj2['tot_citations_datapaper_rdj'])
#     ssc.writerow(['altmetric_research_rdj','tot_citations_datapaper_rdj',corr,p_value])

#     #Altmetric-altmetric
#     df_rdj2 = df_rdj.dropna(subset=['altmetric_research_rdj'])
#     df_rdj2 = df_rdj2.dropna(subset=['altmetric_datapaper_rdj'])
#     df_rdj2 = df_rdj2.dropna(subset=['date_research_rdj'])
#     df_rdj2['date_research_rdj'] = [datetime.strptime(str(x), date_format) for x in df_rdj2['date_research_rdj']]
#     df_rdj2['days_since_pub_research'] = df_rdj2['data_collection_date'] - df_rdj2['date_research_rdj']
#     df_rdj2['days_since_pub_research'] = [x.days for x in df_rdj2['days_since_pub_research']]
#     df_rdj2['altmetric_research_rdj'] = df_rdj2['altmetric_research_rdj']/df_rdj2['days_since_pub_research']
#     corr, p_value = spearmanr(df_rdj2['altmetric_research_rdj'], df_rdj2['altmetric_datapaper_rdj'])
#     ssc.writerow(['altmetric_research_rdj','altmetric_datapaper_rdj',corr,p_value])

#     #Altmetric-views
#     df_rdj2 = df_rdj.dropna(subset=['altmetric_research_rdj'])
#     df_rdj2 = df_rdj2.dropna(subset=['views_datapaper_rdj'])
#     df_rdj2 = df_rdj2.dropna(subset=['date_research_rdj'])
#     df_rdj2['date_research_rdj'] = [datetime.strptime(str(x), date_format) for x in df_rdj2['date_research_rdj']]
#     df_rdj2['days_since_pub_research'] = df_rdj2['data_collection_date'] - df_rdj2['date_research_rdj']
#     df_rdj2['days_since_pub_research'] = [x.days for x in df_rdj2['days_since_pub_research']]
#     df_rdj2['altmetric_research_rdj'] = df_rdj2['altmetric_research_rdj']/df_rdj2['days_since_pub_research']
#     corr, p_value = spearmanr(df_rdj2['altmetric_research_rdj'], df_rdj2['views_datapaper_rdj'])
#     ssc.writerow(['altmetric_research_rdj','views_datapaper_rdj',corr,p_value])

#     #Altmetric-downloads
#     df_rdj2 = df_rdj.dropna(subset=['altmetric_research_rdj'])
#     df_rdj2 = df_rdj2.dropna(subset=['downloads_datapaper_rdj'])
#     df_rdj2 = df_rdj2.dropna(subset=['date_research_rdj'])
#     df_rdj2['date_research_rdj'] = [datetime.strptime(str(x), date_format) for x in df_rdj2['date_research_rdj']]
#     df_rdj2['days_since_pub_research'] = df_rdj2['data_collection_date'] - df_rdj2['date_research_rdj']
#     df_rdj2['days_since_pub_research'] = [x.days for x in df_rdj2['days_since_pub_research']]
#     df_rdj2['altmetric_research_rdj'] = df_rdj2['altmetric_research_rdj']/df_rdj2['days_since_pub_research']
#     corr, p_value = spearmanr(df_rdj2['altmetric_research_rdj'], df_rdj2['downloads_datapaper_rdj'])
#     ssc.writerow(['altmetric_research_rdj','downloads_datapaper_rdj',corr,p_value])

    #RDJ INTERNAL
    #DATA PAPERS
    #Altmetric-citations
    df_rdj2 = df_rdj.dropna(subset=['altmetric_datapaper_rdj'])
    df_rdj2 = df_rdj2.dropna(subset=['tot_citations_datapaper_rdj'])
    corr, p_value = spearmanr(df_rdj2['altmetric_datapaper_rdj'], df_rdj2['tot_citations_datapaper_rdj'])
    ssc.writerow(['altmetric_datapaper_rdj','tot_citations_datapaper_rdj',corr,p_value])

    #Views-citations
    df_rdj2 = df_rdj.dropna(subset=['views_datapaper_rdj'])
    df_rdj2 = df_rdj2.dropna(subset=['tot_citations_datapaper_rdj'])
    corr, p_value = spearmanr(df_rdj2['views_datapaper_rdj'], df_rdj2['tot_citations_datapaper_rdj'])
    ssc.writerow(['views_datapaper_rdj','tot_citations_datapaper_rdj',corr,p_value])

    #Altmetric-views
    df_rdj2 = df_rdj.dropna(subset=['altmetric_datapaper_rdj'])
    df_rdj2 = df_rdj2.dropna(subset=['views_datapaper_rdj'])
    corr, p_value = spearmanr(df_rdj2['altmetric_datapaper_rdj'], df_rdj2['views_datapaper_rdj'])
    ssc.writerow(['altmetric_datapaper_rdj','views_datapaper_rdj',corr,p_value])

    #Altmetric-downloads
    df_rdj2 = df_rdj.dropna(subset=['altmetric_datapaper_rdj'])
    df_rdj2 = df_rdj2.dropna(subset=['downloads_datapaper_rdj'])
    corr, p_value = spearmanr(df_rdj2['altmetric_datapaper_rdj'], df_rdj2['downloads_datapaper_rdj'])
    ssc.writerow(['altmetric_datapaper_rdj','downloads_datapaper_rdj',corr,p_value])

    #RDJ + JOHD
    #DATA PAPERS -internal
    #Altmetric-citations
    df_rdj2 = df_rdj.dropna(subset=['altmetric_datapaper_rdj'])
    df_rdj2 = df_rdj2.dropna(subset=['tot_citations_datapaper_rdj'])
    df2 = df.dropna(subset=['altmetric_datapaper_johd'])
    df2 = df2.dropna(subset=['tot_citations_datapaper_johd'])
    newx = list(df_rdj2['altmetric_datapaper_rdj']) + list(df2['altmetric_datapaper_johd'])
    newy = list(df_rdj2['tot_citations_datapaper_rdj']) + list(df2['tot_citations_datapaper_johd'])
    corr, p_value = spearmanr(newx, newy)
    ssc.writerow(['altmetric_datapaper_all','tot_citations_datapaper_all',corr,p_value])

    #Views-citations
    df_rdj2 = df_rdj.dropna(subset=['views_datapaper_rdj'])
    df_rdj2 = df_rdj2.dropna(subset=['tot_citations_datapaper_rdj'])
    df2 = df.dropna(subset=['views_datapaper_johd'])
    df2 = df2.dropna(subset=['tot_citations_datapaper_johd'])
    newx = list(df_rdj2['views_datapaper_rdj']) + list(df2['views_datapaper_johd'])
    newy = list(df_rdj2['tot_citations_datapaper_rdj']) + list(df2['tot_citations_datapaper_johd'])
    corr, p_value = spearmanr(newx, newy)
    ssc.writerow(['views_datapaper_all','tot_citations_datapaper_all',corr,p_value])

    #Downloads-citations
    df_rdj2 = df_rdj.dropna(subset=['downloads_datapaper_rdj'])
    df_rdj2 = df_rdj2.dropna(subset=['tot_citations_datapaper_rdj'])
    df2 = df.dropna(subset=['downloads_datapaper_johd'])
    df2 = df2.dropna(subset=['tot_citations_datapaper_johd'])
    newx = list(df_rdj2['downloads_datapaper_rdj']) + list(df2['downloads_datapaper_johd'])
    newy = list(df_rdj2['tot_citations_datapaper_rdj']) + list(df2['tot_citations_datapaper_johd'])
    corr, p_value = spearmanr(newx, newy)
    ssc.writerow(['downloads_datapaper_all','tot_citations_datapaper_all',corr,p_value])

    #Altmetric-views
    df_rdj2 = df_rdj.dropna(subset=['altmetric_datapaper_rdj'])
    df_rdj2 = df_rdj2.dropna(subset=['views_datapaper_rdj'])
    df2 = df.dropna(subset=['altmetric_datapaper_johd'])
    df2 = df2.dropna(subset=['views_datapaper_johd'])
    newx = list(df_rdj2['altmetric_datapaper_rdj']) + list(df2['altmetric_datapaper_johd'])
    newy = list(df_rdj2['views_datapaper_rdj']) + list(df2['views_datapaper_johd'])
    corr, p_value = spearmanr(newx, newy)
    ssc.writerow(['views_datapaper_all','altmetric_datapaper_all',corr,p_value])

    #Altmetric-downloads
    df_rdj2 = df_rdj.dropna(subset=['altmetric_datapaper_rdj'])
    df_rdj2 = df_rdj2.dropna(subset=['downloads_datapaper_rdj'])
    df2 = df.dropna(subset=['altmetric_datapaper_johd'])
    df2 = df2.dropna(subset=['downloads_datapaper_johd'])
    newx = list(df_rdj2['altmetric_datapaper_rdj']) + list(df2['altmetric_datapaper_johd'])
    newy = list(df_rdj2['downloads_datapaper_rdj']) + list(df2['downloads_datapaper_johd'])
    corr, p_value = spearmanr(newx, newy)
    ssc.writerow(['downloads_datapaper_all','altmetric_datapaper_all',corr,p_value])

    #downloads-views
    df_rdj2 = df_rdj.dropna(subset=['views_datapaper_rdj'])
    df_rdj2 = df_rdj2.dropna(subset=['downloads_datapaper_rdj'])
    df2 = df.dropna(subset=['views_datapaper_johd'])
    df2 = df2.dropna(subset=['downloads_datapaper_johd'])
    newx = list(df_rdj2['views_datapaper_rdj']) + list(df2['views_datapaper_johd'])
    newy = list(df_rdj2['downloads_datapaper_rdj']) + list(df2['downloads_datapaper_johd'])
    corr, p_value = spearmanr(newx, newy)
    ssc.writerow(['views_datapaper_all','downloads_datapaper_all',corr,p_value])

    ## RDJ + JOHD
    ## RESEARCH - DATAPAPER
    #citations-citations
    df_rdj2 = df_rdj.dropna(subset=['tot_citations_datapaper_rdj'])
    df_rdj2 = df_rdj2.dropna(subset=['tot_citations_research_rdj'])
    df2 = df.dropna(subset=['tot_citations_datapaper_johd'])
    df2 = df2.dropna(subset=['tot_citations_research_johd'])
    newx = list(df_rdj2['tot_citations_datapaper_rdj']) + list(df2['tot_citations_datapaper_johd'])
    newy = list(df_rdj2['tot_citations_research_rdj']) + list(df2['tot_citations_research_johd'])
    corr, p_value = spearmanr(newx, newy)
    ssc.writerow(['tot_citations_research_all','tot_citations_datapaper_all',corr,p_value])

    #Altmetric-Altmetric
    df_rdj2 = df_rdj.dropna(subset=['altmetric_research_rdj'])
    df_rdj2 = df_rdj2.dropna(subset=['altmetric_datapaper_rdj'])
    df2 = df.dropna(subset=['altmetric_research_johd'])
    df2 = df2.dropna(subset=['altmetric_datapaper_johd'])
    newx = list(df_rdj2['altmetric_research_rdj']) + list(df2['altmetric_research_johd'])
    newy = list(df_rdj2['altmetric_datapaper_rdj']) + list(df2['altmetric_datapaper_johd'])
    corr, p_value = spearmanr(newx, newy)
    ssc.writerow(['altmetric_research_all','tot_citations_datapaper_all',corr,p_value])

    #citations-Altmetric
    df_rdj2 = df_rdj.dropna(subset=['altmetric_research_rdj'])
    df_rdj2 = df_rdj2.dropna(subset=['tot_citations_datapaper_rdj'])
    df2 = df.dropna(subset=['altmetric_research_johd'])
    df2 = df2.dropna(subset=['tot_citations_datapaper_johd'])
    newx = list(df_rdj2['altmetric_research_rdj']) + list(df2['altmetric_research_johd'])
    newy = list(df_rdj2['tot_citations_datapaper_rdj']) + list(df2['tot_citations_datapaper_johd'])
    corr, p_value = spearmanr(newx, newy)
    ssc.writerow(['altmetric_research_all','tot_citations_datapaper_all',corr,p_value])

    #Altmetric-citations
    df_rdj2 = df_rdj.dropna(subset=['altmetric_datapaper_rdj'])
    df_rdj2 = df_rdj2.dropna(subset=['tot_citations_research_rdj'])
    df2 = df.dropna(subset=['altmetric_datapaper_johd'])
    df2 = df2.dropna(subset=['tot_citations_research_johd'])
    newx = list(df_rdj2['altmetric_datapaper_rdj']) + list(df2['altmetric_datapaper_johd'])
    newy = list(df_rdj2['tot_citations_research_rdj']) + list(df2['tot_citations_research_johd'])
    corr, p_value = spearmanr(newx, newy)
    ssc.writerow(['altmetric_datapaper_all','tot_citations_research_all',corr,p_value])

    #Views-citations
    df_rdj2 = df_rdj.dropna(subset=['views_datapaper_rdj'])
    df_rdj2 = df_rdj2.dropna(subset=['tot_citations_research_rdj'])
    df2 = df.dropna(subset=['views_datapaper_johd'])
    df2 = df2.dropna(subset=['tot_citations_research_johd'])
    newx = list(df_rdj2['views_datapaper_rdj']) + list(df2['views_datapaper_johd'])
    newy = list(df_rdj2['tot_citations_research_rdj']) + list(df2['tot_citations_research_johd'])
    corr, p_value = spearmanr(newx, newy)
    ssc.writerow(['views_datapaper_all','tot_citations_research_all',corr,p_value])

    #Downloads-citations
    df_rdj2 = df_rdj.dropna(subset=['downloads_datapaper_rdj'])
    df_rdj2 = df_rdj2.dropna(subset=['tot_citations_research_rdj'])
    df2 = df.dropna(subset=['downloads_datapaper_johd'])
    df2 = df2.dropna(subset=['tot_citations_research_johd'])
    newx = list(df_rdj2['downloads_datapaper_rdj']) + list(df2['downloads_datapaper_johd'])
    newy = list(df_rdj2['tot_citations_research_rdj']) + list(df2['tot_citations_research_johd'])
    corr, p_value = spearmanr(newx, newy)
    ssc.writerow(['downloads_datapaper_all','tot_citations_research_all',corr,p_value])

    #views-altmetric
    df_rdj2 = df_rdj.dropna(subset=['altmetric_research_rdj'])
    df_rdj2 = df_rdj2.dropna(subset=['views_datapaper_rdj'])
    df2 = df.dropna(subset=['altmetric_research_johd'])
    df2 = df2.dropna(subset=['views_datapaper_johd'])
    newx = list(df_rdj2['altmetric_research_rdj']) + list(df2['altmetric_research_johd'])
    newy = list(df_rdj2['views_datapaper_rdj']) + list(df2['views_datapaper_johd'])
    corr, p_value = spearmanr(newx, newy)
    ssc.writerow(['views_datapaper_all','altmetric_research_all',corr,p_value])

    #downloads-altmetric
    df_rdj2 = df_rdj.dropna(subset=['altmetric_research_rdj'])
    df_rdj2 = df_rdj2.dropna(subset=['downloads_datapaper_rdj'])
    df2 = df.dropna(subset=['altmetric_research_johd'])
    df2 = df2.dropna(subset=['downloads_datapaper_johd'])
    newx = list(df_rdj2['altmetric_research_rdj']) + list(df2['altmetric_research_johd'])
    newy = list(df_rdj2['downloads_datapaper_rdj']) + list(df2['downloads_datapaper_johd'])
    corr, p_value = spearmanr(newx, newy)
    ssc.writerow(['downloads_datapaper_all','altmetric_research_all',corr,p_value])

newdf = pd.read_csv('./SSC.csv')
strength = []
significance = []

# Following Dancey & Reidy 2007 (Psychology) for interpreting strength of correlation
for rho in newdf['rho']:
        if rho == 1 or rho == -1:
                strength.append('Perfect')
        elif 1 > rho >= 0.7 or -1 < rho <= -0.7:
                strength.append('Strong')
        elif 0.7 > rho >= 0.4 or -0.7 < rho <= -0.4:
                strength.append('Moderate')
        elif 0.4 > rho >= 0.1 or -0.4 < rho <= -0.1:
                strength.append('Weak')
        elif 0.1 > rho > -0.1:
                strength.append('Weak')
        elif rho == 0:
                strength.append('Zero')
        else:
                strength.append('NA')

for p in newdf['p-value']:
        if p <= 0.05:
                significance.append('Significative')
        elif 0.05 < p <= 0.07:
                significance.append('Borderline') # Can be considered a trend
        else:
                significance.append('Not significative')

newdf['Strength of correlation'] = strength
newdf['Significative?'] = significance

newdf.to_csv('./outputs/analysis_outputs/{}-correlations.csv'.format(dateoflastdf),index=False)