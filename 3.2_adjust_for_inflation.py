import pandas as pd

#adjusting all dollar values for inflation

inflation_multiplier = 1.08
timeframes = ["2010-2014", "2015-2019"]

for timeframe in timeframes:
    housing_data = pd.read_csv(f"Building_Blocks/Housing_on_Census_{timeframe}.csv")
    if timeframe == "2010-2014":
        housing_data["inf_med_hh_income"] = housing_data["med_hh_income"] * inflation_multiplier
        housing_data["inf_med_rent"] = housing_data["med_rent"] * inflation_multiplier
        housing_data["inf_med_home_value"] = housing_data["med_home_value"] * inflation_multiplier
    else:
        housing_data["inf_med_hh_income"] = housing_data["med_hh_income"]
        housing_data["inf_med_rent"] = housing_data["med_rent"]
        housing_data["inf_med_home_value"] = housing_data["med_home_value"]

    housing_data.to_csv(f"Building_Blocks/Housing_on_Census_{timeframe}.csv", index=False)
    print(f"Updated {timeframe} data with neighborhood labels.")
