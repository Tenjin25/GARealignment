import json

with open(r'c:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data\results_by_year_grouped.final.json') as f:
    data = json.load(f)

print('=== Comparing 2022 Structure vs Other Years ===\n')

# Check structure of 2020 (working year) vs 2022
print('2020 President Structure:')
pres_2020 = data['results_by_year']['2020']['president_2020']
print(f'Keys: {list(pres_2020.keys())}')
if 'results' in pres_2020:
    sample_county = list(pres_2020['results'].values())[0]
    print(f'Sample county keys: {list(sample_county.keys())[:10]}...')

print('\n2022 Governor Structure:')
gov_2022 = data['results_by_year']['2022']['governor_2022']
print(f'Keys: {list(gov_2022.keys())}')
if 'results' in gov_2022:
    sample_county = list(gov_2022['results'].values())[0]
    print(f'Sample county keys: {list(sample_county.keys())[:10]}...')

# Check Gwinnett specifically
print('\n=== Gwinnett County Full Structure ===\n')

print('2020 President - Gwinnett:')
gwin_2020 = data['results_by_year']['2020']['president_2020']['results'].get('Gwinnett')
if gwin_2020:
    for key, value in list(gwin_2020.items())[:15]:
        print(f'  {key}: {value}')
else:
    print('  NOT FOUND')

print('\n2022 Governor - Gwinnett:')
gwin_2022 = data['results_by_year']['2022']['governor_2022']['results'].get('Gwinnett')
if gwin_2022:
    for key, value in list(gwin_2022.items())[:15]:
        print(f'  {key}: {value}')
else:
    print('  NOT FOUND')

# Check if there's a missing field
print('\n=== Missing Fields Check ===\n')

if gwin_2020 and gwin_2022:
    keys_2020 = set(gwin_2020.keys())
    keys_2022 = set(gwin_2022.keys())
    
    missing_in_2022 = keys_2020 - keys_2022
    extra_in_2022 = keys_2022 - keys_2020
    
    if missing_in_2022:
        print(f'❌ Fields in 2020 but missing in 2022: {missing_in_2022}')
    if extra_in_2022:
        print(f'ℹ️  Extra fields in 2022 not in 2020: {extra_in_2022}')
    if not missing_in_2022 and not extra_in_2022:
        print('✅ All fields match!')

# Check all required fields
required_fields = ['dem_candidate', 'rep_candidate', 'dem_votes', 'rep_votes', 
                   'total_votes', 'winner', 'winner_name', 'margin_pct', 
                   'competitiveness', 'county', 'year', 'contest']

print('\n=== Required Fields Check ===\n')
print('2022 Governor - Gwinnett:')
for field in required_fields:
    value = gwin_2022.get(field) if gwin_2022 else None
    status = '✅' if value is not None else '❌'
    print(f'  {status} {field}: {value}')
