import pandas as pd

# Load the datasets
deprivation_df = pd.read_csv("output/ward_deprivation.csv")
results_df = pd.read_csv("output/Filtered_Results.csv")

# Standardize column names
deprivation_df.rename(columns={"Ward_Code": "Ward Code"}, inplace=True)

# Merge the datasets on Ward Code
merged_df = pd.merge(results_df, deprivation_df, on="Ward Code")

# Calculate deciles for the deprivation scores
merged_df["Decile"] = pd.qcut(merged_df["Deprivation Score"], 10, labels=False) + 1

# Define the main parties
main_parties = ["Con", "Lab", "LDem", "Grn", "Ind"]

# Initialize an empty list to collect DataFrame rows
results_list = []

# Process each decile
for decile in range(1, 11):
    decile_data = {"Decile": decile}
    total_other_changes = 0

    # Calculate net changes for each party
    for party in merged_df["Leading"].unique():
        defending_mask = (merged_df["Decile"] == decile) & (
            merged_df["Defending"] == party
        )
        leading_mask = (merged_df["Decile"] == decile) & (merged_df["Leading"] == party)

        losses = (
            (defending_mask) & (merged_df["Defending"] != merged_df["Leading"])
        ).sum()
        gains = (
            (leading_mask) & (merged_df["Defending"] != merged_df["Leading"])
        ).sum()

        net_change = gains - losses

        if party in main_parties:
            decile_data[party] = net_change
        else:
            total_other_changes += net_change

    # Add the total changes for 'Other' parties
    decile_data["Other"] = total_other_changes

    # Append decile data to the list
    results_list.append(decile_data)

# Convert list to DataFrame
results_df = pd.DataFrame(results_list)

# Save the results to a CSV file
results_df.to_csv("output/party_gains_losses_by_decile.csv", index=False)
