import json

with open(r'c:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data\results_by_year_grouped.updated2022.json') as f:
    d = json.load(f)

gov = d['results_by_year']['2022']['governor_2022']['results']

print('=== 2022 Governor Race Verification ===\n')

# Test Gwinnett (Democratic)
gwinnett = gov['Gwinnett']
print('Gwinnett County:')
print(f'  Dem: {gwinnett["dem_candidate"]} - {gwinnett["dem_votes"]:,} votes')
print(f'  Rep: {gwinnett["rep_candidate"]} - {gwinnett["rep_votes"]:,} votes')
print(f'  Total: {gwinnett["total_votes"]:,}')
print(f'  Winner: {gwinnett["winner_name"]} ({gwinnett["margin_pct"]})')
print(f'  Competitiveness: {gwinnett["competitiveness"]["category"]} - {gwinnett["competitiveness"]["party"]}')
print(f'  Color: {gwinnett["competitiveness"]["color"]}\n')

# Test a Republican county
if 'Forsyth' in gov:
    forsyth = gov['Forsyth']
    print('Forsyth County:')
    print(f'  Winner: {forsyth["winner_name"]} ({forsyth["margin_pct"]})')
    print(f'  Competitiveness: {forsyth["competitiveness"]["category"]} - {forsyth["competitiveness"]["party"]}')
    print(f'  Color: {forsyth["competitiveness"]["color"]}\n')

# Count by competitiveness
categories = {}
for county, data in gov.items():
    cat = data['competitiveness']['category']
    categories[cat] = categories.get(cat, 0) + 1

print('Counties by Competitiveness:')
for cat in ['Annihilation', 'Dominant', 'Stronghold', 'Safe', 'Likely', 'Lean', 'Tilt', 'Tossup']:
    if cat in categories:
        print(f'  {cat}: {categories[cat]}')
