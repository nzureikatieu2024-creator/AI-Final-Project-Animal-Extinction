Copy-paste this as your final `README.md`:

````md
# AI-Final-Project-Animal-Extinction

By: Noor Zureikat, Karim Junaidi, Hamza Almadi, Tina Haddad, Mohamed Embaby, and Haya Mourad

## Amphibian Extinction Risk Classification

This project uses machine learning to predict whether an amphibian species is at high extinction risk.

The project uses two original Excel files:

- `All_amphibians_tabular_data.xlsx`
- `Threats_to_Threatened_Species.xlsx`

These were cleaned and merged into:

- `data/amphibian_cleaned.xlsx`

The target variable is `High_Risk`:

- `1` = high-risk species
- `0` = lower-risk species

## How to Run the Project

First, clone the repository:

```bash
git clone https://github.com/nzureikatieu2024-creator/AI-Final-Project-Animal-Extinction.git
````

Move into the project folder:

```bash
cd AI-Final-Project-Animal-Extinction
```

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

Then run the final pipeline:

```bash
python final_pipeline.py
```

If your system uses `python3`, use:

```bash
python3 -m pip install -r requirements.txt
python3 final_pipeline.py
```

`final_pipeline.py` is the main file for the final submission. It runs the full workflow from data loading to model evaluation. The other Python files are included to show the earlier separate stages of the project and individual contributions.

## Note on Colab Export

This project was developed in Google Colab and exported into `.py` files. Because of that, some formatting may look slightly unusual, such as text sections appearing as triple-quoted markdown comments. This does not affect execution. The final pipeline still runs as a normal Python script.

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
├── 01_eda_preprocessing.py
├── 02_feature_sets_and_pipeline.py
├── 03_baseline_models.py
├── 04_hyperparamater_tuning.py
├── 05_final_model_evaluation.py
├── final_pipeline.py
├── requirements.txt
└── README.md
```

## File Descriptions

* `00_data_cleaning_merging.py`: cleans and merges the raw datasets
* `01_eda_preprocessing.py`: explores and preprocesses the dataset
* `02_feature_sets_and_pipeline.py`: creates feature sets and preprocessing pipelines
* `03_baseline_models.py`: trains baseline models
* `04_hyperparamater_tuning.py`: tunes the final models
* `05_final_model_evaluation.py`: evaluates the final models
* `final_pipeline.py`: runs the complete final workflow

## Feature Sets

We compared two feature sets:

**Restricted feature set**

* Taxonomy
* Geography
* Biological traits

**Full feature set**

* Restricted features
* Threat-related variables

The full model gave stronger numerical results, but we interpreted it carefully because threat variables may be linked to the Red List assessment process. For final interpretation, we focused more on the Restricted Random Forest because it is more conservative and better suited for identifying independent early indicators.

## Main Results

**Full Random Forest**

* F1-score: 0.992
* ROC-AUC: 0.996

**Restricted Random Forest**

* F1-score: 0.618
* ROC-AUC: 0.728

## Common Issues

If you get this error:

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



## Requirements

This project was developed in Python and exported from Google Colab into `.py` files.  
Some text sections may appear as triple-quoted markdown comments, but the code runs as a normal Python script.

To install everything needed to run the project, check the requiremnts.txt file
