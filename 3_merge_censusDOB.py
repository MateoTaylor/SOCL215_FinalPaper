import pandas as pd

'''

THIS MERGES CENSUS DATA WITH DOB DATA

Output: 3 CSV files, 
    one for each timeframe and one for both timeframes combined

'''


timeframes = ["2010-2014", "2015-2019"]
census_data = pd.read_csv(f"brooklyn_acs_tracts.csv")
compiled_data = pd.DataFrame()

# since the census data has seperate columns for state/county/tract, we need to combine for it
census_data["BoroCT2010"] = (
    "3" + census_data["tract"].astype(str).str.zfill(6) # boro code is 3 for Brooklyn
)
census_data["BoroCT2010"] = census_data["BoroCT2010"].astype('int64')

for timeframe in timeframes:    
    # Load the DOB data
    dob_data = pd.read_csv(f"Building_Blocks/DOB_{timeframe}.csv")
    period_data = census_data[census_data["acs_period"] == timeframe]

    # Merge the two datasets on the GEOID column
    merged_data = pd.merge(dob_data, period_data, on="BoroCT2010", how="left")

    # since our DOB data has all 5 boroughs but we only want Brooklyn, we need to filter
    merged_data = merged_data[merged_data["county"] == 47]

    # Save the merged data to a new CSV file
    merged_data.to_csv(f"Building_Blocks/Housing_on_Census_{timeframe}.csv", index=False, mode='w')
    print(f"Saved merged data for {timeframe} to Building_Blocks/Housing_on_Census_{timeframe}.csv")

    # Append the merged data to the compiled_data DataFrame
    compiled_data = pd.concat([compiled_data, merged_data], ignore_index=True)
compiled_data.to_csv("Final_Results/Housing_on_Census_FULL.csv", index=False)

