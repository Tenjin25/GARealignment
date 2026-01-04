#!/usr/bin/env python3
"""Fix 2014 data where Republicans are incorrectly marked as 'I' (Independent)."""
import json
from copy import deepcopy

DATA_PATH = 'data/results_by_year_grouped.final.json'
OUT_PATH = 'data/results_by_year_grouped.fixed2014.json'

# Known 2014 Republican candidates who are incorrectly marked as "I"
REPUBLICAN_CANDIDATES_2014 = {
    'J. NATHAN DEAL',
    'NATHAN DEAL',
    'BRIAN P. KEMP',
    'BRIAN KEMP',
    'SAMUEL S. OLENS',
    'SAM OLENS',
    'RALPH T. HUDGENS',
    'RALPH HUDGENS',
    'J. MARK BUTLER',
    'MARK BUTLER',
}

def normalize_name(name):
    """Normalize candidate name for comparison."""
    if not name:
        return ''
    return str(name).strip().upper()

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

results_2014 = data.get('results_by_year', {}).get('2014', {})
new_data = deepcopy(data)
fixes_applied = 0

print('Fixing 2014 Republican candidates incorrectly marked as Independent...\n')

for contest_key, contest_obj in results_2014.items():
    results = contest_obj.get('results', {})
    
    if not isinstance(results, dict):
        continue
    
    for county, county_data in results.items():
        winner_party = county_data.get('winner_party', '')
        winner_name = normalize_name(county_data.get('winner_name', ''))
        
        # Check if this is marked as "I" but is actually a known Republican
        if winner_party == 'I' and winner_name in REPUBLICAN_CANDIDATES_2014:
            print(f'{contest_key} - {county}: Fixing {winner_name} from "I" to "REPUBLICAN"')
            
            # Update in new_data
            target = new_data['results_by_year']['2014'][contest_key]['results'][county]
            target['winner_party'] = 'REPUBLICAN'
            target['winner'] = 'REPUBLICAN'
            
            # Also fix rep_votes vs dem_votes if needed
            dem_votes = target.get('dem_votes', 0)
            rep_votes = target.get('rep_votes', 0)
            winner_votes = target.get('winner_votes', 0)
            
            # If rep_votes is 0 but winner_votes is not, swap them
            if rep_votes == 0 and winner_votes > 0:
                print(f'  Also swapping dem_votes ({dem_votes}) <-> rep_votes ({rep_votes}), winner_votes={winner_votes}')
                target['rep_votes'] = winner_votes
                target['dem_votes'] = dem_votes
                # Recalculate margin
                total = target.get('two_party_total', 0) or (winner_votes + dem_votes)
                if total > 0:
                    margin = winner_votes - dem_votes
                    margin_pct = abs(margin) / total * 100
                    target['margin'] = margin
                    target['margin_pct'] = f'R+{margin_pct:.2f}'
            
            # Fix competitiveness if needed
            margin_pct_str = target.get('margin_pct', '')
            if margin_pct_str and isinstance(margin_pct_str, str):
                # Parse margin
                try:
                    if margin_pct_str.startswith('D+'):
                        # Change to R+
                        margin_val = float(margin_pct_str[2:])
                        target['margin_pct'] = f'R+{margin_val:.2f}'
                        print(f'  Changed margin from {margin_pct_str} to R+{margin_val:.2f}')
                except:
                    pass
            
            # Update competitiveness object
            if 'competitiveness' in target:
                comp = target['competitiveness']
                if comp.get('party') in ('I', 'INDEPENDENT'):
                    comp['party'] = 'REPUBLICAN'
                    code = comp.get('code', '')
                    if code.startswith('I_') or code.startswith('INDEPENDENT_'):
                        category = comp.get('category', 'Safe')
                        comp['code'] = f'REPUBLICAN_{category.upper()}'
                    print(f'  Updated competitiveness party to REPUBLICAN')
            
            fixes_applied += 1

print(f'\nTotal fixes applied: {fixes_applied}')

if fixes_applied > 0:
    with open(OUT_PATH, 'w', encoding='utf-8') as out:
        json.dump(new_data, out, indent=2, ensure_ascii=False)
    print(f'Written corrected data to {OUT_PATH}')
    print('\nTo apply these fixes, run:')
    print(f'  copy {OUT_PATH} {DATA_PATH}')
else:
    print('No fixes needed.')
