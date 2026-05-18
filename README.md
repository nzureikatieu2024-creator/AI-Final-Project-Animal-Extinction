# AI-Final-Project-Animal-Extinction

By: Noor Zureikat, Karim Junaidi, Hamza Almadi, Tina Haddad, Mohamed Embaby, and Haya Mourad

## Amphibian Extinction Risk Classification

This project predicts whether an amphibian species is at high extinction risk using machine learning.

The project uses two original Excel files:

- `All_amphibians_tabular_data.xlsx`
- `Threats_to_Threatened_Species.xlsx`

These were cleaned and merged into:

- `data/amphibian_cleaned.xlsx`

The target variable is `High_Risk`:

- `1` = high-risk species
- `0` = lower-risk species

## How to Run

Install the required packages:

```bash
python -m pip install -r requirements.txt
````

Then run the final pipeline:

```bash
python final_pipeline.py
```

or:

```bash
python3 final_pipeline.py
```

`final_pipeline.py` is the main file for the final submission. The other Python files show the earlier separate stages of the project.

The final pipeline was exported from Google Colab, so some text appears as triple-quoted markdown comments. This does not affect the code. It still runs as a normal Python script.

## Project Structure

```text
AI-Final-Project-Animal-Extinction/
├── data/
│   ├── All_amphibians_tabular_data.xlsx
│   ├── Threats_to_Threatened_Species.xlsx
│   └── amphibian_cleaned.xlsx
├── models/
├── outputs/
├── 00_data_cleaning_merging.py
├── 01_eda.py
├── 02_feature_engineering_pipeline.py
├── 03_baseline_models.py
├── 04_model_tuning.py
├── 05_final_model_evaluation.py
├── final_pipeline.py
├── requirements.txt
└── README.md
```

## Files

* `00_data_cleaning_merging.py`: cleans and merges the raw datasets
* `01_eda.py`: explores the dataset
* `02_feature_engineering_pipeline.py`: creates feature sets and preprocessing
* `03_baseline_models.py`: trains baseline models
* `04_model_tuning.py`: tunes the final models
* `05_final_model_evaluation.py`: evaluates the final models
* `final_pipeline.py`: runs the full final workflow

## Feature Sets

We compared two feature sets:

**Restricted features**

* Taxonomy
* Geography
* Biological traits

**Full features**

* Restricted features
* Threat-related variables

The full model gave stronger numerical results, but we interpreted it carefully because threat variables may be linked to the Red List assessment process. For final interpretation, we focused more on the Restricted Random Forest because it is more conservative.

## Main Results

**Full Random Forest**

* F1-score: 0.992
* ROC-AUC: 0.996

**Restricted Random Forest**

* F1-score: 0.618
* ROC-AUC: 0.728

## Common Issues

If you get:

```text
ModuleNotFoundError: No module named 'pandas'
```

run:

```bash
python -m pip install -r requirements.txt
```

If you get an `openpyxl` error, run:

```bash
python -m pip install openpyxl
```

If you see a `ResourceTracker` or `ChildProcessError` warning at the end, the code may still have run correctly as long as the results printed and the output files were created.
