import json

with open(r'c:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data\results_by_year_grouped.final.json') as f:
    data = json.load(f)

print('=== Checking 2000 Data for Rating Issues ===\n')

def get_expected_category(margin_pct):
    """Calculate what category should be based on margin"""
    margin = abs(margin_pct)
    
    if margin >= 40:
        return "Annihilation"
    elif margin >= 30:
        return "Dominant"
    elif margin >= 20:
        return "Stronghold"
    elif margin >= 10:
        return "Safe"
    elif margin >= 5.5:
        return "Likely"
    elif margin >= 1:
        return "Lean"
    elif margin >= 0.5:
        return "Tilt"
    else:
        return "Tossup"

year_2000 = data['results_by_year'].get('2000', {})
contests = list(year_2000.keys())

print(f'2000 Contests: {contests}\n')

# Check each contest
for contest_name in contests:
    results = year_2000[contest_name].get('results', {})
    print(f'\n=== {contest_name} ({len(results)} counties) ===\n')
    
    # Show sample of different ratings
    by_category = {}
    for county_name, county_data in results.items():
        cat = county_data.get('competitiveness', {}).get('category', 'Unknown')
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append((county_name, county_data))
    
    print('Counties by Category:')
    for cat in ['Annihilation', 'Dominant', 'Stronghold', 'Safe', 'Likely', 'Lean', 'Tilt', 'Tossup']:
        if cat in by_category:
            print(f'\n  {cat}: {len(by_category[cat])} counties')
            # Show first 3 examples
            for i, (county, cdata) in enumerate(by_category[cat][:3]):
                margin = cdata.get('margin_pct', '')
                winner = cdata.get('winner_name', '')
                party = cdata.get('competitiveness', {}).get('party', '')
                code = cdata.get('competitiveness', {}).get('code', '')
                print(f'    - {county}: {winner} ({margin}) → {code}')
    
    # Check for any mismatches
    errors = []
    for county_name, county_data in results.items():
        margin_pct_str = county_data.get('margin_pct', '')
        if not margin_pct_str:
            continue
        
        try:
            margin_value = float(margin_pct_str.replace('R+', '').replace('D+', '').replace('%', ''))
        except:
            continue
        
        expected_cat = get_expected_category(margin_value)
        actual_cat = county_data.get('competitiveness', {}).get('category', 'Unknown')
        
        if expected_cat != actual_cat:
            errors.append({
                'county': county_name,
                'margin': margin_pct_str,
                'margin_value': margin_value,
                'expected': expected_cat,
                'actual': actual_cat
            })
    
    if errors:
        print(f'\n  ❌ Found {len(errors)} errors:')
        for err in errors[:5]:
            print(f'    - {err["county"]}: {err["margin"]} → Expected {err["expected"]}, got {err["actual"]}')
    else:
        print(f'\n  ✅ All ratings correct')

# Also show counties at boundaries
print('\n\n=== Boundary Cases (around thresholds) ===\n')

pres_2000 = year_2000.get('president_2000', {}).get('results', {})
boundary_cases = []

for county_name, county_data in pres_2000.items():
    margin_pct_str = county_data.get('margin_pct', '')
    if not margin_pct_str:
        continue
    
    try:
        margin_value = float(margin_pct_str.replace('R+', '').replace('D+', '').replace('%', ''))
    except:
        continue
    
    # Check if near boundaries (±1% of threshold)
    thresholds = [0.5, 1, 5.5, 10, 20, 30, 40]
    for threshold in thresholds:
        if abs(margin_value - threshold) < 1:
            boundary_cases.append({
                'county': county_name,
                'margin': margin_pct_str,
                'margin_value': margin_value,
                'category': county_data.get('competitiveness', {}).get('category'),
                'threshold': threshold
            })
            break

print('Counties near category boundaries:')
for case in sorted(boundary_cases, key=lambda x: x['margin_value'])[:10]:
    print(f'  {case["county"]:15} {case["margin"]:10} → {case["category"]:15} (near {case["threshold"]}% threshold)')
