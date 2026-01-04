import json

with open(r'c:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data\results_by_year_grouped.final.json') as f:
    data = json.load(f)

print('=== Comparing 2022 vs Other Years ===\n')

# Get all unique categories across all years
all_years_categories = {}

for year, year_data in data['results_by_year'].items():
    categories = set()
    for contest_name, contest_data in year_data.items():
        for county_data in contest_data.get('results', {}).values():
            comp = county_data.get('competitiveness', {})
            cat_code = comp.get('code', 'UNKNOWN')
            categories.add(cat_code)
    all_years_categories[year] = categories

# Check if 2022 uses same categories as other years
all_possible_categories = set()
for cats in all_years_categories.values():
    all_possible_categories.update(cats)

print(f'All unique category codes across all years: {len(all_possible_categories)}')
print(f'Expected: 15\n')

print('2022 Categories Used:')
year_2022_cats = sorted(all_years_categories['2022'])
for cat in year_2022_cats:
    print(f'  {cat}')

print(f'\nTotal 2022 categories: {len(year_2022_cats)}')

# Verify the exact categories match the 15-tier system
expected_categories = [
    'REPUBLICAN_ANNIHILATION', 'REPUBLICAN_DOMINANT', 'REPUBLICAN_STRONGHOLD',
    'REPUBLICAN_SAFE', 'REPUBLICAN_LIKELY', 'REPUBLICAN_LEAN', 'REPUBLICAN_TILT',
    'TOSSUP',
    'DEMOCRAT_TILT', 'DEMOCRAT_LEAN', 'DEMOCRAT_LIKELY', 'DEMOCRAT_SAFE',
    'DEMOCRAT_STRONGHOLD', 'DEMOCRAT_DOMINANT', 'DEMOCRAT_ANNIHILATION'
]

missing = set(expected_categories) - all_years_categories['2022']
extra = all_years_categories['2022'] - set(expected_categories)

if missing:
    print(f'\n⚠️ Missing from 2022: {missing}')
else:
    print('\n✅ All expected categories present in 2022')

if extra:
    print(f'⚠️ Extra in 2022: {extra}')

# Compare specific examples
print('\n=== Sample 2022 Counties ===\n')

gov_2022 = data['results_by_year']['2022']['governor_2022']['results']

samples = [
    ('Gwinnett', 'Should be Safe Democrat'),
    ('Fulton', 'Should be strong Democrat'),
    ('Forsyth', 'Should be strong Republican'),
    ('Chattooga', 'Should be strong Republican'),
]

for county, description in samples:
    if county in gov_2022:
        c = gov_2022[county]
        print(f'{county} ({description}):')
        print(f'  Winner: {c["winner_name"]} ({c["margin_pct"]})')
        print(f'  Category: {c["competitiveness"]["category"]} - {c["competitiveness"]["party"]}')
        print(f'  Code: {c["competitiveness"]["code"]}')
        print(f'  Color: {c["competitiveness"]["color"]}\n')
