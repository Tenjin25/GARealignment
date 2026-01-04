#!/usr/bin/env python3
"""List all unique contest types across all years in the data."""
import json

with open('data/results_by_year_grouped.final.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

all_contests = set()
by_year = {}

for year, contests in data['results_by_year'].items():
    contest_keys = list(contests.keys())
    by_year[year] = contest_keys
    all_contests.update(contest_keys)

print("Contests by year:")
for year in sorted(by_year.keys()):
    print(f"\n{year}:")
    for contest in sorted(by_year[year]):
        print(f"  - {contest}")

print("\n\nAll unique contest types:")
for contest in sorted(all_contests):
    print(f"  {contest}")
