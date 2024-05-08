import pandas as pd

# Load the lookup table
lookup_table = pd.read_csv("output/lookup_table.csv")

# Load the population data
population_data = pd.read_csv("data/population.csv")

# Load the deprivation data from the Excel file
deprivation_data = pd.read_excel(
    "source/deprivation.xlsx", sheet_name="UK_IMD_E", usecols=["lsoa", "UK_IMD_E_score"]
)

# Merge the lookup table with the population data
merged_data = pd.merge(
    lookup_table,
    population_data,
    left_on="Small_Area",
    right_on="area_code",
    how="left",
)

# Merge the merged data with the deprivation data
merged_data = pd.merge(
    merged_data, deprivation_data, left_on="Small_Area", right_on="lsoa", how="left"
)

# Calculate the weighted population based on overlap proportion
merged_data["weighted_population"] = (
    merged_data["population"] * merged_data["overlap_proportion"]
)

# Filter out rows with missing Ward_Code and Ward_Name
merged_data = merged_data[
    merged_data["Ward_Code"].notna() | merged_data["Ward_Name"].notna()
]

# Calculate the weighted average rank of deprivation for each ward
ward_deprivation_code = (
    merged_data[merged_data["Ward_Code"].notna()]
    .groupby(["Ward_Code"], as_index=False)
    .apply(
        lambda x: pd.Series(
            {
                "Ward_Code": x["Ward_Code"].iloc[0],
                "Ward_Name": "",
                "Deprivation Score": (
                    x["weighted_population"] * x["UK_IMD_E_score"]
                ).sum()
                / x["weighted_population"].sum(),
            }
        )
    )
)

ward_deprivation_name = (
    merged_data[merged_data["Ward_Name"].notna()]
    .groupby(["Ward_Name"], as_index=False)
    .apply(
        lambda x: pd.Series(
            {
                "Ward_Code": "",
                "Ward_Name": x["Ward_Name"].iloc[0],
                "Deprivation Score": (
                    x["weighted_population"] * x["UK_IMD_E_score"]
                ).sum()
                / x["weighted_population"].sum(),
            }
        )
    )
)

# Combine the results
ward_deprivation = pd.concat(
    [ward_deprivation_code, ward_deprivation_name], ignore_index=True
)

# Save the result to a new CSV file
ward_deprivation.to_csv("output/ward_deprivation.csv", index=False)
