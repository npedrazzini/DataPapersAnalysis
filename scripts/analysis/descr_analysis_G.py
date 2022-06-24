# Visualize age of publication (x-axis) and n of citations/Altmetric score of all Humanities
# research papers in Dimensions (2015-2022)
# Author: Marton Ribary

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

data_collection_date = '2022-06-04' # change to date of last export

df = pd.read_csv('./zenodo_dimensions_all_humss/dimensions_humss_research.csv')

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
df['tot_citations'] = df['tot_citations']/df['days_since_publication']
df['altmetric'] = df['altmetric']/df['days_since_publication']

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
plt.grid(axis='y', alpha=0.75)
plt.title('All humanities research paper in Dimensions (UK/US 2015-2022)')
plt.show()