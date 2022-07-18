#### Twitter data analysis: 
#### does mentioning a paper in a campaign or announcing its publication on Twitter have a positive impact on the visibility of the paper? We propose an analysis of the two hashtags #showmeyourdata and #johdpapers, to spot the difference (if any) between the two strategies ###########

import pandas as pd
from datetime import datetime
import functools as ft
import scipy.stats as stats
import statistics
import csv


dateoflastdf = '2022-06-04' # change to date of last export

johd_show = pd.read_csv('./twitter_analysis/metrics_by_hashtag/johd_show.csv'.format(dateoflastdf)) #metrics about the papers in #showmeyourdata

johd_not_show = pd.read_csv('./twitter_analysis/metrics_by_hashtag/johd_not_show.csv'.format(dateoflastdf)) #metrics about the papers NOT in #showmeyourdata                           
                            
johd_tweeted = pd.read_csv('./twitter_analysis/metrics_by_hashtag/johd_tweeted.csv'.format(dateoflastdf))  #metrics about the papers in #johdpapers

johd_not_tweeted = pd.read_csv('./twitter_analysis/metrics_by_hashtag/johd_not_tweeted.csv'.format(dateoflastdf))  #metrics about the papers NOT in #johdpapers

#rename columns
johd_show = johd_show.rename(columns={"date": "date_show","views": "views_show", "downloads": "downloads_show","tweets": "tweets_show", "Times cited": "tot_citations_show","Recent citations": "rec_citations_show"})

johd_not_show = johd_not_show.rename(columns={"date": "date_not_show","views": "views_not_show", "downloads": "downloads_not_show","tweets": "tweets_not_show", "Times cited": "tot_citations_not_show","Recent citations": "rec_citations_not_show"})

johd_tweeted = johd_tweeted.rename(columns={"date": "date_tweeted","views": "views_tweeted", "downloads": "downloads_tweeted", "Times cited": "tot_citations_tweeted","Recent citations": "rec_citations_tweeted"})

johd_not_tweeted = johd_not_tweeted.rename(columns={"date": "date_not_tweeted","views": "views_not_tweeted", "downloads": "downloads_not_tweeted", "Times cited": "tot_citations_not_tweeted","Recent citations": "rec_citations_not_tweeted"})

# print(johd_not_show)
# johd_not_show.to_csv("/home/sitel/Bureau/johd_not_show.csv")

#### NORMALISATION ##############
############ normalise metrics by date of publication of the paper ##############
date_format = "%Y-%m-%d"

########## for #showmeyourdata ##################### 

df1 = [johd_show]
df1 = ft.reduce(lambda left, right: pd.merge(left, right, on='DOI'), df1)
df1['data_collection_date'] = [datetime.strptime(x, date_format) for x in df1['data_collection_date']]
df1 = df1[df1['date_show'].notna()]

df1['date_show'] = [datetime.strptime(str(x), date_format) for x in df1['date_show']]
df1['days_since_pub_show'] = df1['data_collection_date'] - df1['date_show']
df1['days_since_pub_show'] = [x.days for x in df1['days_since_pub_show']]

df1['downloads_show'] = df1['downloads_show']/df1['days_since_pub_show']
df1['views_show'] = df1['views_show']/df1['days_since_pub_show']
df1['tot_citations_show'] = df1['tot_citations_show']/df1['days_since_pub_show']
df1['rec_citations_show'] = df1['rec_citations_show']/df1['days_since_pub_show']

df1.to_csv("/home/sitel/Bureau/johd_show.csv")

df = [johd_not_show]
df = ft.reduce(lambda left, right: pd.merge(left, right, on='DOI'), df)
df['data_collection_date'] = [datetime.strptime(x, date_format) for x in df['data_collection_date']]
df = df[df['date_not_show'].notna()]

