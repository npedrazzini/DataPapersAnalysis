#Do research papers in the humanities that have data papers associated with them get higher metrics?
from statistics import mean, stdev
import pandas as pd
from scipy import stats
import random
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import csv
import itertools

dateoflastdf = '2022-07-04' # change to date of last export

df_dimens = pd.read_csv('dimensions_humss_research.csv')

#Drop duplicates
df_dimens = df_dimens.drop_duplicates('Publication ID', keep='last')

df_linked1 = pd.read_csv("./outputs/final_outputs/research_papers/{}-final-research_papers-rdj.csv".format(dateoflastdf))
df_linked2 = pd.read_csv("./outputs/final_outputs/research_papers/{}-final-research_papers-johd.csv".format(dateoflastdf))

li = [df_linked1,df_linked2]

df_linked = pd.concat(li, axis=0, ignore_index=True)

df_dimens = df_dimens.dropna(subset=['Publication Date (online)'])
df_linked = df_linked.dropna(subset=['Publication Date (online)'])

# For publication in Dimensions that have no day of the month, assign '15'
df_dimens['Publication Date (online)'] = [str(x) + '-15' if len(str(x)) == 7 else x for x in df_dimens['Publication Date (online)']]

# Drop those that have only a year (i.e. keep dates that are of length 10, e.g. 2022-03-04)
df_dimens = df_dimens[df_dimens['Publication Date (online)'].str.len()==10]

date_format = "%Y-%m-%d"

#NORMALIZATION
df_dimens['Publication Date (online)'] = [datetime.strptime(str(x), date_format) for x in df_dimens['Publication Date (online)']]
df_linked['Publication Date (online)'] = [datetime.strptime(str(x), date_format) for x in df_linked['Publication Date (online)']]

# Dates when data was collected is different for the 2 dfs
datedf_dimens = datetime.strptime('2022-06-05', date_format)
datedf_linked = datetime.strptime('2022-07-05', date_format)

# Exclude pub date beyond '2022-06-04'
df_dimens = df_dimens[df_dimens['Publication Date (online)']<datedf_dimens]

# Calculate days since publication
df_dimens['days_since_pub'] = datedf_dimens - df_dimens['Publication Date (online)']
df_dimens['days_since_pub'] = [x.days for x in df_dimens['days_since_pub']]

df_linked['days_since_pub'] = datedf_linked - df_linked['Publication Date (online)']
df_linked['days_since_pub'] = [x.days for x in df_linked['days_since_pub']]


# Normalize dividing by age
# df_dimens['Times cited'] = df_dimens['Times cited']/df_dimens['days_since_pub']
# df_linked['Times cited'] = df_linked['Times cited']/df_linked['days_since_pub']

df_dimens2 = df_dimens.dropna(subset=['Times cited'])
df_linked2 = df_linked.dropna(subset=['Times cited'])

# Remove outliers
q1, q3= np.percentile(sorted(df_dimens2['Times cited']),[25,75])
iqr = q3 - q1
lower_bound_citations = q1 -(1.5 * iqr) 
upper_bound_citations = q3 +(1.5 * iqr) 
outlier_max_citations = upper_bound_citations         # Set the outlier threshold (max)
outlier_min_citations = lower_bound_citations             # Set the outlier threshold (min)
print('Citations Dimensions lower limit: ',outlier_min_citations)
print('Citations Dimensions upper limit: ',outlier_max_citations)
df_dimens2  = df_dimens2.loc[(df_dimens2['Times cited'] <= outlier_max_citations) & (df_dimens2['Times cited'] >= outlier_min_citations)] 

q1, q3= np.percentile(sorted(df_linked2['Times cited']),[25,75])
iqr = q3 - q1
lower_bound_citations = q1 -(1.5 * iqr) 
upper_bound_citations = q3 +(1.5 * iqr) 
outlier_max_citations = upper_bound_citations         # Set the outlier threshold (max)
outlier_min_citations = lower_bound_citations             # Set the outlier threshold (min)
print('Citations JOHD/RDJ lower limit: ',outlier_min_citations)
print('Citations JOHD/RDJ upper limit: ',outlier_max_citations)
df_linked2  = df_linked2.loc[(df_linked2['Times cited'] <= outlier_max_citations) & (df_linked2['Times cited'] >= outlier_min_citations)] 


#10-fold random sampling
with open('./outputs/analysis_outputs/{}-means-citations-analysis-B.csv'.format(dateoflastdf), 'w') as outcsv:
    outcsv = csv.writer(outcsv, delimiter=',')
    outcsv.writerow(['variable1','variable2','mean_variable1','mean_variable2','welchs_stats','welchs_pvalue','mannwhit_stats','mannwhit_pvalue'])
    for _ in itertools.repeat(None, 10):
        df_dimens2 = df_dimens2.dropna(subset=['Times cited'])
        df_linked2 = df_linked2.dropna(subset=['Times cited'])

        y = random.sample(sorted(list(df_dimens2['Times cited'])), 5000)
        
        all_research_citations_mean = mean(y)
        research_withDP_citations_mean = mean(df_linked2['Times cited'])

        welchs_stats_citations, welchs_p_citations = stats.ttest_ind(df_linked2['Times cited'], y, equal_var = False)
        mannwhit_stats_citations, mannwhit_p_citations = stats.mannwhitneyu(df_linked2['Times cited'], y)
        
        outcsv.writerow(['all-HSS-res-papers_cit','res-papers-with-data-paper_cit',all_research_citations_mean,research_withDP_citations_mean,welchs_stats_citations,welchs_p_citations,mannwhit_stats_citations,mannwhit_p_citations])

