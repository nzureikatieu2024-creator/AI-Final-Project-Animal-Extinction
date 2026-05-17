# ==============================
# 1. DATA LOADING & EDA
# ==============================

## Step 1:  Dataset
import os

os.system("pip install pandas numpy matplotlib seaborn scikit-learn joblib openpyxl")
from pathlib import Path


# Project structure
BASE_DIR = Path(".")
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
OUTPUTS_DIR = BASE_DIR / "outputs"

# Create folders if they don't exist
MODELS_DIR.mkdir(exist_ok=True)
OUTPUTS_DIR.mkdir(exist_ok=True)

import pandas as pd
# The cleaned dataset was created from the two raw source files using
# 00_data_cleaning_merging.py. The raw files and cleaning script are included
# in the repository for reproducibility.

df = pd.read_excel(DATA_DIR / "amphibian_cleaned.xlsx")
df.head()

"""## Step 2: Overview"""

df.shape
df.info()
df.describe()

"""## Step 3: Columns"""

df.columns

df = df.rename(columns={
    "Mining/energy_production": "Mining_energy_production",
    "Climate_(ongoing)": "Climate_ongoing",
    "Climate_(future)": "Climate_future",
    "Bd_(future)": "Bd_future",
    "Bd_(ongoing)": "Bd_ongoing",
    "Bsal_(future)": "Bsal_future",
    "Bsal_(ongoing)": "Bsal_ongoing"
})

"""#Missing Values"""

missing_counts = df.isnull().sum().sort_values(ascending=False)
missing_percent = (df.isnull().mean() * 100).sort_values(ascending=False)

missing_summary = pd.DataFrame({
    "missing_count": missing_counts,
    "missing_percent": missing_percent
})

missing_summary[missing_summary["missing_count"] > 0]

"""We checked missing values to understand which variables may require imputation before modeling. Missing values will be handled during preprocessing, with categorical variables imputed using the most frequent value and binary indicators filled appropriately."""

df.duplicated().sum()

"""Duplicate rows were checked because repeated observations could bias the model by over-representing certain species.

## Step 4: Target Column (Auto-detect)
"""

possible_targets = [col for col in df.columns if 'status' in col.lower() or 'risk' in col.lower()]

possible_targets

"""## Step 5: Import Libraries"""

import seaborn as sns
import matplotlib.pyplot as plt

"""## Step 6: Histograms"""

df.hist(figsize=(18,14))
plt.show()

"""## Step 7: Correlation"""

plt.figure(figsize=(10,8))
sns.heatmap(df.corr(numeric_only=True), cmap='coolwarm')
plt.show()

"""The correlation matrix shows that most features are weakly correlated, meaning they provide distinct information. However, a group of human-related factors such as agriculture, pollution, and infrastructure development shows moderate positive correlation, suggesting these threats often occur together and may collectively increase extinction risk. The presence of moderate correlations among human-impact variables suggests that these threats may co-occur, reinforcing their combined association with high-risk classification.

## Step 8: Target Distribution
"""

TARGET = 'High_Risk'

import seaborn as sns
import matplotlib.pyplot as plt

sns.countplot(x=TARGET, data=df)
plt.title("High Risk Distribution")
plt.show()

"""The distribution confirms that there are more species classified as not high risk than high risk. Despite this imbalance, the dataset still contains a substantial number of high-risk species, allowing meaningful analysis.

#Target percentages
"""

target_counts = df["High_Risk"].value_counts()
target_percent = df["High_Risk"].value_counts(normalize=True) * 100

pd.DataFrame({
    "count": target_counts,
    "percent": target_percent.round(2)
})

"""The target distribution shows a moderate class imbalance. This indicates that evaluation metrics beyond accuracy, such as precision, recall, F1-score, and ROC-AUC, will be important for model assessment."""

df['High_Risk'].value_counts()

