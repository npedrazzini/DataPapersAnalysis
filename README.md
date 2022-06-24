# JOHD Data Analysis: scripts and data

## Project structure
```
ROOT
├─ README.md
├─ curated_inputs
│  ├─ datasets_datapapers-links-johd.csv
│  ├─ datasets_datapapers-links-rdj.csv
│  ├─ research_datapapers-links-johd.csv
│  └─ research_datapapers-links-rdj.csv
├─ dimensions_exports
│  ├─ johd_rdj
│  └─ research_papers
├─ outputs
│  ├─ analysis_outputs
│  ├─ final_outputs
│  │  ├─ johd
│  │  ├─ rdj
│  │  └─ research_papers
│  └─ scraper_outputs
│     ├─ johd
│     └─ rdj
├─ requirements.txt
├─ scripts
│  ├─ analysis
│  │  ├─ corr_analysis_A.py
│  │  ├─ corr_analysis_B.py
│  │  ├─ corr_analysis_C.py
│  │  ├─ descr_analysis_B-g_h.py
│  │  ├─ descr_analysis_C-D.py
│  │  ├─ descr_analysis_F.py
│  │  └─ descr_analysis_G.py
│  ├─ postprocess
│  │  ├─ merge_johd_dimensions.py
│  │  ├─ merge_rdj_dimensions.py
│  │  └─ merge_research_papers_dimensions.py
│  ├─ scraper
│  │  ├─ datasets_scraper.py
│  │  ├─ johd_scraper.py
│  │  └─ rdj_scraper.py
│  └─ zenodo_api
│     └─ zenodo.ipynb
└─ zenodo_dimensions_all_humss
```

