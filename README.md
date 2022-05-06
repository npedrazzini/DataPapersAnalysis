# JOHD Data Analysis: scripts and data

## Project structure
```
johd_crawler
├─ README.md
├─ crawler_outputs
│  ├─ 2022-04-04-datasets-metrics.csv
│  └─ 2022-04-04-crawler_data.csv
├─ dimensions_exports
│  └─ 2022-04-04-dimensions_export.csv
├─ final_outputs
│  ├─ 2022-04-04-johd_metrics.csv
│  └─ 2022-04-04-datasets-metrics_manual.csv
├─ manual_inputs
│  ├─ 2022-05-04-competitor-manual-export.csv
│  ├─ 2022-05-04-export-manual-dataset.csv
│  └─ manual-datasets.csv
└─ scripts
   ├─ analysis/
   ├─ datasets_crawler.py
   ├─ find_repo_location.py
   ├─ johd_crawler.py
   └─ merge_johd_dimensions.py
```

## pipeline summary
> NB: The whole pipeline needs to be done in the same day, else you may run into inconsistencies.
1. Export data from dimensions.ai (for all publications by JOHD), rename the file to `YYYY-MM-DD-dimensions_export.csv` (where YYYY-MM-DD is the date of the export) and put it in the folder `dimensions_exports/`.
2. Manually add the latest data papers and associated datasets in `manual_inputs/manual-datasets.csv`.
3. Run `python johd_crawler.py`. This will output `crawler_outputs/YYYY-MM-DD-crawler_data.csv` (YYYY-MM-DD will automatically be changed with the date in which you run this script).
4. Run `python datasets_crawler.py`. This will output `crawler_outputs/YYYY-MM-DD-datasets-metrics.csv` (YYYY-MM-DD will automatically be changed with the date in which you run this script).
5. Make a copy of `crawler_outputs/YYYY-MM-DD-datasets-metrics.csv` and put it into `final_outputs/`. Rename it to `crawler_outputs/YYYY-MM-DD-datasets-metrics_manual.csv`.
6. Manually add the metrics for the datasets which we can't crawl (currently 3: see the list under the section **final_outputs**).
7. Run `python merge_johd_dimensions.py`. This will output `final_outputs/johd_metrics.csv`.
8. Congrats! You now have the two final datasets that we need for this month: `johd_metrics.csv` and `YYYY-MM-DD-datasets-metrics_manual.csv`.


## manual_inputs
Here you manually add and rename two files each month:
- `YYYY-MM-DD-competitor-manual-export.csv`: export [this](https://docs.google.com/spreadsheets/d/11MziEnCBh-Wz_GzBHi1PcM4p947yE9Nn/edit#gid=1230857751) spreadsheet (tab: Data JOHD_RDJ).
- `YYYY-MM-DD-export-manual-dataset.csv`: export [this](https://docs.google.com/spreadsheets/d/11MziEnCBh-Wz_GzBHi1PcM4p947yE9Nn/edit#gid=1230857751) spreadsheet (tab: JOHD_Dataset).

Based on `YYYY-MM-DD-export-manual-dataset.csv` update the file `manual-datasets.csv` accordingly with the latest publications (no need to check the older ones). Note: the latter distinguishes between the following repos:
- Zenodo
- OSF
- Dataverse
- DataShare
- DANS
- Figshare
- Figshare-Inst
- Other

> **Figshare-Inst** (institutional Figshare, e.g. [this one](https://kilthub.cmu.edu/articles/dataset/DH_Conference_Index_Data_-_9_22_2020/12987959/1)) needs to be distinguished from Figshare, as it has a slightly different HTML structure than the generic Figshare one.

## crawler_outputs
- `YYYY-MM-DD-dataset-metrics.csv`: dataset metrics crawled from the repos based on the list in `manual-datasets.csv`. The script used to extract these (`datasets_crawler.py`) has bespoke methods for each repository, where possible. Note: data on OSF is not usable as it's no comparable to the others (it only provides views for the last 2 months and there's no easy way to get that info automatically anyway). 'Other' means that that repo either does not provide usage statistics or these need to be collected manually (see instructions in `final_outputs`).

## final_outputs
- `YYYY-MM-DD-johd-metrics.csv`: the very final dataset, a merge of all dataset metrics, Dimension exports, and manually collected dataset if relevant. This is the dataset that will be used for the analysis.
- `YYYY-MM-DD-dataset-metrics_manual.csv`: copy of `YYYY-MM-DD-dataset-metrics.csv` (in `crawler_outputs`), with added manual usage statistics for repository: 'Other', where available. These are the following (check the respective repository in `manual-datasets.csv` and enter the statistics manually in `YYYY-MM-DD-dataset-metrics_manual.csv`):
    - 10.5334/johd.4
    - 10.5334/johd.15
    - 10.5334/johd.33

## dimensions_exports
Here we put a monthly export from dimensions.ai. Note: currently using an institutional account, since that provides more detailed info than the free version. Rename file everytime you add an export in the format: `YYYY-MM-DD-dimensions_export.csv`.

## scripts
- `datasets_crawler.py`: takes `manual_inputs/manual-datasets.csv` as input, outputs `YYYY-MM-DD-dataset-metrics.csv` into `crawler_outputs/`.
- `find_repo_location.py`: attempts to extract repo name from the articles. Because of structure inconsistencies in the data papers, the script does not always manage to extract the info. Don't use.
- `johd_crawler.py`: does not take any input. It simply crawls JOHD's website and loops over every article extracting the following info:
    - DOI (`str <DOI in the format 10.5334/johd.33>`)
    - article_title (`str <article title>`)
    - article_type (`str <Data Papers | Research Papers>`)
    - authors (`str <name1, name2, name3>`)
    - date (`float <data of publication>`)
    - downloads (`float <number of downloads>`)
    - views (`float <number of views>`)
    - tweets (`float <number of tweets>`)
    - data_collection_date: (`str <today>`)
- `merge_johd_dimensions.py`: merges `YYYY-MM-DD-crawler_data.csv` and `YYYY-MM-DD-dimensions_export.csv` and outputs `YYYY-MM-DD-johd_metrics.csv`.
