import json

with open(r'c:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data\results_by_year_grouped.final.json') as f:
    data = json.load(f)

print('=== Checking ALL Counties for Rating Errors ===\n')

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

errors = []
total_checked = 0

for year, year_data in data['results_by_year'].items():
    for contest_name, contest_data in year_data.items():
        for county_name, county_data in contest_data.get('results', {}).items():
            total_checked += 1
            
            # Get margin info
            margin_pct_str = county_data.get('margin_pct', '')
            if not margin_pct_str:
                continue
            
            # Parse margin
            try:
                margin_value = float(margin_pct_str.replace('R+', '').replace('D+', '').replace('%', ''))
                winner_party = 'REPUBLICAN' if margin_pct_str.startswith('R') else 'DEMOCRAT'
            except:
                continue
            
            # Get expected vs actual
            expected_cat = get_expected_category(margin_value)
            actual_cat = county_data.get('competitiveness', {}).get('category', 'Unknown')
            
            if expected_cat != actual_cat:
                errors.append({
                    'year': year,
                    'contest': contest_name,
                    'county': county_name,
                    'margin': margin_pct_str,
                    'margin_value': margin_value,
                    'expected': expected_cat,
                    'actual': actual_cat,
                    'code': county_data.get('competitiveness', {}).get('code', '')
                })

print(f'Total counties checked: {total_checked:,}')
print(f'Errors found: {len(errors)}')

if errors:
    print('\n❌ FOUND RATING ERRORS:\n')
    for i, error in enumerate(errors[:20], 1):  # Show first 20
        print(f'{i}. {error["year"]} - {error["contest"]} - {error["county"]}')
        print(f'   Margin: {error["margin"]} ({error["margin_value"]:.2f}%)')
        print(f'   Expected: {error["expected"]}')
        print(f'   Actual: {error["actual"]} ({error["code"]})')
        print()
    
    if len(errors) > 20:
        print(f'... and {len(errors) - 20} more errors')
    
    # Group errors by type
    print('\n=== Error Summary by Type ===')
    error_types = {}
    for error in errors:
        key = f'{error["expected"]} → {error["actual"]}'
        error_types[key] = error_types.get(key, 0) + 1
    
    for error_type, count in sorted(error_types.items(), key=lambda x: -x[1]):
        print(f'{error_type}: {count} errors')
else:
    print('\n✅ NO ERRORS FOUND! All ratings are correct.')
