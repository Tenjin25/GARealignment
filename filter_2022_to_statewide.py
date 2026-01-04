"""
Filter the standardized 2022 data to include only statewide offices
that match the 2024 format.
"""

import pandas as pd

# Read the standardized 2022 data
input_file = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data\2022_ga_general_precinct-level.csv"
output_file = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data\2022_ga_general_precinct-level_statewide.csv"

print("Loading standardized 2022 data...")
df = pd.read_csv(input_file)

print(f"Original shape: {df.shape}")
print(f"Unique offices: {df['office'].nunique()}")

# Define statewide offices to keep (matching 2024 format)
statewide_offices = [
    'U.S. Senate',
    'Governor',
    'Lieutenant Governor',
    'Secretary of State',
    'Attorney General',
    'Commissioner of Agriculture',
    'Commissioner of Insurance',
    'Commissioner of Labor',
    'U.S. House',
    'State Senate',
    'State House'
]

# Filter to only statewide offices
df_statewide = df[df['office'].isin(statewide_offices)].copy()

print(f"\nAfter filtering to statewide offices:")
print(f"Shape: {df_statewide.shape}")
print(f"Unique offices: {df_statewide['office'].nunique()}")
print(f"\nOffices included:")
for office in sorted(df_statewide['office'].unique()):
    count = len(df_statewide[df_statewide['office'] == office])
    print(f"  {office}: {count:,} rows")

print(f"\nSample data:")
print(df_statewide.head(20))

# Save filtered data
print(f"\nSaving to {output_file}...")
df_statewide.to_csv(output_file, index=False)

print("Done!")
print(f"\nFinal statistics:")
print(f"Total rows: {len(df_statewide):,}")
print(f"Total votes: {df_statewide['total_votes'].sum():,.0f}")
print(f"Unique counties: {df_statewide['county'].nunique()}")
print(f"Unique precincts: {df_statewide['precinct'].nunique()}")
