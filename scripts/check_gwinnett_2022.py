import json

with open(r'c:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data\results_by_year_grouped.final.json') as f:
    data = json.load(f)

print('=== Checking Gwinnett County in 2022 ===\n')

year_2022 = data['results_by_year'].get('2022', {})

# Check all 2022 contests for Gwinnett
for contest_name in year_2022.keys():
    results = year_2022[contest_name].get('results', {})
    
    # Try different capitalizations
    gwinnett_found = None
    for county_name in results.keys():
        if 'gwinnett' in county_name.lower():
            gwinnett_found = county_name
            break
    
    if gwinnett_found:
        print(f'✅ {contest_name}: Found as "{gwinnett_found}"')
        gwin = results[gwinnett_found]
        print(f'   {gwin["dem_candidate"]} ({gwin["dem_votes"]:,}) vs {gwin["rep_candidate"]} ({gwin["rep_votes"]:,})')
        print(f'   Winner: {gwin["winner_name"]} ({gwin["margin_pct"]})')
    else:
        print(f'❌ {contest_name}: Gwinnett NOT FOUND')
        print(f'   Total counties in this contest: {len(results)}')
        # Show similar names
        similar = [c for c in results.keys() if c.startswith('G')]
        if similar:
            print(f'   Counties starting with G: {", ".join(sorted(similar)[:5])}')

# List all counties to see exact names
print('\n=== All County Names in 2022 Governor ===\n')
gov_counties = sorted(year_2022['governor_2022']['results'].keys())
print(f'Total: {len(gov_counties)} counties\n')

# Show counties around "G"
g_counties = [c for c in gov_counties if c.startswith('G')]
print(f'Counties starting with G ({len(g_counties)}):')
for c in g_counties:
    print(f'  - {c}')
