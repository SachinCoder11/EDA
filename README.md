# Space Mission Analysis — Project Review

## 1. Executive summary

This repository is an exploratory data-analysis project about historical orbital launches. It covers **4,324 missions from 1957 through 2020**, and investigates mission outcomes, launch activity, organisations, countries, launch vehicles, seasonality, rocket status, and launch-price estimation.

The strongest part of the project is its descriptive analysis of mission reliability and launch activity. The data cleaning also creates useful derived fields such as country, vehicle name, launch month/year, and decade. The most important caveat is price: **only 964 of 4,324 original records (22.29%) have an observed price**. Results involving price therefore depend heavily on the chosen imputation method. Two incompatible imputed datasets are present, and the fully populated analysis dataset creates a severe $5,000M concentration. This means its mean price and long-term price trend should not be treated as observed historical facts.

## 2. Project purpose and source context

The included Word brief describes a dataset scraped from Next Spaceflight's historical-launch pages. Its stated objective is to examine space missions from the beginning of the Space Race, including the organisation, launch location/date, rocket detail/status, price in USD millions, and mission outcome.

The project turns that source into a presentation-oriented analysis, with particular emphasis on:

- how mission success has changed by decade;
- countries, organisations, and vehicles with high activity or reliability;
- launch timing by month;
- active versus retired rockets; and
- estimating a largely missing price field.

## 3. Repository inventory

| Asset | Role | Notes |
|---|---|---|
| `orignal.csv` | Raw/source-like input | 4,324 rows and 9 columns; name contains a typo. It retains location/date/detail but has no cleaned country or vehicle fields. |
| `Space_Mission_Data_Final.csv` | Presentation/analysis dataset | 4,324 rows and 12 columns; adds country, ISO code, vehicle, launch date/month/year, and decade; its `Price` column has no missing values. |
| `Space_Mission_Data_RealWorld_Imputed.csv` | Alternative price-imputed dataset | 4,324 rows and 12 columns; retains raw-style columns and adds benchmark/provenance fields. 21 prices remain missing. |
| `w.py` | Reproducible benchmark-imputation script | Produces `Space_Mission_Data_RealWorld_Imputed.csv` from `orignal.csv`. |
| `Space_Mission_Data.ipynb` | Main EDA/presentation notebook | Covers mission status, trends, countries, organisations, vehicles, months, and price by decade. |
| `project001.ipynb` | Price-imputation experimentation notebook | Tests median-based imputations and a later multi-level model. |
| `final002.ipynb` | Imputation comparison/presentation notebook | Compares the final dataset with the real-world-benchmark dataset. |
| `FINAL _FINAL_BOSS.ipynb` | Price-distribution follow-up notebook | Investigates the $5B concentration and price bands. |
| `Space Mission Dataset.docx` | Dataset background | Defines the original fields and source context. |

There is no dependency file, README, requirements list, or single end-to-end pipeline entry point. Several notebooks use absolute machine-specific paths or filenames that are not included, so they cannot be executed from a fresh clone without edits.

## 4. Data lineage and schema

### 4.1 Original dataset

`orignal.csv` contains the following useful analytical fields:

`Organisation`, `Location`, `Date`, `Detail`, `Rocket_Status`, `Price`, and `Mission_Status`.

It also contains two index-like columns (`Unnamed: 0.1` and `Unnamed: 0`) that are artifacts, not mission attributes. Price is stored as text and may contain commas. After numeric conversion:

- rows: **4,324**;
- observed prices: **964**;
- missing prices: **3,360** (**77.71%**);
- observed-price median: **$62.00M**;
- observed-price mean: **$153.79M**;
- observed-price range: **$5.30M to $5,000M**.

### 4.2 Cleaned analysis dataset

`Space_Mission_Data_Final.csv` has a more convenient analysis schema:

`Organisation`, `Country`, `ISO Code`, `Vehicle_Name`, `Launch_date`, `Launch_Month`, `Launch_Year`, `Rocket_Status`, `Price`, `Mission_Status`, and `Decade`.

The `Decade` value is the decade start year (for example, 2019 maps to 2010), which is appropriate for grouping and plotting. It has 36 missing ISO codes, but no missing values in its principal analytical fields. Its leading `Unnamed: 0` column should be dropped before downstream use.

### 4.3 Benchmark-imputed dataset

`Space_Mission_Data_RealWorld_Imputed.csv` is produced by `w.py`. It:

1. converts raw price strings to numeric values;
2. copies the observed amount to `Price_Original` in memory;
3. maps organisations to a manually curated `org_benchmark` dictionary of USD-million launch costs;
4. fills only missing prices where a benchmark exists;
5. creates `Price_Source` with `Original Observed`, `Real-World Organisation Benchmark`, or `Still Missing`; and
6. asserts that no originally observed price changed before export.