df['date_not_show'] = [datetime.strptime(str(x), date_format) for x in df['date_not_show']]
df['days_since_pub_not_show'] = df['data_collection_date'] - df['date_not_show']
df['days_since_pub_not_show'] = [x.days for x in df['days_since_pub_not_show']]

df['downloads_not_show'] = df['downloads_not_show']/df['days_since_pub_not_show']
df['views_not_show'] = df['views_not_show']/df['days_since_pub_not_show']
df['tot_citations_not_show'] = df['tot_citations_not_show']/df['days_since_pub_not_show']
df['rec_citations_not_show'] = df['rec_citations_not_show']/df['days_since_pub_not_show']


df.to_csv("/home/sitel/Bureau/johd_not_show.csv")

############ for #johdpapers ##########################################

df_tweeted = [johd_tweeted]
df_tweeted = ft.reduce(lambda left, right: pd.merge(left, right, on='DOI'), df_tweeted)
df_tweeted['data_collection_date'] = [datetime.strptime(x, date_format) for x in df_tweeted['data_collection_date']]
df_tweeted = df_tweeted[df_tweeted['date_tweeted'].notna()]

df_tweeted['date_tweeted'] = [datetime.strptime(str(x), date_format) for x in df_tweeted['date_tweeted']]
df_tweeted['days_since_pub_tweeted'] = df_tweeted['data_collection_date'] - df_tweeted['date_tweeted']
df_tweeted['days_since_pub_tweeted'] = [x.days for x in df_tweeted['days_since_pub_tweeted']]

df_tweeted['downloads_tweeted'] = df_tweeted['downloads_tweeted']/df_tweeted['days_since_pub_tweeted']
df_tweeted['views_tweeted'] = df_tweeted['views_tweeted']/df_tweeted['days_since_pub_tweeted']
df_tweeted['tot_citations_tweeted'] = df_tweeted['tot_citations_tweeted']/df_tweeted['days_since_pub_tweeted']
df_tweeted['rec_citations_tweeted'] = df_tweeted['rec_citations_tweeted']/df_tweeted['days_since_pub_tweeted']

df_tweeted.to_csv("/home/sitel/Bureau/johd_tweeted.csv")

df_not_tweeted = [johd_not_tweeted]
df_not_tweeted = ft.reduce(lambda left, right: pd.merge(left, right, on='DOI'), df_not_tweeted)
df_not_tweeted['data_collection_date'] = [datetime.strptime(x, date_format) for x in df_not_tweeted['data_collection_date']]
df_not_tweeted = df_not_tweeted[df_not_tweeted['date_not_tweeted'].notna()]

df_not_tweeted['date_not_tweeted'] = [datetime.strptime(str(x), date_format) for x in df_not_tweeted['date_not_tweeted']]
df_not_tweeted['days_since_pub_not_tweeted'] = df_not_tweeted['data_collection_date'] - df_not_tweeted['date_not_tweeted']
df_not_tweeted['days_since_pub_not_tweeted'] = [x.days for x in df_not_tweeted['days_since_pub_not_tweeted']]

df_not_tweeted['downloads_not_tweeted'] = df_not_tweeted['downloads_not_tweeted']/df_not_tweeted['days_since_pub_not_tweeted']
df_not_tweeted['views_not_tweeted'] = df_not_tweeted['views_not_tweeted']/df_not_tweeted['days_since_pub_not_tweeted']
df_not_tweeted['tot_citations_not_tweeted'] = df_not_tweeted['tot_citations_not_tweeted']/df_not_tweeted['days_since_pub_not_tweeted']
df_not_tweeted['rec_citations_not_tweeted'] = df_not_tweeted['rec_citations_not_tweeted']/df_not_tweeted['days_since_pub_not_tweeted']

df_not_tweeted.to_csv("/home/sitel/Bureau/johd_not_tweeted.csv")


#################   ANALYSIS    ################
#Is there a statistically significant difference between papers somehow mentioned on our Twitter account and papers that were not?
# -> Welch's test

