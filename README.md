# LE Deprivation Project

This project uses various datasets and scripts to analyse and visualise local election results and deprivation data across different wards.

## Imported Datasets

The project includes the following datasets:

-   `population.csv`: Population data.
-   `small_area.geojson`: GeoJSON file for small areas.
-   `deprivation.xlsx`: Deprivation indices.

These files are sourced from the Ward-Deprivation Github project.

## Data Sources

### Election Data

Election results data are sourced from:

-   [2024 Local Election Results (Britain Elects aggregate)](https://docs.google.com/spreadsheets/d/1ykzMwrloKCk3NmZAeWV1AaQAP22WtczfqxI2sq_VD2c/edit#gid=0)
-   [LE2024 Results](https://docs.google.com/spreadsheets/d/1iKB61smRmRaOQS6hEB8p15xQYFBlg87z6KcB4C0MYWk/edit#gid=0)

### Ward Boundary Data

Ward boundary data is obtained from:

-   [OS Data Hub - Boundary Line](https://osdatahub.os.uk/downloads/open/BoundaryLine)

## Scripts

### lookup.py

Performs spatial joins between small areas and wards to create a lookup table. It calculates the overlap between areas and outputs the results in a CSV file.

### match.py

Processes election results from two sources, cleans and merges them based on ward names and local authority. Outputs a CSV file with the merged results.