"""The target variable shows a moderate class imbalance, with more species classified as not high risk (0) than high risk (1). However, both classes are well represented, making the dataset suitable for classification analysis.

#Step 9: Key Drivers of Extinction Risk
"""

df.select_dtypes(include=['int64','float64']).columns

features = [
    'Agriculture',
    'Pollution',
    'Climate_ongoing',
    'Invasive_species',
    'Over-exploitation'
]

for col in features:
    plt.figure()
    sns.barplot(x='High_Risk', y=col, data=df)
    plt.title(f"{col} vs High Risk")
    plt.ylim(0,1)
    plt.show()

"""Agriculture

Species exposed to agricultural pressures show a higher likelihood of being classified as high risk, suggesting that land use changes and habitat modification are associated with higher-risk classification.

Pollution

Pollution is strongly associated with increased extinction risk, as species exposed to environmental contamination are more frequently classified as high risk.

 Climate (ongoing)

Ongoing climate change appears to contribute to higher extinction risk, indicating that changing environmental conditions play a critical role in species vulnerability.

Invasive species

The presence of invasive species is linked to higher extinction risk, likely due to increased competition and ecosystem disruption affecting native species.

Over-exploitation

Over-exploitation is strongly associated with high-risk classification, suggesting that human-driven resource use significantly threatens species survival.

Target explanation

The target variable shows a moderate class imbalance, with more species classified as not high risk than high risk. However, both classes are sufficiently represented, making the dataset suitable for classification analysis

#Grouped means for threat variables
"""

threat_cols = [
    "Agriculture",
    "Pollution",
    "Climate_ongoing",
    "Invasive_species",
    "Over-exploitation"
]

df.groupby("High_Risk")[threat_cols].mean().T

"""The grouped means compare the average presence of each threat variable for low-risk and high-risk species. This supports the visual analysis by showing whether high-risk species have higher average exposure to specific threats. Across all threat variables, high-risk species consistently show higher average values, indicating a clear and consistent pattern of increased exposure to environmental and human pressures.

Among the analyzed features, agriculture and pollution appear to show stronger differences between high-risk and low-risk species compared to other variables, suggesting they may be more influential predictors.

#Geography analysis
"""

geo_cols = [
    "Afrotropical",
    "Australasian/Oceanian",
    "Indomalayan",
    "Nearctic",
    "Neotropical",
    "Palearctic"
]

df.groupby("High_Risk")[geo_cols].mean().T

"""Geographic indicators were compared across the target classes to examine whether species from certain regions are more frequently associated with high-risk classification.

# Biology analysis
"""

bio_cols = [
    "Egg_Laying",
    "Free_Living_Larval_Stage",
    "Live_Birth",
    "Water_Breeding"
]

df.groupby("High_Risk")[bio_cols].mean().T

"""Biological traits were compared across risk groups to check whether reproductive or life-stage characteristics are associated with high-risk status.

#**Conclusion**


The EDA suggests that high-risk species tend to show higher average exposure to multiple human-impact and environmental threat indicators, including pollution, agriculture, climate-related pressures, invasive species, and over-exploitation. These factors consistently show stronger associations with high-risk classification. However, these relationships should be interpreted as associations rather than causal effects, as the dataset reflects expert assessments rather than controlled observations.

These findings provide a strong foundation for feature selection and support the use of classification models in the next stage of the project.

# ==============================
# 2. TRAIN / TEST SPLIT
# ==============================
"""

# recreate the SAME split used in modeling (20% test set)
from sklearn.model_selection import train_test_split

_, X_test = train_test_split(df, test_size=0.2, stratify=df['High_Risk'], random_state=42)

# plot class distribution of TEST SET
sns.countplot(x='High_Risk', data=X_test)
plt.title("Class Distribution of Test Set")
plt.xticks([0,1], ['Low Risk','High Risk'])
plt.ylabel("Number of Species")
plt.xlabel("Risk Category")
plt.show()

df['High_Risk'].value_counts()


