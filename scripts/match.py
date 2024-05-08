import pandas as pd
import geopandas as gpd
import re


def clean_string(s):
    """Clean strings by lowering case, removing specific keywords, and non-alphabetic characters."""
    s = (
        s.lower()
        .replace(" district", "")
        .replace(" county", "")
        .replace(" ed", "")
        .replace(" and ", "")
        .replace(" & ", "")
        .replace(" ward", "")
    )
    s = re.sub(r"\(.*?\)|[^a-z\s]", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


# Load and preprocess datasets
britain_elects_df = pd.read_csv("data/results/BritainElects_Results.csv", skiprows=3)
britain_elects_df.columns = britain_elects_df.columns.str.replace(
    "\n", " ", regex=True
).str.strip()
britain_elects_df = britain_elects_df[
    britain_elects_df["Local authority"].notna() & britain_elects_df["Ward"].notna()
]
britain_elects_df["Local authority"] = britain_elects_df["Local authority"].apply(
    clean_string
)
britain_elects_df["Ward"] = britain_elects_df["Ward"].apply(clean_string)

election_maps_df = pd.read_csv("data/results/ElectionMaps_Results.csv")
wards_gdf = gpd.read_file("data/maps/wards.geojson")
merged_maps_wards = pd.merge(
    election_maps_df, wards_gdf, left_on="Ward Code", right_on="Census_Code"
)
merged_maps_wards["Council"] = merged_maps_wards["Council"].apply(clean_string)
merged_maps_wards["Ward Name"] = merged_maps_wards["Ward Name"].apply(clean_string)

# Merge datasets
final_merged_df = pd.merge(
    britain_elects_df,
    merged_maps_wards,
    left_on=["Local authority", "Ward"],
    right_on=["Council", "Ward Name"],
    how="inner",
)

# Select and rename columns
result_df = final_merged_df[
    ["Ward Code", "Ward Name", "Council", "Defending (20XX)", "Leading (2023)"]
]
result_df.columns = ["Ward Code", "Ward Name", "Council Name", "Defending", "Leading"]

# Save the result
result_df.to_csv("output/filtered_results.csv", index=False)
print(result_df.head())
