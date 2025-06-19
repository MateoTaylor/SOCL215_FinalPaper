import requests
import pandas as pd

API_KEY = '----'

# Map end‐year to human label
periods = {
    '2015': '2010-2014',
    '2019': '2015-2019'
}

vars_defs = {
    'total_pop':       'B01003_001E',
    'total_hh':        'B11001_001E',
    'housing_units':   'B25001_001E',
    'vacant_units':    'B25002_003E',
    'occupied_units':  'B25003_001E',
    'owner_occ_units': 'B25003_002E',
    'med_hh_income':     'B19013_001E',
    'med_family_income': 'B19113_001E',
    'per_capita_inc':    'B19301_001E',
    'med_home_value':    'B25077_001E',
    'pop_in_pov':    'B17001_002E',
    'pop_pov_univ':  'B17001_001E',
    'fam_in_pov':    'B17010_002E',
    'fam_pov_univ':  'B17010_001E',
    'foreign_born': 'B05002_013E',
    'foreign_univ': 'B05002_001E',
    'sf_units':   'B25024_002E',
    'du_units':   'B25024_003E',
    'm19_units':  ['B25024_004E','B25024_005E','B25024_006E','B25024_007E'], 
    'm50_units':  'B25024_008E',
    'unit_univ':  'B25024_001E',
    'white':      'B02001_002E',
    'black':      'B02001_003E',
    'asian':      'B02001_005E',
    'other_race': 'B02001_007E',
    'two_more':   'B02001_008E',
    'hisp_lat':     'B03001_003E',
    'mexican':      'B03001_004E',
    'puerto_rican': 'B03001_005E',
    'cuban':        'B03001_006E',
    'med_rent': 'B25064_001E',
}

geo_fields = {'state', 'county', 'tract'}

all_dfs = []

for year, label in periods.items():
    print(f"Pulling ACS {label} (vintage {year})…")

    # Get available variables for this vintage
    var_url = f'https://api.census.gov/data/{year}/acs/acs5/variables.json'
    resp = requests.get(var_url, params={'key': API_KEY})
    resp.raise_for_status()
    available = set(resp.json()['variables'].keys())
    print(f"  Found {len(available)} variables in vintage {year}.")

    # Flatten vars_defs.values() to handle both strings and lists
    all_vars = {item for value in vars_defs.values() for item in (value if isinstance(value, list) else [value])}
    missing = all_vars - available
    print(f"  Missing {len(missing)} variables: {missing}")
    if missing:
        print("  Exiting.")
        exit(1)

    # Pull data
    data_url = f"https://api.census.gov/data/{year}/acs/acs5"
    params = {
        "get": "NAME," + ",".join(all_vars),
        "for": "tract:*",
        "in": "state:36+county:047",
        "key": API_KEY
    }
    resp = requests.get(data_url, params=params)
    resp.raise_for_status()
    data = resp.json()

    # Convert to DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])
    # Convert numeric columns to integers before replacing invalid values
    numeric_cols = df.columns.difference(['NAME', 'state', 'county', 'tract'])    
    df['acs_period'] = label  # Add ACS period label
    all_dfs.append(df)

#Concatenate and save to CSV
full_df = pd.concat(all_dfs, ignore_index=True)

#  Convert numeric columns to float
cols_to_numeric = full_df.columns.difference(['NAME', 'state', 'county', 'tract', 'acs_period'])
full_df[cols_to_numeric] = full_df[cols_to_numeric].apply(pd.to_numeric, errors='coerce')

# Normalize multi-unit counts using raw codes
full_df['m19_units'] = full_df[['B25024_004E','B25024_005E','B25024_006E','B25024_007E']].sum(axis=1)
full_df['m50_units'] = full_df['B25024_008E']

# Drop the raw-code columns
drop_cols = [
    'B25024_004E','B25024_005E','B25024_006E','B25024_007E','B25024_008E'
]
full_df.drop(columns=drop_cols, inplace=True)

# Now build code + label map and rename
code_to_label = {}
for label, codes in vars_defs.items():
    if isinstance(codes, list):
        for code in codes:
            code_to_label[code] = label
    else:
        code_to_label[codes] = label

full_df.rename(columns=code_to_label, inplace=True)

# now set any rows with missing values to NA
full_df.replace([-666666666, -999999999, -333333333, -222222222, 
                 '-666666666', '-999999999', '-333333333', '-222222222'], pd.NA, inplace=True)


full_df.to_csv("brooklyn_acs_tracts.csv", index=False)
print("Saved combined data to brooklyn_acs_tracts.csv")
