# AI-Final-Project-Animal-Extinction
By: Noor Zureikat, Karim Junadi, Hamza Madi, Tina Haddad, Mohamed Embaby and Haya Mourad

# Amphibian Extinction Risk Classification Project

## Overview

This project predicts whether an amphibian species is at high extinction risk using machine learning.

We used two original Excel files:

- `All_amphibians_tabular_data.xlsx`
- `Threats_to_Threatened_Species.xlsx`

These were cleaned and merged into:

```text
data/amphibian_cleaned.xlsx
````

The target variable is `High_Risk`:

* `1` = high-risk species
* `0` = lower-risk species

## Main File

To run the project, use:

```bash
python final_pipeline.py
```

or:

```bash
python3 final_pipeline.py
```

The other Python files are included to show the separate work done during the project. They are mainly evidence of the process and individual contributions. For the final version, only `final_pipeline.py` needs to be run.

## Project Structure

```text
AI-Final-Project-Animal-Extinction/
├── data/
│   ├── All_amphibians_tabular_data.xlsx
│   ├── Threats_to_Threatened_Species.xlsx
│   └── amphibian_cleaned.xlsx
│
├── models/
├── outputs/
│
├── 00_data_cleaning_merging.py
├── 01_eda.py
├── 02_feature_engineering_pipeline.py
├── 03_baseline_models.py
├── 04_model_tuning.py
├── 05_final_model_evaluation.py
├── final_pipeline.py
└── README.md
```

## Setup

Install the required packages before running the code:

```bash
python -m pip install pandas numpy matplotlib seaborn scikit-learn joblib openpyxl
```

If that does not work, try:

```bash
python3 -m pip install pandas numpy matplotlib seaborn scikit-learn joblib openpyxl
```

## What the Final Pipeline Does

`final_pipeline.py` runs the full workflow:

1. Loads the data
2. Runs EDA
3. Creates the feature sets
4. Splits the data into train and test sets
5. Builds preprocessing pipelines
6. Trains baseline models
7. Tunes the final models
8. Saves model and output files
9. Evaluates the final models

## Individual Files

The separate files show the steps we worked on before combining everything:

* `00_data_cleaning_merging.py`: cleans and merges the raw datasets
* `01_eda.py`: explores the dataset
* `02_feature_engineering_pipeline.py`: creates features and preprocessing
* `03_baseline_models.py`: trains baseline models
* `04_model_tuning.py`: tunes the final models
* `05_final_model_evaluation.py`: evaluates and explains the final results
* `final_pipeline.py`: main file to run

## Models and Features

We compared two feature sets:

**Restricted features**

* Taxonomy
* Geography
* Biological traits

**Full features**

* Restricted features
* Threat-related variables

The full model gave the strongest numerical results, but we treated it carefully because threat variables may be closely connected to the Red List assessment process.

For final interpretation, we focused more on the Restricted Random Forest because it is a more conservative model.

## Main Results

Full Random Forest:

```text
F1-score: 0.992
ROC-AUC: 0.996
```

Restricted Random Forest:

```text
F1-score: 0.618
ROC-AUC: 0.728
```

The full model performs much better, showing that threat variables are highly predictive. The restricted model performs more moderately, but it is more useful for discussing early indicators because it relies only on taxonomy, geography, and biological traits.

## Common Issues

If you get:

```text
ModuleNotFoundError: No module named 'pandas'
```

run:

```bash
python -m pip install pandas numpy matplotlib seaborn scikit-learn joblib openpyxl
```

If you get an `openpyxl` error, run:

```bash
python -m pip install openpyxl
```

If you see a `ResourceTracker` or `ChildProcessError` warning at the end, the code may still have run correctly as long as the results printed. This warning can happen during model tuning.

## Final Note

For the final submission, run:

```bash
python final_pipeline.py
```

The other files are included for evidence and organization, but the final pipeline is the main file.


