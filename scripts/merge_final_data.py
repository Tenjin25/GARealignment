#!/usr/bin/env python3
"""
Merge corrected competitiveness ratings with new 2022 aggregated data.
Creates a final complete file while keeping originals as backup.
"""
import json
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CORRECTED_PATH = os.path.join(ROOT, 'data', 'results_by_year_grouped.corrected.json')
UPDATED_2022_PATH = os.path.join(ROOT, 'data', 'results_by_year_grouped.updated2022.json')
FINAL_PATH = os.path.join(ROOT, 'data', 'results_by_year_grouped.final.json')

print('Loading corrected competitiveness ratings...')
with open(CORRECTED_PATH, 'r', encoding='utf-8') as f:
    corrected_data = json.load(f)

print('Loading updated 2022 data with CSV aggregation...')
with open(UPDATED_2022_PATH, 'r', encoding='utf-8') as f:
    updated_2022_data = json.load(f)

print('Merging data...')

# Start with the corrected data (has all years with fixed competitiveness)
final_data = corrected_data

# Replace the entire 2022 section with the newly aggregated data
final_data['results_by_year']['2022'] = updated_2022_data['results_by_year']['2022']

# Verify the merge
years = sorted(final_data['results_by_year'].keys())
print(f'\n=== Final Data Summary ===')
print(f'Total years: {len(years)}')
print(f'Years: {", ".join(years)}')

# Check 2022 contests
contests_2022 = list(final_data['results_by_year']['2022'].keys())
print(f'\n2022 Contests ({len(contests_2022)}):')
for contest in contests_2022:
    county_count = len(final_data['results_by_year']['2022'][contest]['results'])
    print(f'  {contest}: {county_count} counties')

# Verify a sample county
gwinnett_gov = final_data['results_by_year']['2022']['governor_2022']['results'].get('Gwinnett')
if gwinnett_gov:
    print(f'\nSample - Gwinnett 2022 Governor:')
    print(f'  {gwinnett_gov["dem_candidate"]} vs {gwinnett_gov["rep_candidate"]}')
    print(f'  Winner: {gwinnett_gov["winner_name"]} ({gwinnett_gov["margin_pct"]})')
    print(f'  Competitiveness: {gwinnett_gov["competitiveness"]["category"]} - {gwinnett_gov["competitiveness"]["party"]}')

# Write final merged file
print(f'\nWriting final merged data to {FINAL_PATH}...')
with open(FINAL_PATH, 'w', encoding='utf-8') as f:
    json.dump(final_data, f, indent=2)

print('\n✅ Done!')
print(f'Final file created: {FINAL_PATH}')
print(f'Original file preserved: data/results_by_year_grouped.json')
print(f'Backup files available: results_by_year_grouped.corrected.json, results_by_year_grouped.updated2022.json')
