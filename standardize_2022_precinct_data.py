"""
Standardize 2022 GA precinct data to match the 2024 format.

Input: ga22_cleaned.csv (2022 precinct data)
Output: 2022_ga_general_precinct-level.csv (standardized format)
"""

import pandas as pd
import os

# Define file paths
input_file = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data\2022-ga-local-precinct-general\ga22_cleaned.csv"
output_file = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data\2022_ga_general_precinct-level.csv"

print("Loading 2022 data...")
# Read the 2022 data in chunks to handle large file
chunk_size = 100000
chunks = []
for i, chunk in enumerate(pd.read_csv(input_file, chunksize=chunk_size, low_memory=False)):
    print(f"  Reading chunk {i+1}... ({len(chunk)} rows)")
    chunks.append(chunk)

df = pd.concat(chunks, ignore_index=True)
print(f"\nOriginal shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

# Filter to only TOTAL mode (remove early voting, absentee, etc. subcategories)
df_total = df[df['mode'] == 'TOTAL'].copy()

print(f"After filtering to TOTAL mode: {df_total.shape}")

# Create the standardized format
# Target columns: county, precinct, office, district, party, candidate, total_votes
standardized = pd.DataFrame({
    'county': df_total['county_name'],
    'precinct': df_total['precinct'],
    'office': df_total['office'],
    'district': df_total['district'].fillna(''),  # Fill NaN with empty string
    'party': df_total['party_simplified'],
    'candidate': df_total['candidate'],
    'total_votes': df_total['votes']
})

# Clean up the data
# Convert county names to title case to match 2024 format
standardized['county'] = standardized['county'].str.title()

# Standardize office names to match 2024 format
office_mapping = {
    'US SENATE': 'U.S. Senate',
    'GOVERNOR': 'Governor',
    'LIEUTENANT GOVERNOR': 'Lieutenant Governor',
    'SECRETARY OF STATE': 'Secretary of State',
    'ATTORNEY GENERAL': 'Attorney General',
    'COMMISSIONER OF AGRICULTURE': 'Commissioner of Agriculture',
    'COMMISSIONER OF INSURANCE': 'Commissioner of Insurance',
    'COMMISSIONER OF LABOR': 'Commissioner of Labor',
    'STATE SENATE': 'State Senate',
    'STATE HOUSE': 'State House',
    'US HOUSE': 'U.S. House'
}

standardized['office'] = standardized['office'].replace(office_mapping)

# Standardize party names to match 2024 format
party_mapping = {
    'DEMOCRAT': 'Democrat',
    'REPUBLICAN': 'Republican',
    'LIBERTARIAN': 'Libertarian',
    'GREEN': 'Green'
}

standardized['party'] = standardized['party'].replace(party_mapping)

# Sort by county, precinct, office, party, candidate
standardized = standardized.sort_values(['county', 'precinct', 'office', 'party', 'candidate'])

# Reset index
standardized = standardized.reset_index(drop=True)

print(f"\nStandardized shape: {standardized.shape}")
print(f"\nFirst few rows:")
print(standardized.head(20))

print(f"\nUnique offices:")
print(standardized['office'].unique())

print(f"\nUnique parties:")
print(standardized['party'].unique())

print(f"\nSample counties:")
print(standardized['county'].unique()[:10])

# Save to CSV
print(f"\nSaving to {output_file}...")
standardized.to_csv(output_file, index=False)

print("Done! Standardized 2022 data saved.")

# Print some statistics
print(f"\nStatistics:")
print(f"Total rows: {len(standardized)}")
print(f"Unique counties: {standardized['county'].nunique()}")
print(f"Unique precincts: {standardized['precinct'].nunique()}")
print(f"Unique offices: {standardized['office'].nunique()}")
print(f"Total votes: {standardized['total_votes'].sum():,.0f}")
