import json

with open(r'c:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data\results_by_year_grouped.corrected.json') as f:
    data = json.load(f)

print('=== Sample Verification ===\n')

# Check 2020 Presidential
pres_2020 = data['results_by_year']['2020']['president_2020']['results']['Gwinnett']
print('2020 President - Gwinnett:')
print(f'  Winner: {pres_2020["winner_name"]} ({pres_2020["margin_pct"]})')
print(f'  Competitiveness: {pres_2020["competitiveness"]["category"]} - {pres_2020["competitiveness"]["party"]}')
print(f'  Color: {pres_2020["competitiveness"]["color"]}\n')

# Check different categories across years
print('=== Category Distribution by Year ===\n')

for year in ['2016', '2018', '2020', '2022']:
    if year not in data['results_by_year']:
        continue
    
    categories = {}
    for contest_name, contest_data in data['results_by_year'][year].items():
        for county_data in contest_data.get('results', {}).values():
            cat = county_data.get('competitiveness', {}).get('category', 'Unknown')
            categories[cat] = categories.get(cat, 0) + 1
    
    print(f'{year}:')
    total = sum(categories.values())
    for cat in ['Annihilation', 'Dominant', 'Stronghold', 'Safe', 'Likely', 'Lean', 'Tilt', 'Tossup']:
        if cat in categories:
            pct = (categories[cat] / total * 100) if total > 0 else 0
            print(f'  {cat}: {categories[cat]} ({pct:.1f}%)')
    print()
