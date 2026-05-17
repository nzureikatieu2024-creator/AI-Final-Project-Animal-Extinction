# AI-Final-Project-Animal-Extinction
By: Noor Zureikat, Karim Junadi, Hamza Madi, Tina Haddad, Mohamed Embaby and Haya Mourad

## Project Overview

This project uses machine learning to predict whether an amphibian species is at high extinction risk based on biological, taxonomic, geographic, and threat-related indicators.

The goal of the project is not only to build the highest-performing model, but also to evaluate which features provide meaningful and reliable early indicators of extinction risk.

The final target variable is:

- `High_Risk = 1`: species classified as vulnerable, endangered, critically endangered, or possibly extinct
- `High_Risk = 0`: species classified as least concern or near threatened

The project compares two main feature sets:

1. **Restricted feature set**
   - Taxonomy
   - Geography
   - Biological traits

2. **Full feature set**
   - Restricted features
   - Threat-related variables

The full feature set performs best numerically, but the restricted model is used for the final conservative interpretation because some threat variables may be closely connected to the Red List assessment process.

---

## Important Note About the Files

The individual Python files are included as **evidence of each team member’s contribution** and to show the development process of the project.

However, the file that should be run for the final project output is:

```text
final_pipeline.py
