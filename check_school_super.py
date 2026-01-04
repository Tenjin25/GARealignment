#!/usr/bin/env python3
"""
Check all school superintendent contests
"""
import json

with open('data/results_by_year_grouped.final.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("School Superintendent Contests by Year:")
print("=" * 50)

for year in sorted(data['results_by_year'].keys()):
    year_data = data['results_by_year'][year]
    
    for contest_key in year_data.keys():
        if 'school' in contest_key.lower() or 'superintendent' in contest_key.lower():
            county_count = len(year_data[contest_key].get('results', {}))
            print(f"{year}: {contest_key} ({county_count} counties)")