## Pipeline summary
> NB: Every step in the pipeline needs to be done on the same day, else you may run into inconsistencies.
1. Update the curated inputs in this repository:
    - `datasets_datapapers-links-johd.csv`: add the latest data papers by JOHD and associated datasets (from [here](https://docs.google.com/spreadsheets/d/11MziEnCBh-Wz_GzBHi1PcM4p947yE9Nn/edit#gid=1230857751) or manually by checking the website).
    - `datasets_datapapers-links-rdj.csv`:  add the latest data papers by RDJ and associated datasets (from [here](https://docs.google.com/spreadsheets/d/11MziEnCBh-Wz_GzBHi1PcM4p947yE9Nn/edit#gid=1230857751) or manually by checking the website).
    - `research_datapapers-links-johd.csv`: add any missing research paper associated to JOHD data papers (from [here](https://docs.google.com/spreadsheets/d/1e0FiSv6VaOabt5rBFDyytj2A8tDS48ZZ5OLgxJ1dQ5E/edit#gid=0)).
    - `research_datapapers-links-rdj.csv`: add any missing research paper associated to RDJ data papers (from [here](https://docs.google.com/spreadsheets/d/1e0FiSv6VaOabt5rBFDyytj2A8tDS48ZZ5OLgxJ1dQ5E/edit#gid=0)).
2. Export the following data from Dimensions:
    - all publications by JOHD and RDJ (one dataset). Put the export in dimensions_exports/johd_rdj and rename the file to YYYY-MM-DD-dimensions_export.csv (where YYYY-MM-DD is the date of the export).
    - all DOIs of research papers associated with data papers as listed in `curated_inputs/research_datapapers-links-johd.csv` and `curated_inputs/research_datapapers-links-rdj.csv`.
3. Run `python scripts/scraper/johd_scraper.py`. This will output `outputs/scraper_outputs/johd/YYYY-MM-DD-scraper-datapapers-johd` (YYYY-MM-DD will automatically be changed with the date in which you run this script).
4. Run `python scripts/scraper/dataset_scraper.py`. This will output `outputs/scraper_outputs/johd/YYYY-MM-DD-scraper-datasets-johd.csv` (YYYY-MM-DD will automatically be changed with the date in which you run this script).
4. Run `python scripts/scraper/rdj_scraper.py`. This will output `outputs/scraper_outputs/rdj/YYYY-MM-DD-scraper-datasets-rdj.csv` (YYYY-MM-DD will automatically be changed with the date in which you run this script).
5. Make a copy of `outputs/scraper_outputs/johd/YYYY-MM-DD-scraper-datasets-johd.csv` and put it into `outputs/final_outputs/johd/`. Rename it to `YYYY-MM-DD-final-datasets-johd.csv`.
6. Manually add the metrics for the datasets which we can't crawl but can retrieve manually (currently 3):
    - 10.5334/johd.4
    - 10.5334/johd.15
    - 10.5334/johd.33
7. Run `python scripts/postprocess/merge_johd_dimensions.py`. This will output `outputs/final_outputs/johd/YYYY-MM-DD-final-datapapers-johd.csv`.
9. Run `python scripts/postprocess/merge_rdj_dimensions.py`. This will output `outputs/final_outputs/research_papers/YYYY-MM-DD-final-datapapers-rdj.csv`.
8. Run `python scripts/postprocess/merge_research_papers_dimensions.py`. This will output `outputs/final_outputs/research_papers/YYYY-MM-DD-final-research_papers-johd.csv` and `outputs/final_outputs/research_papers/YYYY-MM-DD-final-research_papers-rdj.csv`.
10. Congrats! You now have the final datasets that you need to run the analyses: 
- `YYYY-MM-DD-final-datasets-johd.csv`
- `YYYY-MM-DD-final-datapapers-johd.csv`
- `YYYY-MM-DD-final-datasets-rdj.csv`
- `YYYY-MM-DD-final-datapapers-rdj.csv`
- `YYYY-MM-DD-final-research_papers-johd`
- `YYYY-MM-DD-final-research_papers-rdj`

## Details about folders
### Curated inputs
This folder contains all manually-curated data papers-datasets and data papers-research papers linking for both JOHD and RDJ.

The data papers-datasets linking files contain the following variables:
- `DOI`: DOI of the data paper
- `repourl`: URL of the repository of the associated dataset
- `reponame`: Name of repository. Note that this variable is used as input to the dataset scraper (each repository has its own scraping method)
- `pub-date`: publication date of dataset

The data papers-research papers linking files contain the following variables:
- `DOI`: DOI of the data paper
- `DOI_research_paper`: DOI of the research paper

### Dimensions exports
This folder contains two subfolders:
- `johd_rdj`: monthly export from Dimensions for all JOHD + RDJ publications
- `research_papers`: monthly export from Dimensions for research papers linked with JOHD and RDJ data papers (one exports each, based on the linking files under `curated_inputs`).

### Outputs
#### `analysis_outputs`
This is where the analysis scripts will save all outputs.

#### `final_outputs`
This is where all final outputs are saved. These are also the inputs for the analysis scripts.
Three subfolders:
- `johd`
    - `YYYY-MM-DD-final-datapapers-johd.csv`: merged dataset containing both scraped metrics on data papers and relevant Dimensions variables on them.
    - `YYYY-MM-DD-final-datasets-johd.csv`: this file results from merging the data paper-dataset linking file with the metrics on datasets scraped from the respective repos.
- `rdj`
    -`YYYY-MM-DD-final-datapapers-rdj.csv`: merged dataset containing both scraped metrics on data papers and relevant Dimensions variables on them.
- `research_papers`
    -`YYYY-MM-DD-final-research_papers-johd.csv`: subset of the Dimensions export for research papers associated with JOHD data papers, containing relevant Dimensions variables and with added column for DOI of related data paper.
    -`YYYY-MM-DD-final-research_papers-rdj.csv`: subset of the Dimensions export for research papers associated with RDJ data papers, containing relevant Dimensions variables and with added column for DOI of related data paper.

#### `scraper_outputs`
This is where all the outputs of the scraping scripts are saved.
Two subfolders:
- `johd`:
    - `YYYY-MM-DD-scraper-datapapers-johd.csv`: datapapers metrics scraped from JOHD's website based on the list of publications in `datasets_datapapers-links-johd.csv`.
    - `YYYY-MM-DD-scraper-datasets-johd.csv`: dataset metrics scraped from the repos based on the list in `datasets_datapapers-links-johd.csv`.
- `rdj`:
    - `YYYY-MM-DD-scraper-datapapers-rdj.csv`: datapapers metrics (downloads, views) scraped from RDJ's website, based on the list of published articles in `datasets_datapapers-links-rdj.csv`

### zenodo_api
- `zenodo.ipynb`: builds a dataset of datasets published on Zenodo in the humanities and social sciences between 29 September 2015 (the date of the first JOHD article) and 4 June 2022 by communicating with the Zenodo REST API, and extracting the datastes's doi, html, publication_date, downloads and views; the output is a dataframe save in .json and .csv format. (Please note that you need your own Zenodo access token to reproduce these results.)

### zenodo_dimensions_all_humss
> Not included in GitHub repo because of LFS limit
Folder containing:
- `zenodo_humss_datasets.csv` and `zenodo_humss_datasets.json`: files with metrics for all humanities datasets in Zenodo (2015-2022) (CSV and JSON formats contain the same info).
- `dimensions_humss_research.csv`: file containing metrics from Dimensions for all humanities research papers published 2015-2022.

### Analysis scripts
#### `corr_analysis_A.py`
> Change value of variable `dateoflastdf` to date of latest datasets.

Runs correlation analysis between data paper metrics and associated dataset metric. 
It outputs `YYYY-MM-DD-correlations.csv`, which will contain the following variables:
- `variable1`: first variable
- `variable2`: second variable
- `rho`: Spearman's rank correlation coefficient
- `p-value`: p-value
- `Strength of correlation`: 'Strong' (1 > rho >= 0.7 or -1 < rho <= -0.7), 'Moderate' (0.7 > rho >= 0.4 or -0.7 < rho <= -0.4) or 'Weak' (0.4 > rho >= 0.1 or -0.4 < rho <= -0.1)
- `Significative?`: 'Significative' (p <= 0.05), 'Borderline' (0.05 < p <= 0.07) or 'Non-significative (p > 0.07)

#### `corr_analysis_B.py`
> Change value of variable `dateoflastdf` to date of latest datasets.

Runs **Mann-Whitney U-test** and **Welch's t-test** between the altmetric/citation counts of all research papers in the Humanities (2015-2022) and the altmetric/citation counts of research papers with associated data paper. It also plots a boxplot comparing the medians.
It outputs the statistics in two separate CSVs:
- YYYY-MM-DD-means-altmetric-analysis-B
- YYYY-MM-DD-means-citations-analysis-B
Each of the above contains 10 rows, corresponding to 10 different random sampling (each 5000 publications) of the dataset with all research papers in the Humanities.

#### `corr_analysis_C.py`
> Change value of variable `dateoflastdf` to date of latest datasets.

Runs **Mann-Whitney U-test** and **Welch's t-test** between the downloads/views of all datasets in the Humanities (2015-2022) and the downloads/views of datasets with associated data paper. It also plots a boxplot comparing the medians.
It outputs the statistics in two separate CSVs:
- YYYY-MM-DD-means-downloads-analysis-C
- YYYY-MM-DD-means-views-analysis-C
Each of the above contains 10 rows, corresponding to 10 different random sampling (each 5000 publications) of the dataset with all Zenodo datasets in the Humanities.

#### `descr_analysis_A.py`
Plots differences between JOHD and RDJHSS research fields, and  the number of publications along the years. 

#### `descr_analysis_B-g_h.py`
Plots difference in publication date between data papers and associated research papers, and the difference between data papers and associated datasets (to check which ones are generally published first, or how long before/after the other).

#### `descr_analysis_C-D.py`
Plots overall changes in metrics growth/decrease rates over time for JOHD/RDJ articles, normalizing by article/dataset age.

#### `descr_analysis_F.py`
Plots overall changes in metrics growth/decrease rates over time for all humanities datasets in Zenodo (2015-2022), normalizing by dataset age.

#### `descr_analysis_G.py`
Plots overall changes in metrics growth/decrease rates over time for all humanities research papers from Dimensions (2015-2022), normalizing by article/dataset age.

#### `johd_rdjhss_graphs_from_CompetitorData`
Plots differences in research fields between JOHD and RDJHSS, as well as the number of publications for each year. This is based on the data available in the .csv file named RDJ_JOHD_CompetitorData.xlsx - Data_JOHD_RDJ.csv

# NOTES
- In `datasets_datapapers-links-rdj.csv`:
    - For the title _Dative alternation revisited_ the DOI is not retrievable on Dimensions for the individual chapter (only for whole volume).
    - 10.6084/m9.figshare.14743044.v2 also not retrievable on Dimensions
    - CEUR proceedings publications not retrievable on Dimensions
- The script used to extract dataset metrics has bespoke methods for each repository, where possible. Note: data on OSF is not usable as it's not comparable to the others (it only provides views for the last 2 months and there's no easy way to get that info automatically anyway). 'Other' means that that repo either does not provide usage statistics or these need to be collected manually (see instructions in Pipeline summary).
- The dataset scraper will only distinguishes between the following repos: Zenodo, OSF, Dataverse, DataShare, DANS, Figshare, Figshare-Inst, Other
- **Figshare-Inst** (institutional Figshare, e.g. [this one](https://kilthub.cmu.edu/articles/dataset/DH_Conference_Index_Data_-_9_22_2020/12987959/1)) needs to be distinguished from Figshare, as it has a slightly different HTML structure than the generic Figshare one.


# TODO
