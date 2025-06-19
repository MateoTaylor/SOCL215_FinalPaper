
# Calculates percent change between values in timeframes 2010-2014 and 2015-2019

import pandas as pd

# Read the CSV file
period1_data = pd.read_csv("Building_Blocks/Housing_on_Census_2010-2014.csv")
period2_data = pd.read_csv("Building_Blocks/Housing_on_Census_2015-2019.csv")

variables = [
    "inf_med_hh_income",
    "inf_med_rent",
    "inf_med_home_value",
    "black",
    "total_pop",
    "white",
    "Units Added",
    "total_hh",
    "owner_occ_units",
]

# Calculate percent change for each variable
for variable in variables:
    if variable in period1_data.columns and variable in period2_data.columns:
        # go row by row and calculate the percent change
        for index, row in period1_data.iterrows():
            if period1_data.at[index, variable] != 0:
                matching_row = period2_data[period2_data['BoroCT2010'] == row['BoroCT2010']]
                if not matching_row.empty:
                    period1_data.at[index, f"{variable}_pct_change"] = (
                        (matching_row.iloc[0][variable] - row[variable]) / row[variable]
                    ) * 100
                else:
                    period1_data.at[index, f"{variable}_pct_change"] = pd.NA
            else:
                period1_data.at[index, f"{variable}_pct_change"] = pd.NA
    else:
        print(f"Variable '{variable}' not found in both datasets.")
    

# Save the updated DataFrame to a new CSV file
period1_data.to_csv("Building_Blocks/Housing_on_Census_2010-2014.csv", index=False)
print("DONE!!!!")