The saved file contains 964 original observed prices, **3,339 benchmark-imputed prices**, and **21 still-missing prices**. It achieves **99.51% price coverage**. Its completed-price median is **$40.00M**, mean is **$101.54M**, and range is **$0.30M to $5,000M**. The unresolved records belong to AMBA (8), KCST (5), CECLES (4), SRC (3), and IRGC (1).

The file also contains two index artifacts and an entirely empty `Unnamed: 9` column; these should be removed in a cleaned release.

## 5. Validated descriptive findings

The following metrics were recomputed from `Space_Mission_Data_Final.csv`, rather than copied only from notebook prose.

### 5.1 Overall mission outcome and rocket status

| Measure | Count | Share |
|---|---:|---:|
| Successful missions | 3,879 | 89.71% |
| Failures | 339 | 7.84% |
| Partial failures | 102 | 2.36% |
| Prelaunch failures | 4 | 0.09% |
| Retired rockets | 3,534 | 81.73% |
| Active rockets | 790 | 18.27% |

The headline conclusion is well supported: historical launch success is high overall, with outright failure representing less than one in twelve records. The outcome labels should nevertheless be retained separately; combining partial and prelaunch failure with failure would conceal meaningful operational differences.

### 5.2 Reliability over time

| Decade | Missions | Success rate |
|---:|---:|---:|
| 1950s | 51 | 31.37% |
| 1960s | 774 | 79.07% |
| 1970s | 1,012 | 92.69% |
| 1980s | 631 | 93.66% |
| 1990s | 642 | 91.74% |
| 2000s | 475 | 93.26% |
| 2010s | 676 | 93.64% |
| 2020s | 63 | 90.48% |

The data supports a large reliability improvement from the early Space Race to the 1970s, after which success remains around 92–94%. The 1950s and 2020s have far fewer records than other decades, so their rates have greater uncertainty and should not be overcompared with mature decades.

### 5.3 Mission concentration

The dataset is dominated by a small number of organisations and launch locations. The most frequent organisations are RVSN USSR (1,777 missions), Arianespace (279), CASC (251), General Dynamics (251), NASA (203), and VKS RF (201). The leading countries/locations are Russia (1,395), USA (1,345), Kazakhstan (701), France (303), and China (269).

This concentration matters for every aggregate comparison: a global trend is strongly shaped by Soviet/Russian and US activity. The `Country` field appears to represent the launch location/country rather than the operating organisation's home country—Kazakhstan, for example, is a major launch-site location—so it should be named and interpreted carefully.

For the ten countries with the highest launch counts, France has the highest success rate (94.06%), followed by Russia (93.41%). Kazakhstan has 86.73%; India has 82.89%, based on 76 records; and Iran has 35.71%, based on only 14. The latter small denominators are a reason to show both counts and rates together.

### 5.4 Vehicles and launch calendar

The most frequently recorded vehicle is **Cosmos-3M (11K65M)** with 446 launches, followed by **Voskhod** with 299. The next highest are Molniya-M /Block ML (128), Cosmos-2I (63SM) (126), Soyuz U (125), Tsyklon-3 (122), and Tsyklon-2 (106). This reinforces the theme that repeated use of established systems is a major part of the history in this data.

Launches are not evenly distributed by month. December is highest with **450** launches and January lowest with **268**; June is second with **402**. This is descriptive seasonality only: the notebooks offer plausible operational explanations, but the dataset does not contain budgets, weather, scheduling constraints, or payload readiness, so it cannot establish why the difference occurs.

## 6. Price analysis and imputation assessment

### 6.1 What the notebooks attempted

`project001.ipynb` first evaluates three approaches on a random 20% holdout of known prices:

- global median: notebook-reported MAE **$116.02M**;
- organisation median: **$20.09M**;
- organisation + decade median: **$12.46M**.

It then proposes a richer fallback hierarchy with a minimum group size of three: Rocket + Organisation + Decade; Rocket + Organisation; Rocket + Decade; Organisation + Decade; Rocket; Organisation; then global median. A decade factor is subsequently applied. This is a sensible attempt to use the available context and protect against tiny group estimates.

`final002.ipynb` explicitly warns that different imputation strategies yield materially different costs and compares the all-filled "team" dataset with the real-world benchmark dataset. This is an important and correct caution.

### 6.2 Critical inconsistency in the committed outputs

The method described in `project001.ipynb` does not cleanly reproduce or document the `Price` field in `Space_Mission_Data_Final.csv`. That final file:

- contains no missing prices;
- preserves every originally observed price in the same row order; but
- contains **1,777 values exactly equal to $5,000M**, all belonging to **RVSN USSR**.

Its resulting price summary is:

| Statistic | Value |
|---|---:|
| Mean | $2,130.26M |
| Median | $200.00M |
| 25th percentile | $62.00M |
| 75th percentile | $5,000.00M |
| Maximum | $5,000.00M |

This is not a naturally interpretable price distribution. The $5,000M values alone make up **41.10%** of all missions, so the mean, 75th percentile, price bands, organisation comparisons, and apparent historical price trend are dominated by a repeated imputation rather than observed cost data. The follow-up notebook correctly detects that concentration, but it analyses it after the fact instead of preventing or labeling it.

