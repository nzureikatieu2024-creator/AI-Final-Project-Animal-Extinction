import pandas as pd
from pathlib import Path

# Set paths
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Load the two original Excel files
amphibians = pd.read_excel(
    DATA_DIR / "All_amphibians_tabular_data.xlsx",
    sheet_name="Red listing, realms, breeding"
)

threats = pd.read_excel(
    DATA_DIR / "Threats_to_Threatened_Species.xlsx",
    sheet_name="Sheet1"
)

# Keep the columns we need from the amphibian dataset
base_columns = [
    "Order",
    "Family",
    "Species Name",
    "Afrotropical",
    "Australasian/Oceanian",
    "Indomalayan",
    "Nearctic",
    "Neotropical",
    "Palearctic",
    "Egg Laying",
    "Free Living Larval Stage",
    "Live Birth ",
    "Water Breeding",
    "2022 GAA2 Red List Category"
]

amphibians = amphibians[base_columns]

# Remove categories that are not useful for our binary model
valid_categories = ["LC", "NT", "VU", "EN", "CR", "CR(PE)", "CR(PEW)"]

amphibians = amphibians[
    amphibians["2022 GAA2 Red List Category"].isin(valid_categories)
].copy()

# Convert breeding columns from Yes/No to 1/0
breeding_columns = [
    "Egg Laying",
    "Free Living Larval Stage",
    "Live Birth ",
    "Water Breeding"
]

for col in breeding_columns:
    amphibians[col] = (
        amphibians[col]
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("yes")
        .astype(int)
    )

# Fill missing values in realm columns with 0
realm_columns = [
    "Afrotropical",
    "Australasian/Oceanian",
    "Indomalayan",
    "Nearctic",
    "Neotropical",
    "Palearctic"
]

for col in realm_columns:
    amphibians[col] = amphibians[col].fillna(0).astype(int)

# Clean the threats dataset
threats = threats.drop(columns=["2022 GAA2 Red List Category"], errors="ignore")

threat_columns = [col for col in threats.columns if col != "Species Name"]

for col in threat_columns:
    threats[col] = threats[col].fillna(0).astype(int)

# Merge both datasets using species name
amphibian_cleaned = amphibians.merge(
    threats,
    on="Species Name",
    how="left"
)

# Fill missing threat values after the merge with 0
for col in threat_columns:
    amphibian_cleaned[col] = amphibian_cleaned[col].fillna(0).astype(int)

# Create the binary target variable
high_risk_categories = ["VU", "EN", "CR", "CR(PE)", "CR(PEW)"]

amphibian_cleaned["High_Risk"] = (
    amphibian_cleaned["2022 GAA2 Red List Category"]
    .isin(high_risk_categories)
    .astype(int)
)

# Drop the original Red List column because High_Risk is now the target
amphibian_cleaned = amphibian_cleaned.drop(
    columns=["2022 GAA2 Red List Category"]
)

# Rename columns to make them easier to use in Python
amphibian_cleaned = amphibian_cleaned.rename(columns={
    "Species Name": "Species_Name",

    "Egg Laying": "Egg_Laying",
    "Free Living Larval Stage": "Free_Living_Larval_Stage",
    "Live Birth ": "Live_Birth",
    "Water Breeding": "Water_Breeding",

    "Timber and plant harvesting": "Timber_and_plant_harvesting",
    "Infrastructure development": "Infrastructure_development",
    "Mining/energy production": "Mining_energy_production",
    "Water management": "Water_management",
    "Human disturbance": "Human_disturbance",
    "Geological Events": "Geological_Events",

    "Climate (ongoing)": "Climate_ongoing",
    "Climate (future)": "Climate_future",

    "Bd (future)": "Bd_future",
    "Bd (ongoing)": "Bd_ongoing",
    "Bsal (future)": "Bsal_future",
    "Bsal (ongoing)": "Bsal_ongoing",

    "Invasive species": "Invasive_species",
    "Natives species": "Natives_species"
})

# Save the final cleaned dataset inside the data folder
amphibian_cleaned.to_excel(DATA_DIR / "amphibian_cleaned.xlsx", index=False)

print("Final cleaned dataset created successfully.")
print("Shape:", amphibian_cleaned.shape)
print("Columns:")
print(amphibian_cleaned.columns.tolist())
print(amphibian_cleaned.head())
