#!/usr/bin/env python3
"""
Aggregate precinct-level CSV data to county level for 2022 elections.
Extracts first 5 digits of GEOID20 as county code, sums all numeric fields by county.
"""
import csv
import json
import os
from collections import defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CSV_PATH = os.path.join(ROOT, 'data_files', 'Election_Data_GA.v04', 'election_data_GA.v04-aligned.csv')
GEOJSON_PATH = os.path.join(ROOT, 'tl_2020_13_county20.geojson')
OUT_PATH = os.path.join(ROOT, 'data_files', 'Election_Data_GA.v04', 'aggregated_2022_by_county.json')

# Read GeoJSON to get county names
print('Loading county GeoJSON...')
with open(GEOJSON_PATH, 'r', encoding='utf-8') as f:
    geojson = json.load(f)

county_names = {}
for feature in geojson['features']:
    props = feature['properties']
    geoid = props.get('GEOID20')
    name = props.get('NAME20')
    if geoid and name:
        county_names[geoid] = name.lower()

print(f'Loaded {len(county_names)} counties from GeoJSON')

# Read CSV and aggregate by county
print('Reading and aggregating CSV data...')
with open(CSV_PATH, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = [{k.strip(): v for k, v in r.items() if k} for r in reader]

# Columns to aggregate (all 2022 election columns)
columns_22 = [h for h in rows[0].keys() if '22' in h or '16-22' in h]
print(f'Found {len(columns_22)} columns to aggregate for 2022')

# Aggregate by county GEOID (first 5 digits)
county_data = defaultdict(lambda: defaultdict(int))

for row in rows:
    geoid = row.get('GEOID20', '')
    if len(geoid) < 5:
        continue
    
    county_geoid = geoid[:5]
    
    # Sum all numeric columns
    for col in columns_22:
        value = row.get(col, '0')
        try:
            county_data[county_geoid][col] += int(value)
        except (ValueError, TypeError):
            # Skip non-numeric values
            pass

# Build output structure matching the county GeoJSON
output = {}
for county_geoid, data in county_data.items():
    county_name = county_names.get(county_geoid, 'unknown').title()
    
    output[county_name.lower()] = {
        'GEOID20': county_geoid,
        'Name': county_name,
        'data': {k: str(v) for k, v in data.items()}
    }

# Write output
with open(OUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2)

print(f'\nWrote aggregated data to {OUT_PATH}')
print(f'Counties processed: {len(output)}')
print(f'\nSample (first county):')
first_county = list(output.keys())[0]
print(f'{first_county}: GEOID={output[first_county]["GEOID20"]}, Data keys={len(output[first_county]["data"])}')