The benchmark dataset is more auditable because it names the price source. It is still not a ground-truth cost dataset: a single present-day/representative organisation benchmark is assigned to many missions across several decades and mission types. Its estimates are useful for sensitivity analysis, not as verified historical launch prices.

### 6.3 Interpretation rule

Use observed prices for claims about historical cost. If estimated prices must be included, present them with a source flag and report sensitivity under more than one method. Never describe the price-imputed trend as a direct measure of affordability without controlling for inflation, currency year, mission scope, launch vehicle, payload, and the high level of missingness.

## 7. Notebook-by-notebook assessment

### `Space_Mission_Data.ipynb`

This is the primary analysis narrative. It correctly motivates the data, computes status distributions, success rates by decade and country, launch counts by organisation/location/vehicle, vehicle success rates, monthly volume, and an average-price-by-decade plot. Its main limitations are hard-coded absolute file paths, a reference to an unavailable `space_mission_data.csv`, and several chart/question-label mismatches (for example, a section called cities counts `Country`; a section headed organisation launches instead plots success-to-failure ratio).

### `project001.ipynb`

This is the best methodological notebook. It cleans price values, derives dates/decades, performs a holdout validation, and develops successive imputation ideas. It needs a clear final export step that generates the documented release file, stores model/validation outputs, sets the random-split methodology and seed in the report, and marks estimated values in the dataset.

### `final002.ipynb`

This notebook is a valuable comparison between the two imputation philosophies. Its markdown description is inconsistent: one section says a three-level mean-based approach, while another says organisation median → decade median → overall median. The actual files should be the source of truth and the narrative should name exactly which method produced each file.

### `FINAL _FINAL_BOSS.ipynb`

This is mainly a price-distribution investigation and Plotly sunburst visualization. It highlights the $5B cluster and advises caution, but one cell incorrectly calls `Space_Mission_Data_Final.csv` the "original" dataset when calculating data availability. It also references a nonexistent `csv_Final_Bosss.xlsx` file. The closing unrelated "personal info" markdown cell should be removed.

## 8. Quality, reproducibility, and analytical risks

1. **No canonical release dataset or pipeline.** Three CSV variants and multiple notebooks make it unclear which output should be used for each conclusion.
2. **Price provenance is missing in the main analysis dataset.** `Price_Source` and the original amount should accompany every estimated value.
3. **High missingness makes cost conclusions fragile.** 77.71% of original prices are absent; a full-price chart is mostly modeling output.
4. **Potentially incorrect/opaque $5B imputation.** Every RVSN USSR record receives the same value in the final file, materially distorting results.
5. **No inflation adjustment.** Nominal prices across 1957–2020 are not directly comparable as a time series.
6. **Sampling validation may leak time or group patterns.** A single random split is useful but should be supplemented with repeated cross-validation or time-aware/group-aware validation.
7. **Sparse-group and denominator effects.** Success-rate rankings need launch counts, confidence intervals, or a minimum-count rule.
8. **Schema hygiene issues.** Index columns remain in all CSVs; the benchmark file has an empty column; field names and date columns vary between files.
9. **Portability issues.** Absolute local paths and absent inputs prevent reliable reruns.
10. **Notebook narrative needs editorial cleanup.** Typos, duplicated questions, and unsupported causal explanations reduce presentation quality despite mostly sound calculations.

## 9. Recommended next steps

1. Define one authoritative cleaned dataset with a data dictionary and a versioned `README`.
2. Keep `price_observed`, `price_estimated`, `price_source`, `imputation_method`, and (where applicable) `benchmark_version` as separate fields; do not overwrite observed/estimated distinction.
3. Investigate and replace the RVSN USSR $5,000M mass assignment before using `Space_Mission_Data_Final.csv` for price conclusions.
4. Produce two explicit analyses: an observed-price analysis (honest but smaller sample) and a sensitivity analysis across imputation methods.
5. Convert all monetary values to a chosen constant-dollar year if comparing decades, and document the conversion source.
6. Replace hard-coded paths with paths relative to the repository, add `requirements.txt`, and create one reproducible cleaning script/notebook that writes outputs deterministically.
7. Drop artifact columns, validate dates/categories, and document whether `Country` means launch-site country or organisation nationality.
8. Improve visuals by showing counts with percentages, labelling estimated-price charts prominently, adding sample sizes to rankings, and avoiding pie charts for ratios.

## 10. Bottom line

The project provides a solid beginner-level historical launch EDA and successfully identifies a compelling core story: launch reliability rose sharply after the early Space Race and high mission volume is concentrated among a few organisations, locations, and vehicle families. The conclusions about reliability, counts, and seasonality are generally supported by the data. The price story is not yet production-ready: it is valuable as an imputation case study, but its current all-filled final dataset is dominated by undocumented estimates. Resolving price provenance and reproducibility would turn this from a good exploratory project into a trustworthy analytical deliverable.
