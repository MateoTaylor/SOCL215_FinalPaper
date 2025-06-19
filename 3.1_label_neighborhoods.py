import pandas as pd

# attaching label to tracts in prospect park lefferts + prospect park south

# CTlabel of Prospect Lefferts = 798.02, 798.01, 802, 800, 327, 213, 325, 323x
# CTlabel of PPS = 1522, 506, 512, 510.02, 510.01, 508.01, 508.03, 508.04, 492, 796.02, 796.01

timeframes = ["2010-2014", "2015-2019"]

for timeframe in timeframes:
    housing_data = pd.read_csv(f"Building_Blocks/Housing_on_Census_{timeframe}.csv")
    # Create a new column 'neighborhood' and set default value to 'other'
    housing_data['park_adjacent'] = 0 
    # Define the neighborhoods and their corresponding CT labels
    neighborhoods = {
    1: ['3079802', '3079801', '3080200', '3080000', '3032700', '3021300', '3032500', '3032300','3152200', '3050600', '3051200', '3051002', '3051001', '3050801', '3050803', '3050804', '3049200', '3079602', '3079601']
    }
    # Iterate through the neighborhoods and assign the label
    for neighborhood, labels in neighborhoods.items():
        # Update the 'neighborhood' column where 'BoroCT2010' matches any of the labels
        housing_data.loc[housing_data['BoroCT2010'].astype(str).isin(labels), 'park_adjacent'] = neighborhood
    # Save the updated DataFrame back in
    housing_data.to_csv(f"Building_Blocks/Housing_on_Census_{timeframe}.csv", index=False)
    print(f"Updated {timeframe} data with neighborhood labels.")

# Now update the full dataset
compiled_data = pd.read_csv("Final_Results/Housing_on_Census_FULL.csv")
compiled_data['park_adjacent'] = 0 
# Define the neighborhoods and their corresponding CT labels
neighborhoods = {
    1: ['3079802', '3079801', '3080200', '3080000', '3032700', '3021300', '3032500', '3032300','3152200', '3050600', '3051200', '3051002', '3051001', '3050801', '3050803', '3050804', '3049200', '3079602', '3079601']
}
# Iterate through the neighborhoods and assign the label
for neighborhood, labels in neighborhoods.items():
    # Update the 'neighborhood' column where 'BoroCT2010' matches any of the labels
    compiled_data.loc[compiled_data['BoroCT2010'].astype(str).isin(labels), 'park_adjacent'] = neighborhood
# Save the updated DataFrame back in
compiled_data.to_csv("Final_Results/Housing_on_Census_FULL.csv", index=False)
print("Updated full dataset with neighborhood labels.")