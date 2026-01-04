#!/usr/bin/env python3
"""Check 2014 data for independent (I) party designations."""
import json

with open('data/results_by_year_grouped.final.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

results_2014 = data.get('results_by_year', {}).get('2014', {})

if not results_2014:
    print('No 2014 data found.')
    exit()

print('Checking 2014 contests for independent/unusual party designations...\n')

for contest_key, contest_obj in results_2014.items():
    print(f'\n=== {contest_key} ===')
    results = contest_obj.get('results', {})
    
    if not isinstance(results, dict):
        print('  Results not in expected format')
        continue
    
    independent_counties = []
    
    for county, county_data in results.items():
        winner_party = county_data.get('winner_party', '')
        winner = county_data.get('winner', '')
        winner_name = county_data.get('winner_name', '')
        
        # Check for Independent or unusual party designations
        if 'I' in str(winner_party).upper() and 'REPUBLICAN' not in str(winner_party).upper() and 'DEMOCRAT' not in str(winner_party).upper():
            independent_counties.append({
                'county': county,
                'winner_party': winner_party,
                'winner': winner,
                'winner_name': winner_name,
                'dem_votes': county_data.get('dem_votes', 0),
                'rep_votes': county_data.get('rep_votes', 0),
                'margin_pct': county_data.get('margin_pct', ''),
            })
    
    if independent_counties:
        print(f'  Found {len(independent_counties)} counties with independent/unusual party:')
        for item in independent_counties[:10]:  # Show first 10
            print(f'    {item["county"]}: party="{item["winner_party"]}", winner="{item["winner"]}", name="{item["winner_name"]}"')
            print(f'      Dem votes: {item["dem_votes"]}, Rep votes: {item["rep_votes"]}, Margin: {item["margin_pct"]}')
    else:
        print('  No independent/unusual party designations found')

print('\n\nChecking for specific party values across all 2014 contests...')
all_parties = set()
for contest_key, contest_obj in results_2014.items():
    results = contest_obj.get('results', {})
    if isinstance(results, dict):
        for county_data in results.values():
            party = county_data.get('winner_party', '')
            if party:
                all_parties.add(str(party))

print('Unique winner_party values in 2014:')
for party in sorted(all_parties):
    print(f'  - {party}')
