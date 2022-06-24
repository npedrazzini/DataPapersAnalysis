#Do datasets that we know have data paper associated get higher downloads/views than datasets overall? 
#Binomial test/proportion test between distribution of downloads of all datasets vs distribution of downloads of datasets in our df

from statistics import mean, stdev
import pandas as pd
from scipy import stats
import random
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import itertools
import csv

dateoflastdf = '2022-06-04' # change to date of last export

zenodos = pd.read_csv('./zenodo_dimensions_all_humss/zenodo_humss_datasets.csv',usecols=['downloads','views','publication_date','days_since_publication'])
withdatapapers = pd.read_csv('./outputs/final_outputs/johd/{}-final-datasets-johd.csv'.format(dateoflastdf),usecols=['views','downloads','date'])

date_format = "%Y-%m-%d"

zenodos = zenodos.dropna(subset=['publication_date'])
withdatapapers = withdatapapers.dropna(subset=['date'])

#NORMALIZATION
zenodos['date'] = [datetime.strptime(str(x), date_format) for x in zenodos['publication_date']]
withdatapapers['date'] = [datetime.strptime(str(x), date_format) for x in withdatapapers['date']]

# Dates when data was collected is different for the 2 dfs
dateextr = datetime.strptime(dateoflastdf, date_format)

# Calculate days since publication

zenodos = zenodos.dropna(subset=['downloads'])
zenodos = zenodos.dropna(subset=['views'])
withdatapapers = withdatapapers.dropna(subset=['downloads'])
withdatapapers = withdatapapers.dropna(subset=['views'])
withdatapapers['days_since_pub'] = dateextr - withdatapapers['date']
withdatapapers['days_since_pub'] = [x.days for x in withdatapapers['days_since_pub']]
zenodos['days_since_pub'] = dateextr - zenodos['date']
zenodos['days_since_pub'] = [x.days for x in zenodos['days_since_pub']]

# Remove outliers
q1, q3= np.percentile(sorted(zenodos['downloads']),[25,75])
iqr = q3 - q1
lower_bound_citations = q1 -(1.5 * iqr) 
upper_bound_citations = q3 +(1.5 * iqr) 
outlier_max_citations = upper_bound_citations         # Set the outlier threshold (max)
outlier_min_citations = lower_bound_citations             # Set the outlier threshold (min)
print('Downloads Zenodo lower limit: ',outlier_min_citations)
print('Downloads Zenodo upper limit: ',outlier_max_citations)
zenodos  = zenodos.loc[(zenodos['downloads'] <= outlier_max_citations) & (zenodos['downloads'] >= outlier_min_citations)] 

# Remove outliers
q1, q3= np.percentile(sorted(zenodos['views']),[25,75])
iqr = q3 - q1
lower_bound_citations = q1 -(1.5 * iqr) 
upper_bound_citations = q3 +(1.5 * iqr) 
outlier_max_citations = upper_bound_citations         # Set the outlier threshold (max)
outlier_min_citations = lower_bound_citations             # Set the outlier threshold (min)
print('views Zenodo lower limit: ',outlier_min_citations)
print('views Zenodo upper limit: ',outlier_max_citations)
zenodos  = zenodos.loc[(zenodos['views'] <= outlier_max_citations) & (zenodos['views'] >= outlier_min_citations)] 

# Remove outliers
q1, q3= np.percentile(sorted(withdatapapers['downloads']),[25,75])
iqr = q3 - q1
lower_bound_citations = q1 -(1.5 * iqr) 
upper_bound_citations = q3 +(1.5 * iqr) 
outlier_max_citations = upper_bound_citations         # Set the outlier threshold (max)
outlier_min_citations = lower_bound_citations             # Set the outlier threshold (min)
print('views JOHD datasets lower limit: ',outlier_min_citations)
print('views JOHD datasets upper limit: ',outlier_max_citations)
withdatapapers  = withdatapapers.loc[(withdatapapers['downloads'] <= outlier_max_citations) & (withdatapapers['downloads'] >= outlier_min_citations)] 

