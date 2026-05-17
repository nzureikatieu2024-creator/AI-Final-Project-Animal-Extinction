import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

amphibians = pd.read_excel(
    DATA_DIR / "All_amphibians_tabular_data.xlsx",
    sheet_name="Red listing, realms, breeding"
)

threats = pd.read_excel(
    DATA_DIR / "Threats_to_Threatened_Species.xlsx",
    sheet_name="Sheet1"
)

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

valid_categories = ["LC", "NT", "VU", "EN", "CR", "CR(PE)", "CR(PEW)"]

amphibians = amphibians[
    amphibians["2022 GAA2 Red List Category"].isin(valid_categories)
].copy()

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

threats = threats.drop(columns=["2022 GAA2 Red List Category"], errors="ignore")

threat_columns = [col for col in threats.columns if col != "Species Name"]

for col in threat_columns:
    threats[col] = threats[col].fillna(0).astype(int)

amphibian_cleaned = amphibians.merge(
    threats,
    on="Species Name",
    how="left"
)

for col in threat_columns:
    amphibian_cleaned[col] = amphibian_cleaned[col].fillna(0).astype(int)

high_risk_categories = ["VU", "EN", "CR", "CR(PE)", "CR(PEW)"]

amphibian_cleaned["High_Risk"] = (
    amphibian_cleaned["2022 GAA2 Red List Category"]
    .isin(high_risk_categories)
    .astype(int)
)

amphibian_cleaned = amphibian_cleaned.drop(
    columns=["2022 GAA2 Red List Category"]
)
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
    "Natives species": "Natives_species",

    "Over exploitation": "Over-exploitation",
    "Over-exploitation": "Over-exploitation",
    "Agriculture": "Agriculture",
    "Pollution": "Pollution",
    "Fire": "Fire"
})


print("Final cleaned dataset created successfully.")
print("Shape:", amphibian_cleaned.shape)
print("Columns:")
print(amphibian_cleaned.columns.tolist())
print(amphibian_cleaned.head())

expected_columns = [
    "Order",
    "Family",
    "Species_Name",
    "Afrotropical",
    "Australasian/Oceanian",
    "Indomalayan",
    "Nearctic",
    "Neotropical",
    "Palearctic",
    "Egg_Laying",
    "Free_Living_Larval_Stage",
    "Live_Birth",
    "Water_Breeding",
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
    "Natives_species",
    "High_Risk"
]

missing = [col for col in expected_columns if col not in amphibian_cleaned.columns]

if missing:
    print("Missing columns:", missing)
else:
    print("All expected final pipeline columns are present.")

amphibian_cleaned.to_excel(DATA_DIR / "amphibian_cleaned.xlsx", index=False)
