#!/usr/bin/env python3
"""
Aggregate standardized precinct-level CSV data to county level for all elections.
Works with the new format: county, precinct, office, district, party, candidate, total_votes
"""
import pandas as pd
import json
import os
from collections import defaultdict

ROOT = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT, 'data')
OUTPUT_PATH = os.path.join(ROOT, 'data_files', 'Election_Data_GA.v04', 'aggregated_by_county.json')

# Files to process
CSV_FILES = {
    '2022_general': os.path.join(DATA_DIR, '20221108__ga__general__precinct-total.csv'),
    '2022_runoff': os.path.join(DATA_DIR, '20221206__ga__general_runoff__precinct.csv'),
    '2021_runoff': os.path.join(DATA_DIR, '20210105__ga__runoff.csv'),
    '2024_general': os.path.join(DATA_DIR, '20241105__ga__general__precinct-level.csv'),
}

print("Aggregating precinct data to county level...")

results = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int))))

def fix_county_name(name):
    """Standardize county names for consistency"""
    name = name.strip().title()
    # Special cases for Mc/Mac counties
    if name.lower() == 'mcduffie':
        return 'McDuffie'
    elif name.lower() == 'mcintosh':
        return 'McIntosh'
    elif name.lower() == 'dekalb':
        return 'DeKalb'
    else:
        return name

for election_name, csv_path in CSV_FILES.items():
    if not os.path.exists(csv_path):
        print(f"  Skipping {election_name} - file not found: {csv_path}")
        continue
    
    print(f"\nProcessing {election_name}...")
    try:
        df = pd.read_csv(csv_path, on_bad_lines='skip')
    except Exception as e:
        print(f"  Error reading file: {e}")
        continue
    
    # Standardize column names FIRST
    df.columns = df.columns.str.strip()
    
    # Check if we need to calculate total_votes from component columns
    if 'total_votes' not in df.columns:
        vote_cols = ['election_day_votes', 'advanced_votes', 'absentee_by_mail_votes', 'provisional_votes']
        available_cols = [col for col in vote_cols if col in df.columns]
        if available_cols:
            df['total_votes'] = df[available_cols].fillna(0).sum(axis=1)
            print(f"  Calculated total_votes from {len(available_cols)} component columns")
        else:
            print(f"  ERROR: No total_votes or component vote columns found")
            print(f"  Available columns: {list(df.columns)}")
            continue
    
    # Check for required columns
    required_cols = ['county', 'office', 'party', 'candidate', 'total_votes']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"  ERROR: Missing required columns: {missing_cols}")
        print(f"  Available columns: {list(df.columns)}")
        continue
    
    df['county'] = df['county'].str.strip().str.title()
    df['county'] = df['county'].apply(fix_county_name)
    df['office'] = df['office'].str.strip()
    df['party'] = df['party'].str.strip()
    df['candidate'] = df['candidate'].str.strip()
    
    # Aggregate by county, office, party, candidate
    grouped = df.groupby(['county', 'office', 'party', 'candidate'])['total_votes'].sum().reset_index()
    
    for _, row in grouped.iterrows():
        county = row['county']
        office = row['office']
        party = row['party']
        candidate = row['candidate']
        votes = int(row['total_votes'])
        
        # Store in results structure
        results[election_name][county][office][f"{party}_{candidate}"] = votes
    
    print(f"  Aggregated {len(grouped)} county-office-candidate combinations")
    print(f"  Counties: {df['county'].nunique()}")

# Convert to final JSON structure
output = {
    'metadata': {
        'description': 'County-level aggregated election results for Georgia',
        'elections': list(CSV_FILES.keys()),
        'generated': 'auto'
    },
    'results': dict(results)
}

# Write output
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2)

print(f"\n✓ Wrote aggregated data to {OUTPUT_PATH}")
print(f"  Total elections: {len(results)}")
print(f"  Sample structure:")
for election in list(results.keys())[:2]:
    counties = list(results[election].keys())[:3]
    print(f"    {election}: {len(results[election])} counties (e.g., {', '.join(counties)})")
