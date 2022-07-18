# Visualize age of publication (x-axis) and n of citations/Altmetric score of all Humanities
# research papers in Dimensions (2015-2022)
# Author: Marton Ribary

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

data_collection_date = '2022-06-04' # change to date of last export

df = pd.read_csv('./dimensions_humss_research.csv')

# Drop any duplicate entry
df = df.drop_duplicates('Publication ID', keep='last')

# Change to more intuitive column names 
df = df.rename(columns={"Publication Date (online)": "date_of_publication", 'Times cited': 'tot_citations', 'Altmetric': 'altmetric'})

date_format = "%Y-%m-%d"

df = df[df['date_of_publication'].notna()]
df['date_of_publication'] = [str(x) + '-15' if len(str(x)) == 7 else x for x in df['date_of_publication']]
df = df[df['date_of_publication'].str.len()==10]

df = df[df['tot_citations'].notna()]
df = df[df['tot_citations'] != 0]
df = df[df['altmetric'].notna()]

# Exclude pub date beyond 'data_collection_date' and before first publication by JOHD

df['date_of_publication'] = [datetime.strptime(str(x), date_format) for x in df['date_of_publication']]
data_collection_date= datetime.strptime(data_collection_date, date_format)
df['days_since_publication'] = (data_collection_date - df['date_of_publication'])
df['days_since_publication'] = [x.days for x in df['days_since_publication']]

mask = (df['date_of_publication'] > '2015-09-1')
mask2 = (df['date_of_publication'] < data_collection_date)
df = df.loc[mask]
df = df.loc[mask2]

#IQR --> points which fall more than 1.5 times the interquartile range above the third quartile or below the first quartile.
q1, q3= np.percentile(sorted(df['tot_citations']),[25,75])
iqr = q3 - q1
lower_bound_citations = q1 -(1.5 * iqr) 
upper_bound_citations = q3 +(1.5 * iqr) 

q1, q3= np.percentile(sorted(df['altmetric']),[25,75])
iqr = q3 - q1
lower_bound_altmetric = q1 -(1.5 * iqr) 
upper_bound_altmetric = q3 +(1.5 * iqr) 

# Remove outliers
outlier_max_citations = upper_bound_citations         # Set the outlier threshold (max)
outlier_min_citations = lower_bound_citations             # Set the outlier threshold (min)
outlier_max_altmetric = upper_bound_altmetric      # Set the outlier threshold (max)
outlier_min_altmetric = lower_bound_altmetric           # Set the outlier threshold (min)

print('Citations lower limit: ',outlier_min_citations)
print('Citations upper limit: ',outlier_max_citations)

print('Altmetric lower limit: ',outlier_min_altmetric)
print('Altmetric upper limit: ',outlier_max_altmetric)

df  = df.loc[(df['altmetric'] <= outlier_max_altmetric) \
    & (df['tot_citations'] <= outlier_max_citations) & (df['altmetric'] >= outlier_min_altmetric) \
    & (df['tot_citations'] >= outlier_min_citations)] 

# Replace downloads and views with time-normalised data
# Skip this cell if you want to work with total counts
# df['tot_citations'] = df['tot_citations']/df['days_since_publication']
# df['altmetric'] = df['altmetric']/df['days_since_publication']

print(df['date_of_publication'])
# Create dataframe with daily averages and remove outliers
days_since_publication = df['days_since_publication'].unique()
altmetric = []
tot_citations = []
for day in days_since_publication:
    mean_citations = df['altmetric'][df['days_since_publication'] == day].mean()
    mean_altmetric = df['tot_citations'][df['days_since_publication'] == day].mean()
    altmetric.append(mean_altmetric)
    tot_citations.append(mean_citations)
df_means = pd.DataFrame({'days_since_publication': days_since_publication, \
    'mean_citations': tot_citations, 'mean_altmetric': altmetric})

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
df_means_period = pd.DataFrame({'less_than_n_days_since_publication': periods, \
    'monthly_mean_citations': p_citations, 'monthly_mean_altmetric': p_altmetric})
df_means_period = df_means_period.sort_values(by='less_than_n_days_since_publication', ascending=False)

df_means_period['less_than_n_days_since_publication'] = [x/365 for x in df_means_period['less_than_n_days_since_publication']]

# Plot 90-day averages for views and downloads
# Views
#remove top citation and altmetric
df_means_period = df_means_period[df_means_period['monthly_mean_citations'] != max(df_means_period['monthly_mean_citations'])]
df_means_period = df_means_period[df_means_period['monthly_mean_altmetric'] != max(df_means_period['monthly_mean_altmetric'])]

x = np.array(df_means_period['less_than_n_days_since_publication'])
y = np.array(df_means_period['monthly_mean_altmetric'])
plt.scatter(x,y,label='Altmetric')

# Downlaods
x = np.array(df_means_period['less_than_n_days_since_publication'])
y = np.array(df_means_period['monthly_mean_citations'])
plt.scatter(x,y,label='Citations')
plt.legend()
plt.xlabel('Years')
plt.ylabel('Age-normalised counts')
plt.grid(axis='y', alpha=0.75)
# plt.savefig("./outputs/figures/figureB12-dev-cit-alt-dims.jpeg",dpi=300)
plt.show()




df = df[df['tot_citations'].notna()]
df3 = list(df['tot_citations'])

df = df[df['altmetric'].notna()]
df4 = list(df['altmetric'])


bp = plt.boxplot([df3,df4], showmeans=True)    
medians = [round(item.get_ydata()[0], 1) for item in bp['medians']]
means = [round(item.get_ydata()[0], 1) for item in bp['means']]
minimums = [round(item.get_ydata()[0], 1) for item in bp['caps']][::2]
maximums = [round(item.get_ydata()[0], 1) for item in bp['caps']][1::2]
q1 = [round(min(item.get_ydata()), 1) for item in bp['boxes']]
q3 = [round(max(item.get_ydata()), 1) for item in bp['boxes']]
fliers = [item.get_ydata() for item in bp['fliers']]
lower_outliers = []
upper_outliers = []
for i in range(len(fliers)):
    lower_outliers_by_box = []
    upper_outliers_by_box = []
    for outlier in fliers[i]:
        if outlier < q1[i]:
            lower_outliers_by_box.append(round(outlier, 1))
        else:
            upper_outliers_by_box.append(round(outlier, 1))
    lower_outliers.append(lower_outliers_by_box)
    upper_outliers.append(upper_outliers_by_box)    
    
# New code
stats = [medians, means, minimums, maximums, q1, q3, lower_outliers, upper_outliers]
stats_names = ['Median', 'Mean', 'Minimum', 'Maximum', 'Q1', 'Q3', 'Lower outliers', 'Upper outliers']
categories = ['cit', 'alt'] # to be updated
for i in range(len(categories)):
    print(f'\033[1m{categories[i]}\033[0m')
    for j in range(len(stats)):
        print(f'{stats_names[j]}: {stats[j][i]}')
    print('\n')

plt.xticks([1,2], ['Citations','Altmetric'])
plt.ylabel('Raw counts')
plt.grid(axis='y', alpha=1)
# plt.ylim(0,min(upper_outliers))
plt.savefig("./outputs/figures/figureB11-cit-alt-dims.jpeg",dpi=300)

plt.show()