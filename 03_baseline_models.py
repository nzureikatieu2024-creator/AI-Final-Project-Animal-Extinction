# Step 3 — Baseline Models

The goal of this section is to run baseline classification models on the cleaned amphibian dataset and produce the first results table for the group.

These results are preliminary holdout benchmarks only. They are not used for final model selection or hyperparameter tuning. Final model selection will be performed using cross-validation inside the training set, and the test set will be used only once at the end for final evaluation.

## Dataset Loading
"""

# ==============================
# 4. BASELINE MODELS
# ==============================

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer

from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

# ------------------------------------------------
# Dataset
# ------------------------------------------------
# Assumes df has already been loaded and columns have already been renamed
# in the earlier pipeline section.

print("Dataset shape:", df.shape)
print("\nTarget distribution:")
print(df["High_Risk"].value_counts())

print("\nTarget proportions:")
print(df["High_Risk"].value_counts(normalize=True).round(3))

# ------------------------------------------------
# Train-test split
# ------------------------------------------------
X = df.drop(columns=["High_Risk", "Species_Name"])
y = df["High_Risk"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

print("Training set:", X_train.shape)
print("Test set:", X_test.shape)

print("\nTrain target distribution:")
print(y_train.value_counts(normalize=True).round(3))

print("\nTest target distribution:")
print(y_test.value_counts(normalize=True).round(3))

# ------------------------------------------------
# Feature sets — aligned with group pipeline
# ------------------------------------------------
TAXONOMY_FEATURES = [
    "Order",
    "Family"
]

GEOGRAPHY_FEATURES = [
    "Afrotropical",
    "Australasian/Oceanian",
    "Indomalayan",
    "Nearctic",
    "Neotropical",
    "Palearctic"
]

BIOLOGY_FEATURES = [
    "Egg_Laying",
    "Free_Living_Larval_Stage",
    "Live_Birth",
    "Water_Breeding"
]

THREAT_FEATURES = [
    "Agriculture",
    "Timber_and_plant_harvesting",
    "Infrastructure_development",
    "Pollution",
    "Mining_energy_production",
    "Water_management",
    "Human_disturbance",
    "Geological_Events",
    "Over-exploitation",
    "Climate_ongoing",
    "Climate_future",
    "Fire",
    "Bd_future",
    "Bd_ongoing",
    "Bsal_future",
    "Bsal_ongoing",
    "Invasive_species",
    "Natives_species"
]

PIPELINE_A_FEATURES = TAXONOMY_FEATURES + GEOGRAPHY_FEATURES + BIOLOGY_FEATURES
PIPELINE_B_FEATURES = PIPELINE_A_FEATURES + THREAT_FEATURES

feature_sets = {
    "Pipeline A - Restricted": PIPELINE_A_FEATURES,
    "Pipeline B - Full": PIPELINE_B_FEATURES
}

for name, features in feature_sets.items():
    print(name, "feature count:", len(features))

# ------------------------------------------------
# Preprocessing
# ------------------------------------------------
def build_preprocessor(feature_list):
    categorical_cols = [col for col in feature_list if col in ["Order", "Family"]]
    binary_cols = [col for col in feature_list if col not in categorical_cols]

    categorical_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    binary_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="constant", fill_value=0))
    ])

    transformers = []

    if categorical_cols:
        transformers.append(("categorical", categorical_pipeline, categorical_cols))

    if binary_cols:
        transformers.append(("binary", binary_pipeline, binary_cols))

    preprocessor = ColumnTransformer(
        transformers=transformers,
        remainder="drop"
    )

    return preprocessor

# ------------------------------------------------
# Baseline models
# ------------------------------------------------
models = {
    "Dummy Classifier": DummyClassifier(strategy="most_frequent"),
    "Logistic Regression": LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42
    ),
    "Decision Tree": DecisionTreeClassifier(
        class_weight="balanced",
        random_state=42
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    ),
    "Gradient Boosting": GradientBoostingClassifier(
        random_state=42
    )
}

# ------------------------------------------------
# Evaluation function
# ------------------------------------------------
def evaluate_model(model, X_train, X_test, y_train, y_test, feature_list):
    preprocessor = build_preprocessor(feature_list)

    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ])

    pipeline.fit(X_train[feature_list], y_train)

    y_pred = pipeline.predict(X_test[feature_list])

    if hasattr(pipeline.named_steps["model"], "predict_proba"):
        y_prob = pipeline.predict_proba(X_test[feature_list])[:, 1]
        roc_auc = roc_auc_score(y_test, y_prob)
    else:
        roc_auc = np.nan

    results = {
        "Accuracy": accuracy_score(y_test, y_pred),
        "Balanced Accuracy": balanced_accuracy_score(y_test, y_pred),
        "F1": f1_score(y_test, y_pred, zero_division=0),
        "Recall": recall_score(y_test, y_pred, zero_division=0),
        "Precision": precision_score(y_test, y_pred, zero_division=0),
        "ROC-AUC": roc_auc
    }

    return results, pipeline

# ------------------------------------------------
# Run baseline models
# ------------------------------------------------
all_results = []
trained_pipelines = {}

for feature_set_name, feature_list in feature_sets.items():
    print(f"Running models for feature set: {feature_set_name}")

    for model_name, model in models.items():
        results_dict, pipeline = evaluate_model(
            model=model,
            X_train=X_train,
            X_test=X_test,
            y_train=y_train,
            y_test=y_test,
            feature_list=feature_list
        )

        results_dict["Feature Set"] = feature_set_name
        results_dict["Model"] = model_name

        all_results.append(results_dict)
        trained_pipelines[(feature_set_name, model_name)] = pipeline

print("All baseline models finished.")

# ------------------------------------------------
# Results table
# ------------------------------------------------
results_table = pd.DataFrame(all_results)

results_table = results_table[
    [
        "Feature Set",
        "Model",
        "Accuracy",
        "Balanced Accuracy",
        "F1",
        "Recall",
        "Precision",
        "ROC-AUC"
    ]
]

results_table = results_table.sort_values(
    by=["Feature Set", "F1"],
    ascending=[True, False]
).round(3)

display(results_table)

# ------------------------------------------------
# Save results
# ------------------------------------------------
results_table.to_csv(OUTPUTS_DIR / "haya_baseline_results.csv", index=False)

print("Saved results as haya_baseline_results.csv")

"""## Baseline Results Interpretation

