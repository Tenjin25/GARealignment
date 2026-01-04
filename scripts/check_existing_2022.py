import json

with open(r'c:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data\results_by_year_grouped.json') as f:
    d = json.load(f)

print('Has 2022:', '2022' in d['results_by_year'])

if '2022' in d['results_by_year']:
    print('2022 contests:', list(d['results_by_year']['2022'].keys()))
    
    gov = d['results_by_year']['2022'].get('governor_2022', {}).get('results', {})
    print(f'\nExisting governor_2022 counties: {len(gov)}')
    
    counties = sorted(gov.keys())
    print('Sample county names:')
    for c in counties[:10]:
        print(f'  - {c}')
    
    # Check for duplicates (different capitalization)
    lower_counties = {}
    for c in counties:
        lower = c.lower()
        if lower in lower_counties:
            print(f'\nDuplicate found: "{lower_counties[lower]}" and "{c}"')
        lower_counties[lower] = c
