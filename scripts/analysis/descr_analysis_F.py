# Visualize age of publication (x-axis) and n of downloads/views of all Humanities
# datasets in Zenodo (2015-2022)
# Author: Marton Ribary

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('./zenodo_humss_datasets.csv')

# IQR-interquartile range to detect outliers
#IQR --> points which fall more than 1.5 times the interquartile range above the third quartile or below the first quartile.
q1, q3= np.percentile(sorted(df['views']),[25,75])
iqr = q3 - q1
lower_bound_views = q1 -(1.5 * iqr) 
upper_bound_views = q3 +(1.5 * iqr) 
print('Views lower limit: ',lower_bound_views)
print('Views upper limit: ',upper_bound_views)

q1, q3= np.percentile(sorted(df['downloads']),[25,75])
iqr = q3 - q1
lower_bound_downloads = q1 -(1.5 * iqr) 
upper_bound_downloads = q3 +(1.5 * iqr) 
print('Downloads lower limit: ',lower_bound_downloads)
print('Downloads upper limit: ',upper_bound_downloads)

# Remove outliers
outlier_max_views = upper_bound_views         # Set the outlier threshold (max)
outlier_min_views = lower_bound_views             # Set the outlier threshold (min)
outlier_max_downloads = upper_bound_downloads      # Set the outlier threshold (max)
outlier_min_downloads = lower_bound_downloads           # Set the outlier threshold (min)
df  = df.loc[(df['views'] <= outlier_max_views) \
    & (df['downloads'] <= outlier_max_downloads) & (df['downloads'] >= outlier_min_downloads) \
    & (df['views'] >= outlier_min_views)] 

# Replace downloads and views with time-normalised data
# # Skip this cell if you want to work with total counts
# df['downloads'] = df['downloads']/df['days_since_publication']
# df['views'] = df['views']/df['days_since_publication']

# Create dataframe with daily averages and remove outliers
days_since_publication = df['days_since_publication'].unique()
views = []
downloads = []
for day in days_since_publication:
    mean_views = df['views'][df['days_since_publication'] == day].mean()
    mean_downloads = df['downloads'][df['days_since_publication'] == day].mean()
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
df_means_period = pd.DataFrame({'less_than_n_days_since_publication': periods, \
    'monthly_mean_views': p_views, 'monthly_mean_downloads': p_downloads})
df_means_period = df_means_period.sort_values(by='less_than_n_days_since_publication', ascending=False)

# Reducing to years to be consistent with the other plots
df_means_period['less_than_n_days_since_publication'] = [x/365 for x in df_means_period['less_than_n_days_since_publication']]

df_means_period = df_means_period[df_means_period['monthly_mean_views'] != max(df_means_period['monthly_mean_views'])]

df_means_period = df_means_period[df_means_period['monthly_mean_downloads'] != max(df_means_period['monthly_mean_downloads'])]

# Plot 90-day averages for views and downloads
# Views
x = np.array(df_means_period['less_than_n_days_since_publication'])
y = np.array(df_means_period['monthly_mean_views'])
plt.scatter(x,y,c='red',label='Views')

# Downlaods
x = np.array(df_means_period['less_than_n_days_since_publication'])
y = np.array(df_means_period['monthly_mean_downloads'])
plt.scatter(x,y,c='yellow',label='Downloads')
plt.legend()
plt.xlabel('Years')
plt.ylabel('Age-normalised counts')
plt.grid(axis='y', alpha=0.75)
# plt.savefig("./outputs/figures/figureB10-down-zen.jpeg",dpi=300)

plt.show()




df = df[df['downloads'].notna()]
df3 = list(df['downloads'])

df = df[df['views'].notna()]
df4 = list(df['views'])


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
categories = ['Downloads', 'Views'] # to be updated
for i in range(len(categories)):
    print(f'\033[1m{categories[i]}\033[0m')
    for j in range(len(stats)):
        print(f'{stats_names[j]}: {stats[j][i]}')
    print('\n')

plt.xticks([1,2], ['Downloads','Views'])
plt.ylabel('Raw counts')
plt.grid(axis='y', alpha=1)
# plt.ylim(0,min(upper_outliers))
plt.savefig("./outputs/figures/figureB9-down-views-zen.jpeg",dpi=300)

plt.show()
