import pandas as pd
import csv
import geopandas as gpd


'''
THIS CREATES TWO TIMEFRAMES AND GATHERS DOB DATA WITHIN THEM
'''

if __name__ == "__main__":
    housing_data = pd.read_csv("HousingDB_2010-2020.csv", low_memory=False)
    
    # one column w/ census tracts in each row, then extra empty columns
    ''' columns = BoroCT2010, Year, Units Added, Units Removed, Completed Projects, Avg Initial Units of Projects Completed
            Percent Unit Change	Projects Permitted, Permitted Units Addition, Permitted Units Removal, Avg Initial Units of Projects Permitted
    '''
    timeframes = [[str(year) for year in range(2010, 2015)], [str(year) for year in range(2015, 2020)]]
    for timeframe in timeframes:
        census_db = gpd.read_file('geo_json/nyct2010.shp') 

        # Convert BoroCT2010 columns to the same data type (string)
        if 'BoroCT2010' in census_db.columns:
            census_db['BoroCT2010'] = census_db['BoroCT2010'].astype(str)
        else:
            raise KeyError("The column 'BoroCT2010' does not exist in the census_db DataFrame.")


        required_columns = [
                "Completed Projects", "Avg Initial Units of Projects Completed", 
                "Units Added", "Units Removed", "Permitted Projects", 
                "Avg Initial Units of Projects Permitted", "Permitted Unit Addition", 
                "Permitted Unit Removal"
            ]
        for column in required_columns:
            if column not in census_db.columns:
                census_db[column] = 0

        for year in timeframe:
            # Ensure required columns exist in census_db with default values

            #completed projects in year
            completed_projects = housing_data[housing_data["Job_Status"] == "5. Completed Construction"]
            yearly_data = completed_projects[completed_projects["CompltYear"] == year]
            for index, row in yearly_data.iterrows():
                # Update Completed Projects
                if not ((census_db["BoroCT2010"] == row["BCT2010"]).any()):
                    exit(1)
                census_db.loc[census_db["BoroCT2010"] == row["BCT2010"], "Completed Projects"] += 1

                # Maintain a count of total inital units of projects completed (we'll average at the end)
                census_db.loc[census_db["BoroCT2010"] == row["BCT2010"], "Avg Initial Units of Projects Completed"] += row["ClassAInit"]

                # Update Units Added and Units Removed
                if row["ClassANet"] > 0:
                    census_db.loc[census_db["BoroCT2010"] == row["BCT2010"], "Units Added"] += row["ClassANet"]
                else:
                    census_db.loc[census_db["BoroCT2010"] == row["BCT2010"], "Units Removed"] += row["ClassANet"]

            #permitted projects in year
            completed_projects = housing_data[housing_data["Job_Status"] == "3. Permitted for Construction"]
            yearly_data = completed_projects[completed_projects["PermitYear"] == year]
            for index, row in yearly_data.iterrows():
                # Update Permitted Projects
                census_db.loc[census_db["BoroCT2010"] == row["BCT2010"], "Permitted Projects"] += 1

                # Maintain a count of total inital units of projects completed (we'll average at the end)
                census_db.loc[census_db["BoroCT2010"] == row["BCT2010"], "Avg Initial Units of Projects Permitted"] += row["ClassAInit"]

                # Update Units Added and Units Removed
                if row["ClassANet"] > 0:
                    census_db.loc[census_db["BoroCT2010"] == row["BCT2010"], "Permitted Unit Addition"] += row["ClassANet"]
                else:
                    census_db.loc[census_db["BoroCT2010"] == row["BCT2010"], "Permitted Unit Removal"] += row["ClassANet"]
            
        # Now run through each census tract and average initial units of projects completed and permitted, as well as % unit change
        for index, row in census_db.iterrows():
            if row["Completed Projects"] > 0:
                # Calculate Avg Initial Units of Projects Completed
                census_db.loc[index, "Avg Initial Units of Projects Completed"] = float(round(
                    float(row["Avg Initial Units of Projects Completed"]) / float(row["Completed Projects"]), 2
                ))

                # Calculate Avg Initial Units of Projects Permitted
                if row["Permitted Projects"] > 0:
                    census_db.loc[index, "Avg Initial Units of Projects Permitted"] = float(round(
                        float(row["Avg Initial Units of Projects Permitted"]) / float(row["Permitted Projects"]), 2
                    ))

        # Now drop all non-required columns
        census_db = census_db[["BoroCT2010", "NTACode", "Completed Projects", "Avg Initial Units of Projects Completed", 
                                "Units Added", "Units Removed", "Permitted Projects", 
                                "Avg Initial Units of Projects Permitted", "Permitted Unit Addition", 
                                "Permitted Unit Removal"]]
        census_db.to_csv("Building_Blocks/DOB_" + timeframe[0] + "-" + timeframe[4] + ".csv", index=False)
                

    print("Done!!")