with open('./SSC.csv', 'w') as csvfile:
    ssc = csv.writer(csvfile)
    ssc.writerow(["variable1", "variable2", "mean difference", "t-test", "p-value"])
    
  #first check with papers that participated in #showmeyourdata campaign vs papers that did not participate

    statistic, pvalue = stats.ttest_ind(df1['downloads_show'], df['downloads_not_show'], equal_var= False)
    mean_diff = statistics.mean(df1['downloads_show']) - statistics.mean(df['downloads_not_show'])
    print(statistics.mean(df1['downloads_show']))
    print(statistics.mean(df['downloads_not_show']))
    ssc.writerow(['downloads_show','downloads_not_show',mean_diff,statistic,pvalue])
    
    
    statistic, pvalue = stats.ttest_ind(df1['views_show'], df['views_not_show'], equal_var= False)
    mean_diff = statistics.mean(df1['views_show']) - statistics.mean(df['views_not_show'])
    print(statistics.mean(df1['views_show']))
    print(statistics.mean(df['views_not_show']))
    ssc.writerow(['views_show','views_not_show',mean_diff,statistic,pvalue])
    
    statistic, pvalue = stats.ttest_ind(df1['tot_citations_show'], df['tot_citations_not_show'], equal_var= False)
    mean_diff = statistics.mean(df1['tot_citations_show']) - statistics.mean(df['tot_citations_not_show'])
    print(statistics.mean(df1['tot_citations_show']))
    print(statistics.mean(df['tot_citations_not_show']))
    ssc.writerow(['tot_citations_show','tot_citations_not_show',mean_diff,statistic,pvalue])
    
   # #now check with papers that were announced by JOHD and papers that were not (#johdpapers) 
   
    statistic, pvalue = stats.ttest_ind(df_tweeted['downloads_tweeted'], df_not_tweeted['downloads_not_tweeted'], equal_var= False)
    mean_diff = statistics.mean(df_tweeted['downloads_tweeted']) - statistics.mean(df_not_tweeted['downloads_not_tweeted'])
    print(statistics.mean(df_tweeted['downloads_tweeted']))
    print(statistics.mean(df_not_tweeted['downloads_not_tweeted']))
    ssc.writerow(['downloads_tweeted','downloads_not_tweeted',mean_diff,statistic,pvalue])

    statistic, pvalue = stats.ttest_ind(df_tweeted['views_tweeted'], df_not_tweeted['views_not_tweeted'], equal_var= False)
    mean_diff = statistics.mean(df_tweeted['views_tweeted']) - statistics.mean(df_not_tweeted['views_not_tweeted'])
    print(statistics.mean(df_tweeted['views_tweeted']))
    print(statistics.mean(df_not_tweeted['views_not_tweeted']))
    ssc.writerow(['views_tweeted','views_not_tweeted',mean_diff,statistic,pvalue])

    statistic, pvalue = stats.ttest_ind(df_tweeted['tot_citations_tweeted'], df_not_tweeted['tot_citations_not_tweeted'], equal_var= False)
    mean_diff = statistics.mean(df_tweeted['tot_citations_tweeted']) - statistics.mean(df_not_tweeted['tot_citations_not_tweeted'])
    print(statistics.mean(df_tweeted['tot_citations_tweeted']))
    print(statistics.mean(df_not_tweeted['tot_citations_not_tweeted']))
    ssc.writerow(["tot_citations_tweeted","tot_citations_not_tweeted",mean_diff,statistic,pvalue])


newdf = pd.read_csv('./SSC.csv')
significance = []

for p in newdf['p-value']:
        if p <= 0.05:
                significance.append('Significative')
        elif 0.05 < p <= 0.07:
                significance.append('Borderline') # Can be considered a trend
        else:
                significance.append('Not significative')


newdf['Significative?'] = significance

newdf.to_csv('./twitter_analysis/welchs_analysis/welchs_results.csv'.format(dateoflastdf),index=False)
