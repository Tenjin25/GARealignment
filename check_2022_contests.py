#!/usr/bin/env python3
"""
Check what contests are in 2022 data
"""
import json

with open('data/results_by_year_grouped.final.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

year_2022 = data['results_by_year'].get('2022', {})

print("2022 Contest Keys:")
print("-" * 50)
for key in sorted(year_2022.keys()):
    # Get county count
    county_count = len(year_2022[key].get('results', {}))
    print(f"{key:<40} {county_count} counties")
