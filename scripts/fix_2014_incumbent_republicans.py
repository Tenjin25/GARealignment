#!/usr/bin/env python3
"""
Fix 2014 data where Republican incumbents are marked as 'I' instead of 'REPUBLICAN'.
Moves their votes from other_votes to rep_votes and updates all related fields.
"""
import json
from copy import deepcopy

DATA_PATH = 'data/results_by_year_grouped.final.json'
OUT_PATH = 'data/results_by_year_grouped.final.json'
BACKUP_PATH = 'data/results_by_year_grouped.final.backup.json'

# Known 2014 Republican incumbents incorrectly marked as "I"
REPUBLICAN_INCUMBENTS_2014 = {
    'J. NATHAN DEAL': 'governor_2014',
    'NATHAN DEAL': 'governor_2014',
    'BRIAN P. KEMP': 'secretary_of_state_2014',
    'BRIAN KEMP': 'secretary_of_state_2014',
    'SAMUEL S. OLENS': 'attorney_general_2014',
    'SAM OLENS': 'attorney_general_2014',
    'RALPH T. HUDGENS': 'commissioner_of_insurance_2014',
    'RALPH HUDGENS': 'commissioner_of_insurance_2014',
    'J. MARK BUTLER': 'commissioner_of_labor_2014',
    'MARK BUTLER': 'commissioner_of_labor_2014',
}

def normalize_name(name):
    """Normalize candidate name for comparison."""
    if not name:
        return ''
    return str(name).strip().upper()

print('Loading data...')
with open(DATA_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Create backup
print(f'Creating backup at {BACKUP_PATH}...')
with open(BACKUP_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

results_2014 = data.get('results_by_year', {}).get('2014', {})
fixes_applied = 0

print('\nFixing 2014 Republican incumbents incorrectly marked as "I"...\n')

for contest_key, contest_obj in results_2014.items():
    results = contest_obj.get('results', {})
    
    if not isinstance(results, dict):
        continue
    
    for county, county_data in results.items():
        # Check candidates object for "I" party incumbents
        candidates = county_data.get('candidates', {})
        
        for cand_name, cand_info in candidates.items():
            cand_name_norm = normalize_name(cand_name)
            party = str(cand_info.get('party', '')).upper()
            is_incumbent = cand_info.get('incumbent', False)
            
            # Check if this is a Republican incumbent marked as "I"
            if party == 'I' and is_incumbent and cand_name_norm in REPUBLICAN_INCUMBENTS_2014:
                votes = cand_info.get('votes', 0)
                
                print(f'{contest_key} - {county}:')
                print(f'  Found Republican incumbent "{cand_name}" marked as "I" with {votes:,} votes')
                print(f'  Current: dem_votes={county_data.get("dem_votes", 0):,}, rep_votes={county_data.get("rep_votes", 0):,}, other_votes={county_data.get("other_votes", 0):,}')
                
                # Update candidate party in candidates object
                cand_info['party'] = 'REPUBLICAN'
                
                # Move votes from other_votes to rep_votes
                dem_votes = county_data.get('dem_votes', 0)
                rep_votes = votes  # This candidate's votes become rep_votes
                other_votes = county_data.get('other_votes', 0) - votes  # Subtract from other
                total_votes = county_data.get('total_votes', 0)
                
                county_data['rep_votes'] = rep_votes
                county_data['rep_candidate'] = cand_name
                county_data['other_votes'] = max(0, other_votes)
                county_data['two_party_total'] = dem_votes + rep_votes
                
                # Recalculate margin
                margin = rep_votes - dem_votes
                county_data['margin'] = margin
                
                if (dem_votes + rep_votes) > 0:
                    margin_pct = abs(margin) / (dem_votes + rep_votes) * 100
                    county_data['margin_pct'] = f'R+{margin_pct:.2f}'
                else:
                    county_data['margin_pct'] = 'R+0.00'
                
                # Update winner fields
                county_data['winner'] = 'REPUBLICAN'
                county_data['winner_party'] = 'REPUBLICAN'
                county_data['winner_name'] = cand_name
                county_data['winner_votes'] = rep_votes
                county_data['winner_incumbent'] = True
                
                # Update all_parties dict
                if 'all_parties' in county_data:
                    all_parties = county_data['all_parties']
                    if 'I' in all_parties:
                        del all_parties['I']
                    all_parties['REPUBLICAN'] = rep_votes
                
                # Recalculate competitiveness
                if (dem_votes + rep_votes) > 0:
                    margin_pct_val = abs(margin) / (dem_votes + rep_votes) * 100
                    
                    if margin_pct_val >= 40:
                        category, color = 'Annihilation', '#67000d'
                    elif margin_pct_val >= 30:
                        category, color = 'Dominant', '#a50f15'
                    elif margin_pct_val >= 20:
                        category, color = 'Stronghold', '#cb181d'
                    elif margin_pct_val >= 10:
                        category, color = 'Safe', '#ef3b2c'
                    elif margin_pct_val >= 5.5:
                        category, color = 'Likely', '#fb6a4a'
                    elif margin_pct_val >= 1:
                        category, color = 'Lean', '#fcae91'
                    elif margin_pct_val >= 0.5:
                        category, color = 'Tilt', '#fee8c8'
                    else:
                        category, color = 'Tossup', '#f7f7f7'
                    
                    county_data['competitiveness'] = {
                        'category': category,
                        'party': 'REPUBLICAN' if margin_pct_val >= 0.5 else 'TOSSUP',
                        'code': f'REPUBLICAN_{category.upper()}' if margin_pct_val >= 0.5 else 'TOSSUP',
                        'color': color
                    }
                
                print(f'  Updated: dem_votes={dem_votes:,}, rep_votes={rep_votes:,}, other_votes={other_votes:,}')
                print(f'  New margin: R+{margin_pct:.2f}%, Competitiveness: {county_data["competitiveness"]["category"]} Republican')
                fixes_applied += 1

print(f'\n✅ Total fixes applied: {fixes_applied}')

if fixes_applied > 0:
    print(f'\n💾 Writing corrected data back to {OUT_PATH}...')
    with open(OUT_PATH, 'w', encoding='utf-8') as out:
        json.dump(data, out, indent=2, ensure_ascii=False)
    print('✅ Data successfully updated!')
    print(f'📦 Backup saved at {BACKUP_PATH}')
else:
    print('ℹ️  No fixes needed.')
