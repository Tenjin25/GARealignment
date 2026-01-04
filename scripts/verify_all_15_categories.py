import json

with open(r'c:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data\results_by_year_grouped.corrected.json') as f:
    data = json.load(f)

print('=== All 15 Competitiveness Categories ===\n')

# Collect all unique category + party combinations across all years
all_categories = set()
category_counts = {}

for year, year_data in data['results_by_year'].items():
    for contest_name, contest_data in year_data.items():
        for county_data in contest_data.get('results', {}).values():
            comp = county_data.get('competitiveness', {})
            category = comp.get('category', 'Unknown')
            party = comp.get('party', 'NONE')
            code = comp.get('code', 'UNKNOWN')
            color = comp.get('color', '#000000')
            
            key = (category, party, code, color)
            all_categories.add(key)
            category_counts[key] = category_counts.get(key, 0) + 1

# Sort and display
print('REPUBLICAN Categories:')
for cat, party, code, color in sorted(all_categories):
    if party == 'REPUBLICAN':
        count = category_counts[(cat, party, code, color)]
        print(f'  {cat:15} - {code:30} - {color} ({count:,} counties)')

print('\nTOSSUP Category:')
for cat, party, code, color in sorted(all_categories):
    if cat == 'Tossup':
        count = category_counts[(cat, party, code, color)]
        print(f'  {cat:15} - {code:30} - {color} ({count:,} counties)')

print('\nDEMOCRAT Categories:')
for cat, party, code, color in sorted(all_categories):
    if party == 'DEMOCRAT':
        count = category_counts[(cat, party, code, color)]
        print(f'  {cat:15} - {code:30} - {color} ({count:,} counties)')

print(f'\n=== Summary ===')
print(f'Total unique categories found: {len(all_categories)}')
print(f'Expected: 15 (7 Republican + 1 Tossup + 7 Democrat)')

# Find examples of each category
print('\n=== Example Counties by Category ===\n')
examples = {}
for year, year_data in data['results_by_year'].items():
    for contest_name, contest_data in year_data.items():
        for county_name, county_data in contest_data.get('results', {}).items():
            comp = county_data.get('competitiveness', {})
            code = comp.get('code', 'UNKNOWN')
            if code not in examples:
                examples[code] = {
                    'county': county_name,
                    'year': year,
                    'contest': contest_name,
                    'margin': county_data.get('margin_pct', ''),
                    'winner': county_data.get('winner_name', '')
                }

for code in ['REPUBLICAN_ANNIHILATION', 'REPUBLICAN_DOMINANT', 'REPUBLICAN_STRONGHOLD', 
             'REPUBLICAN_SAFE', 'REPUBLICAN_LIKELY', 'REPUBLICAN_LEAN', 'REPUBLICAN_TILT',
             'TOSSUP',
             'DEMOCRAT_TILT', 'DEMOCRAT_LEAN', 'DEMOCRAT_LIKELY', 'DEMOCRAT_SAFE',
             'DEMOCRAT_STRONGHOLD', 'DEMOCRAT_DOMINANT', 'DEMOCRAT_ANNIHILATION']:
    if code in examples:
        ex = examples[code]
        print(f'{code:30} - {ex["county"]}, {ex["year"]} ({ex["margin"]})')
