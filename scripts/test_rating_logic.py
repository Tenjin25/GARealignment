"""
Your original categorization system from the JSON:

Republican:
  Annihilation:  R+40%+
  Dominant:      R+30-40%
  Stronghold:    R+20-30%
  Safe:          R+10-20%
  Likely:        R+5.5-10%
  Lean:          R+1-5.5%
  Tilt:          R+0.5-1%

Tossup:          ±0.5%

Democratic:
  Tilt:          D+0.5-1%
  Lean:          D+1-5.5%
  Likely:        D+5.5-10%
  Safe:          D+10-20%
  Stronghold:    D+20-30%
  Dominant:      D+30-40%
  Annihilation:  D+40%+

Current script logic:
  >= 40:    Annihilation
  >= 30:    Dominant
  >= 20:    Stronghold
  >= 10:    Safe
  >= 5.5:   Likely
  >= 1:     Lean
  >= 0.5:   Tilt
  < 0.5:    Tossup

Test cases to verify:
"""
import json

with open(r'c:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data\results_by_year_grouped.final.json') as f:
    data = json.load(f)

print('=== Testing Rating Logic ===\n')

# Test specific margin ranges
test_cases = [
    (45, 'R', 'Should be Annihilation (R+40%+)'),
    (35, 'R', 'Should be Dominant (R+30-40%)'),
    (25, 'R', 'Should be Stronghold (R+20-30%)'),
    (15, 'R', 'Should be Safe (R+10-20%)'),
    (7, 'R', 'Should be Likely (R+5.5-10%)'),
    (3, 'R', 'Should be Lean (R+1-5.5%)'),
    (0.7, 'R', 'Should be Tilt (R+0.5-1%)'),
    (0.3, 'R', 'Should be Tossup (±0.5%)'),
    (0.3, 'D', 'Should be Tossup (±0.5%)'),
    (0.7, 'D', 'Should be Tilt (D+0.5-1%)'),
    (3, 'D', 'Should be Lean (D+1-5.5%)'),
    (7, 'D', 'Should be Likely (D+5.5-10%)'),
    (15, 'D', 'Should be Safe (D+10-20%)'),
    (25, 'D', 'Should be Stronghold (D+20-30%)'),
    (35, 'D', 'Should be Dominant (D+30-40%)'),
    (45, 'D', 'Should be Annihilation (D+40%+)'),
]

# Find actual examples from 2022 data for each range
gov_2022 = data['results_by_year']['2022']['governor_2022']['results']

print('Finding real examples from 2022 Governor race:\n')

# Group counties by margin ranges
margin_ranges = {}
for county, cdata in gov_2022.items():
    margin_str = cdata.get('margin_pct', '')
    comp = cdata.get('competitiveness', {})
    
    # Parse margin
    if margin_str:
        party = 'R' if margin_str.startswith('R') else 'D'
        margin = float(margin_str.replace('R+', '').replace('D+', ''))
        
        # Categorize
        if margin >= 40:
            range_key = f'{party}+40%+'
        elif margin >= 30:
            range_key = f'{party}+30-40%'
        elif margin >= 20:
            range_key = f'{party}+20-30%'
        elif margin >= 10:
            range_key = f'{party}+10-20%'
        elif margin >= 5.5:
            range_key = f'{party}+5.5-10%'
        elif margin >= 1:
            range_key = f'{party}+1-5.5%'
        elif margin >= 0.5:
            range_key = f'{party}+0.5-1%'
        else:
            range_key = '±0.5%'
        
        if range_key not in margin_ranges:
            margin_ranges[range_key] = []
        margin_ranges[range_key].append({
            'county': county,
            'margin': margin_str,
            'category': comp.get('category'),
            'code': comp.get('code')
        })

# Print one example from each range
for range_key in ['R+40%+', 'R+30-40%', 'R+20-30%', 'R+10-20%', 'R+5.5-10%', 'R+1-5.5%', 'R+0.5-1%', 
                  '±0.5%',
                  'D+0.5-1%', 'D+1-5.5%', 'D+5.5-10%', 'D+10-20%', 'D+20-30%', 'D+30-40%', 'D+40%+']:
    if range_key in margin_ranges:
        example = margin_ranges[range_key][0]
        status = '✅' if range_key.replace('+', '_').replace('-', '_').replace('%', '').replace('±', 'TOSSUP').replace('.', '_') in example['code'].replace('_', '').replace('REPUBLICAN', 'R').replace('DEMOCRAT', 'D') else '❌'
        print(f'{status} {range_key:15} - {example["county"]:15} ({example["margin"]:10}) → {example["category"]:15} [{example["code"]}]')
    else:
        print(f'   {range_key:15} - No examples found')
