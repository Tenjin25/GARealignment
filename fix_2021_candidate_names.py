"""
Fix 2021 Senate runoff data to include proper candidate names
"""
import json

JSON_PATH = 'data/results_by_year_grouped.final.json'

# Load data
print("Loading data...")
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Define correct candidates for each contest
CANDIDATE_INFO = {
    'us_senate_2021': {
        'dem_candidate': 'Jon Ossoff',
        'rep_candidate': 'David Perdue'
    },
    'us_senate_special_2021': {
        'dem_candidate': 'Raphael Warnock',
        'rep_candidate': 'Kelly Loeffler'
    }
}

print("\nFixing candidate names in 2021 Senate runoffs...")

for contest_key, names in CANDIDATE_INFO.items():
    if contest_key not in data['results_by_year']['2021']:
        print(f"  WARNING: {contest_key} not found")
        continue
    
    contest_data = data['results_by_year']['2021'][contest_key]
    dem_name = names['dem_candidate']
    rep_name = names['rep_candidate']
    
    # Add candidates array at contest level if missing
    if 'candidates' not in contest_data:
        contest_data['candidates'] = [
            {'name': dem_name, 'party': 'Democrat'},
            {'name': rep_name, 'party': 'Republican'}
        ]
        print(f"\n✓ Added candidates array to {contest_key}")
        print(f"  Democrat: {dem_name}")
        print(f"  Republican: {rep_name}")
    
    # Fix all county results
    fixed_count = 0
    for county_name, result in contest_data['results'].items():
        # Update winner_name if it's generic
        if result.get('winner_name') in ['Democrat', 'Republican']:
            winner_party = result['winner_party']
            result['winner_name'] = dem_name if winner_party == 'Democrat' else rep_name
            fixed_count += 1
        
        # Update candidate names in candidates array
        if 'candidates' in result and isinstance(result['candidates'], list):
            for candidate in result['candidates']:
                if isinstance(candidate, dict):
                    if candidate.get('name') == 'Democrat':
                        candidate['name'] = dem_name
                    elif candidate.get('name') == 'Republican':
                        candidate['name'] = rep_name
    
    print(f"  Fixed {fixed_count} counties with generic candidate names")

# Create backup
import os
backup_path = JSON_PATH.replace('.json', '.backup_before_candidate_fix.json')
if not os.path.exists(backup_path):
    print("\nCreating backup...")
    import shutil
    shutil.copy(JSON_PATH, backup_path)
    print(f"✓ Backup created: {backup_path}")

# Save
print("\nSaving updated data...")
with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f"✓ Saved to {JSON_PATH}")

# Verify
print("\n" + "="*70)
print("Verification")
print("="*70)

for contest_key in CANDIDATE_INFO.keys():
    if contest_key in data['results_by_year']['2021']:
        contest_data = data['results_by_year']['2021'][contest_key]
        print(f"\n{contest_key}:")
        print(f"  Candidates: {contest_data.get('candidates', 'NOT FOUND')}")
        
        # Check a sample county
        sample_county = 'Camden'
        if sample_county in contest_data['results']:
            result = contest_data['results'][sample_county]
            print(f"  {sample_county} winner: {result['winner_name']}")
            print(f"  {sample_county} candidates: {[c['name'] for c in result.get('candidates', [])]}")

print("\n✓ Candidate names fixed!")
