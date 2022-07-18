# Generate boxplots for each metric for each publication type (excluding large Zenodo and Dimensions dfs)
# Views and Downloads are plotted next to each other

import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

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
rdjfile = rdjfile.rename(columns={"date": "date_datapaper","downloads": "downloads_datapaper", "views": "views_datapaper","Times cited": "tot_citations_datapaper","Recent citations": "rec_citations_datapaper", "Altmetric": "altmetric_datapaper"})
rdjdatasetfile = rdjdatasetfile.rename(columns={"date": "date_dataset","views": "views_dataset","unique-views": "unique-views_dataset", "downloads": "downloads_dataset", "unique-downloads": "unique-downloads_dataset"})
researchfile_rdj = researchfile_rdj.rename(columns={"Publication Date (online)": "date_research","Times cited": "tot_citations_research","Recent citations": "rec_citations_research", "Altmetric": "altmetric_research"})

datapaperfile = pd.concat([datapaperfile,rdjfile])
datasetfile = pd.concat([datasetfile,rdjdatasetfile])
researchfile = pd.concat([researchfile,researchfile_rdj])

# DATA PAPERS
## CITATIONS
df = datapaperfile[datapaperfile['tot_citations_datapaper'].notna()]
dps_cit = list(df['tot_citations_datapaper'])
bp = plt.boxplot(dps_cit, showmeans=True)
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
    stats = [medians, means, minimums, maximums, q1, q3, lower_outliers, upper_outliers]
stats_names = ['Median', 'Mean', 'Minimum', 'Maximum', 'Q1', 'Q3', 'Lower outliers', 'Upper outliers']
categories = ['Data paper citations'] # to be updated
for i in range(len(categories)):
    print(f'\033[1m{categories[i]}\033[0m')
    for j in range(len(stats)):
        print(f'{stats_names[j]}: {stats[j][i]}')
    print('\n')
plt.xticks([1], ['Citations'])
plt.ylabel('Raw counts')
plt.grid(axis='y', alpha=1)
plt.savefig("./outputs/figures/figure8-datapapercit.jpeg",dpi=300)

# plt.ylim(bottom_value,top_value)
plt.show()


## ALTMETRIC

df = datapaperfile[datapaperfile['altmetric_datapaper'].notna()]
dps_alt = list(df['altmetric_datapaper'])
bp = plt.boxplot(dps_alt, showmeans=True)
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
categories = ['Data paper altmetric'] # to be updated
for i in range(len(categories)):
    print(f'\033[1m{categories[i]}\033[0m')
    for j in range(len(stats)):
        print(f'{stats_names[j]}: {stats[j][i]}')
    print('\n')
plt.xticks([1], ['Altmetric'])
plt.ylabel('Raw counts')
plt.grid(axis='y', alpha=1)
# plt.ylim(bottom_value,top_value)
plt.savefig("./outputs/figures/figure10-datapaperalt.jpeg",dpi=300)
plt.show()


## DOWNLOADS/VIEWS
df = datapaperfile[datapaperfile['downloads_datapaper'].notna()]
dps_downs = list(df['downloads_datapaper'])
df = df[df['views_datapaper'].notna()]
dps_views = list(df['views_datapaper'])
bp = plt.boxplot([dps_downs,dps_views], showmeans=True)    
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
plt.savefig("./outputs/figures/figureB1-downviews-dp.jpeg",dpi=300)
# plt.ylim(bottom_value,top_value)
plt.show()


# RESEARCH PAPERS
## CITATIONS
df = researchfile[researchfile['tot_citations_research'].notna()]
rps_cit = list(df['tot_citations_research'])
bp = plt.boxplot(rps_cit, showmeans=True)
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
stats = [medians, means, minimums, maximums, q1, q3, lower_outliers, upper_outliers]
stats_names = ['Median', 'Mean', 'Minimum', 'Maximum', 'Q1', 'Q3', 'Lower outliers', 'Upper outliers']
categories = ['Research paper citations'] # to be updated
for i in range(len(categories)):
    print(f'\033[1m{categories[i]}\033[0m')
    for j in range(len(stats)):
        print(f'{stats_names[j]}: {stats[j][i]}')
    print('\n')
plt.xticks([1], ['Citations'])
plt.ylabel('Raw counts')
plt.grid(axis='y', alpha=1)
plt.savefig("./outputs/figures/figureB3-cit-res.jpeg",dpi=300)

# plt.ylim(bottom_value,top_value)
plt.show()


## ALTMETRIC
df = researchfile[researchfile['altmetric_research'].notna()]
rps_alt = list(df['altmetric_research'])
bp = plt.boxplot(rps_alt, showmeans=True)
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
stats = [medians, means, minimums, maximums, q1, q3, lower_outliers, upper_outliers]
stats_names = ['Median', 'Mean', 'Minimum', 'Maximum', 'Q1', 'Q3', 'Lower outliers', 'Upper outliers']
categories = ['Research paper altmetrics'] # to be updated
for i in range(len(categories)):
    print(f'\033[1m{categories[i]}\033[0m')
    for j in range(len(stats)):
        print(f'{stats_names[j]}: {stats[j][i]}')
    print('\n')
plt.xticks([1], ['Altmetric'])
plt.ylabel('Raw counts')
plt.grid(axis='y', alpha=1)
# plt.ylim(bottom_value,top_value)
plt.savefig("./outputs/figures/figureB5-alt-res.jpeg",dpi=300)

plt.show()

# DATASETS
## VIEWS/DOWNLOADS

df = datasetfile[datasetfile['downloads_dataset'].notna()]
dss_downs = list(df['downloads_dataset'])
df = df[df['views_dataset'].notna()]
dss_views = list(df['views_dataset'])
bp = plt.boxplot([dss_downs,dss_views], showmeans=True)    
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
# plt.ylim(bottom_value,top_value)
plt.savefig("./outputs/figures/figureB7-downviews-ds.jpeg",dpi=300)
plt.show()