#!/usr/bin/env python3
"""
Check what data is missing in 2014 elections and identify which counties need data.
"""
import json

with open('data/results_by_year_grouped.final.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

year_2014 = data.get('results_by_year', {}).get('2014', {})

if not year_2014:
    print("No 2014 data found!")
    exit(1)

print("=" * 80)
print("2014 CONTESTS AVAILABLE:")
print("=" * 80)
for contest_key in sorted(year_2014.keys()):
    contest_data = year_2014[contest_key]
    results = contest_data.get('results', {})
    county_count = len(results)
    print(f"\n{contest_key}:")
    print(f"  - Counties with data: {county_count}/159")
    
    if county_count < 159:
        print(f"  - Missing {159 - county_count} counties")
        # Show a sample of counties that DO have data
        sample_counties = list(results.keys())[:5]
        print(f"  - Sample counties with data: {', '.join(sample_counties)}")
        
        # Check if any counties have missing or zero vote totals
        incomplete = []
        for county, county_data in results.items():
            total = county_data.get('total_votes', 0)
            if total == 0:
                incomplete.append(county)
        
        if incomplete:
            print(f"  - Counties with zero votes: {len(incomplete)}")
            print(f"    Examples: {', '.join(incomplete[:10])}")

print("\n" + "=" * 80)
print("SUMMARY:")
print("=" * 80)
print(f"Total contests in 2014: {len(year_2014)}")
print("\nContest completeness:")
for contest_key in sorted(year_2014.keys()):
    results = year_2014[contest_key].get('results', {})
    pct = (len(results) / 159) * 100
    print(f"  {contest_key}: {len(results)}/159 ({pct:.1f}%)")