# Normalize dividing by age
# df_dimens['Altmetric'] = df_dimens['Altmetric']/df_dimens['days_since_pub']
# df_linked['Altmetric'] = df_linked['Altmetric']/df_linked['days_since_pub']
df_dimens3 = df_dimens.dropna(subset=['Altmetric'])
df_linked3 = df_linked.dropna(subset=['Altmetric'])

# Remove outliers
q1, q3= np.percentile(sorted(df_dimens3['Altmetric']),[25,75])
iqr = q3 - q1
lower_bound_citations = q1 -(1.5 * iqr) 
upper_bound_citations = q3 +(1.5 * iqr) 
outlier_max_citations = upper_bound_citations         # Set the outlier threshold (max)
outlier_min_citations = lower_bound_citations             # Set the outlier threshold (min)
print('Altmetric Dimensions lower limit: ',outlier_min_citations)
print('Altmetric Dimensions upper limit: ',outlier_max_citations)
df_dimens3  = df_dimens3.loc[(df_dimens3['Altmetric'] <= outlier_max_citations) & (df_dimens3['Altmetric'] >= outlier_min_citations)] 

# Remove outliers
q1, q3= np.percentile(sorted(df_linked3['Altmetric']),[25,75])
iqr = q3 - q1
lower_bound_citations = q1 -(1.5 * iqr) 
upper_bound_citations = q3 +(1.5 * iqr) 
outlier_max_citations = upper_bound_citations         # Set the outlier threshold (max)
outlier_min_citations = lower_bound_citations             # Set the outlier threshold (min)
print('Altmetric JOHD/RDJ lower limit: ',outlier_min_citations)
print('Altmetric JOHD/RDJ upper limit: ',outlier_max_citations)
df_linked3  = df_linked3.loc[(df_linked3['Altmetric'] <= outlier_max_citations) & (df_linked3['Altmetric'] >= outlier_min_citations)] 

# Take 5000 random values from research paper to check normality of distribution (shapiro can't be done with n>5000)
#10-fold random sampling
with open('./outputs/analysis_outputs/{}-means-altmetric-analysis-B.csv'.format(dateoflastdf), 'w') as outcsv:
    outcsv = csv.writer(outcsv, delimiter=',')
    outcsv.writerow(['variable1','variable2','mean_variable1','mean_variable2','welchs_stats','welchs_pvalue','mannwhit_stats','mannwhit_pvalue'])
    for _ in itertools.repeat(None, 10):
        df_dimens3 = df_dimens3.dropna(subset=['Altmetric'])
        df_linked3 = df_linked3.dropna(subset=['Altmetric'])

        y = random.sample(sorted(list(df_dimens3['Altmetric'])), 5000)
        
        all_research_altmetric_mean = mean(y)
        research_withDP_altmetric_mean = mean(df_linked3['Altmetric'])

        welchs_stats_altmetric, welchs_p_altmetric = stats.ttest_ind(df_linked3['Altmetric'], y, equal_var = False)
        mannwhit_stats_altmetric, mannwhit_p_altmetric = stats.mannwhitneyu(df_linked3['Altmetric'], y)
        
        outcsv.writerow(['all-HSS-res-papers_Alt','res-papers-with-data-paper_Alt',all_research_altmetric_mean,research_withDP_altmetric_mean,welchs_stats_altmetric,welchs_p_altmetric,mannwhit_stats_altmetric,mannwhit_p_altmetric])


# Export df for R boxplots
x = random.sample(sorted(list(df_dimens3['Altmetric'])), 5000)
y = random.sample(sorted(list(df_dimens2['Times cited'])), 5000)

# dimen2 = pd.DataFrame({'Altmetric': x, 'Times cited': y})
# dimen2.to_csv('dimenforR.csv', index=False)
# df_linked2.to_csv('df_linked.csv', columns=['Altmetric','Times cited'], index=False)

array1 = [df_linked3['Altmetric'],x]
plt.boxplot(array1)
# plt.ylim(bottom_value,top_value)
plt.ylabel('Altmetric: raw counts')
plt.grid(axis='y', alpha=0.75)
plt.xticks([1,2], ['Res. papers with data paper','All HSS res. papers'])
plt.savefig("./outputs/figures/figure12-cit-res-vs-dims.jpeg",dpi=300)
plt.show()

array1 = [df_linked2['Times cited'],y]
plt.boxplot(array1)
plt.ylabel('Citations: raw counts')
plt.grid(axis='y', alpha=0.75)
plt.xticks([1,2], ['Res. papers with data paper','All HSS res. papers'])
plt.savefig("./outputs/figures/figure13-alt-res-vs-dims.jpeg",dpi=300)
plt.show()
