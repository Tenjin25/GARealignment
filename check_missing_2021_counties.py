"""
Check which counties are missing from the 2021 runoff data.
"""
import pandas as pd

# Load the files
runoff_2021 = pd.read_csv('data/20210105__ga__runoff.csv')
general_2022 = pd.read_csv('data/20221108__ga__general__precinct-total.csv')

# Strip column names
runoff_2021.columns = runoff_2021.columns.str.strip()
general_2022.columns = general_2022.columns.str.strip()

# Get unique counties
runoff_2021['county'] = runoff_2021['county'].str.strip().str.title()
general_2022['county'] = general_2022['county'].str.strip().str.title()

counties_2021 = set(runoff_2021['county'].unique())
counties_2022 = set(general_2022['county'].unique())

missing_from_2021 = counties_2022 - counties_2021

print(f"2021 Runoff has {len(counties_2021)} counties")
print(f"2022 General has {len(counties_2022)} counties")
print(f"\nMissing from 2021 runoff ({len(missing_from_2021)} counties):")
for county in sorted(missing_from_2021):
    print(f"  - {county}")
