import geopandas as gpd
import pandas as pd

# Load shapefile
tracts = gpd.read_file('geo_json/nyct2010.shp').to_crs(epsg=4326)
timeframes = ["2010-2014", "2015-2019"]

for timeframe in timeframes:
# Load your CSV
    data = pd.read_csv(f'Building_Blocks/Housing_on_Census_{timeframe}.csv')

    # Ensure the GEOID column exists in both dataframes
    tracts.columns = tracts.columns.str.strip()
    data.columns = data.columns.str.strip()

    # Convert GEOID columns to the same data type (string)
    tracts['BoroCT2010'] = tracts['BoroCT2010'].astype(str)
    data['BoroCT2010'] = data['BoroCT2010'].astype(str)

    # Merge on GEOID
    merged = tracts.merge(data, on='BoroCT2010')

    # remove any rows not in Brooklyn
    merged = merged[merged['county'] == 47]

    # Save to GeoJSON
    merged.to_file(f'Final_Results/{timeframe}_tracts.geojson', driver='GeoJSON')

print("GeoJSON files created successfully!")

