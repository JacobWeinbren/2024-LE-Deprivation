import geopandas as gpd

print("Reading files...")
small_areas = gpd.read_file("data/maps/small_areas.geojson")
england_wards = gpd.read_file("data/maps/wards.geojson")

print("Performing Spatial Join...")
england_joined = gpd.sjoin(
    small_areas, england_wards, how="inner", predicate="intersects"
)

print("Calculating overlap areas...")
england_joined["overlap_area"] = england_joined.geometry.intersection(
    england_joined.geometry
).area

print("Calculating overlap proportions...")
england_joined["overlap_proportion"] = england_joined[
    "overlap_area"
] / england_joined.groupby("geo_code")["overlap_area"].transform("sum")

print("Selecting and renaming columns...")
lookup_table = england_joined[["geo_code", "Census_Code", "Name", "overlap_proportion"]]
lookup_table.rename(
    columns={"geo_code": "Small_Area", "Census_Code": "Ward_Code", "Name": "Ward_Name"},
    inplace=True,
)

print("Saving File...")
lookup_table.to_csv("output/lookup_table.csv", index=False)