The baseline models provide the first benchmark for the project. The Dummy Classifier represents the zero-rule baseline because it predicts the majority class without using input features.

The Logistic Regression model provides a simple linear baseline, while Decision Tree, Random Forest, and Gradient Boosting capture non-linear relationships and feature interactions.

The full feature set generally performs better than the restricted set, suggesting that threat-related variables add predictive value for extinction risk.

These results are preliminary and will be used for further hyperparameter tuning and final evaluation.

The results show that models trained on the full feature set consistently outperform those using the restricted set, indicating that threat-related variables significantly improve predictive performance. Among the models, ensemble methods such as Random Forest and Gradient Boosting achieve the highest F1 scores, suggesting that capturing non-linear relationships and feature interactions is important for this classification task.

The full feature set performs much better than the restricted set, suggesting that threat variables provide strong predictive signal. However, these results must be interpreted carefully because some threat indicators may be linked to the same expert assessment process used to assign Red List categories. Therefore, the restricted model is a cleaner early-indicator benchmark, while the full model shows the added predictive value of recorded threat information.

Overall, this section provides valid initial benchmarks, but final conclusions should only be made after cross-validation-based tuning and a single final evaluation on the test set.

### Extra — Baseline Models

For Step 3, I trained baseline classification models on the cleaned amphibian dataset. I used a Dummy Classifier, Logistic Regression, Decision Tree, Random Forest, and Gradient Boosting model. These models were tested on both the restricted feature set and the full feature set.

The purpose of this step was not to tune the models, but to create an initial benchmark for the group. The Dummy Classifier provides the zero-rule baseline, while the other models show whether the available features contain predictive signal for extinction risk.

The resulting table reports F1 score, precision, recall, and ROC-AUC. These results will be used by the next team member for hyperparameter tuning and later by Noor for final evaluation and insights.
"""