# Remove outliers
q1, q3= np.percentile(sorted(withdatapapers['views']),[25,75])
iqr = q3 - q1
lower_bound_citations = q1 -(1.5 * iqr) 
upper_bound_citations = q3 +(1.5 * iqr) 
outlier_max_citations = upper_bound_citations         # Set the outlier threshold (max)
outlier_min_citations = lower_bound_citations             # Set the outlier threshold (min)
print('views JOHD datasets lower limit: ',outlier_min_citations)
print('views JOHD datasets upper limit: ',outlier_max_citations)
withdatapapers  = withdatapapers.loc[(withdatapapers['views'] <= outlier_max_citations) & (withdatapapers['views'] >= outlier_min_citations)] 



# Normalize
zenodos['downloads'] = zenodos['downloads']/zenodos['days_since_pub']
withdatapapers['downloads'] = withdatapapers['downloads']/withdatapapers['days_since_pub']
zenodos['views'] = zenodos['views']/zenodos['days_since_pub']
withdatapapers['views'] = withdatapapers['views']/withdatapapers['days_since_pub']

zenodos = zenodos.replace([np.inf, -np.inf], 0)

##VIEWS
# Take 5000 random values from research paper to check normality of distribution (shapiro can't be done with n>5000)
#10-fold random sampling
with open('./outputs/analysis_outputs/{}-means-downloads-analysis-C.csv'.format(dateoflastdf), 'w') as outcsv:
    outcsv = csv.writer(outcsv, delimiter=',')
    outcsv.writerow(['variable1','variable2','mean_variable1','mean_variable2','welchs_stats','welchs_pvalue','mannwhit_stats','mannwhit_pvalue'])
    for _ in itertools.repeat(None, 10):
        zenodos = zenodos.dropna(subset=['downloads'])
        withdatapapers = withdatapapers.dropna(subset=['downloads'])
        print(zenodos['downloads'])

        y = random.sample(sorted(list(zenodos['downloads'])), 5000)
        
        all_zenodo_downloads_mean = mean(y)
        datasets_withDP_downloads_mean = mean(withdatapapers['downloads'])

        welchs_stats_downloads, welchs_p_downloads = stats.ttest_ind(withdatapapers['downloads'], y, equal_var = False)
        mannwhit_stats_downloads, mannwhit_p_downloads = stats.mannwhitneyu(withdatapapers['downloads'], y)
        
        outcsv.writerow(['all_zenodo_downloads','datasets_withDP_downloads',all_zenodo_downloads_mean,datasets_withDP_downloads_mean,welchs_stats_downloads,welchs_p_downloads,mannwhit_stats_downloads,mannwhit_p_downloads])

with open('./outputs/analysis_outputs/{}-means-views-analysis-C.csv'.format(dateoflastdf), 'w') as outcsv:
    outcsv = csv.writer(outcsv, delimiter=',')
    outcsv.writerow(['variable1','variable2','mean_variable1','mean_variable2','welchs_stats','welchs_pvalue','mannwhit_stats','mannwhit_pvalue'])
    for _ in itertools.repeat(None, 10):
        x = random.sample(sorted(list(zenodos['views'])), 5000)
        all_zenodo_views_mean = mean(x)
        datasets_withDP_views_mean = mean(withdatapapers['views'])

        welchs_stats_views, welchs_p_views = stats.ttest_ind(withdatapapers['views'], x, equal_var = False)
        mannwhit_stats_views, mannwhit_p_views = stats.mannwhitneyu(withdatapapers['views'], x)
        
        outcsv.writerow(['all_zenodo_views','datasets_withDP_views',all_zenodo_views_mean,datasets_withDP_views_mean,welchs_stats_views,welchs_p_views,mannwhit_stats_views,mannwhit_p_views])

#Visualize boxplots
zenodo2 = pd.DataFrame({'downloads': x, 'views': y})

array1 = [zenodo2['downloads'],withdatapapers['downloads']]
plt.boxplot(array1)
# plt.ylim(bottom_value,top_value)
plt.title('Difference in means: downloads all Hum. datasets/downloads datasets with data paper')
plt.show()

array1 = [zenodo2['views'],withdatapapers['views']]
plt.boxplot(array1)
# plt.ylim(bottom_value,top_value)
plt.title('Difference in means: views all Hum. datasets/views datasets with data paper')
plt.show()
