"""
Fix the structure of manually added counties to match existing data format
For 2008 runoff and 2021 runoffs
"""
import json

JSON_PATH = 'data/results_by_year_grouped.final.json'

print("Loading data...")
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Contest information - for 2021 only specific counties need fixing
MANUAL_COUNTIES_2021 = ['Camden', 'Chattooga', 'Grady', 'Greene']

# Contest information
CONTESTS = {
    '2008': {
        'us_senate_runoff_2008': {
            'dem_candidate': 'Jim Martin',
            'rep_candidate': 'Saxby Chambliss',
            'contest': 'U.S. Senate Runoff',
            'year': '2008',
            'all_counties': True  # Fix all counties
        }
    },
    '2021': {
        'us_senate_2021': {
            'dem_candidate': 'Jon Ossoff',
            'rep_candidate': 'David A. Perdue',
            'contest': 'U.S. Senate',
            'year': '2021',
            'manual_only': True  # Fix only manually added counties
        },
        'us_senate_special_2021': {
            'dem_candidate': 'Raphael Warnock',
            'rep_candidate': 'Kelly Loeffler',
            'contest': 'U.S. Senate Special',
            'year': '2021',
            'manual_only': True  # Fix only manually added counties
        }
    }
}

print("\nFixing structure of contest data...")

for year, contests in CONTESTS.items():
    for contest_key, contest_info in contests.items():
        if contest_key not in data['results_by_year'][year]:
            print(f"  WARNING: {contest_key} not found in {year}")
            continue
        
        contest_data = data['results_by_year'][year][contest_key]
        
        print(f"\n{year} - {contest_key}:")
        
        # Determine which counties to fix
        if contest_info.get('all_counties'):
            counties_to_fix = list(contest_data['results'].keys())
        else:
            counties_to_fix = MANUAL_COUNTIES_2021
        
        for county in counties_to_fix:
            if county not in contest_data['results']:
                continue
            
            result = contest_data['results'][county]
            
            # Add missing fields to match the structure
            if 'dem_candidate' not in result:
                result['dem_candidate'] = contest_info['dem_candidate']
            if 'rep_candidate' not in result:
                result['rep_candidate'] = contest_info['rep_candidate']
            if 'other_votes' not in result:
                result['other_votes'] = 0
            if 'two_party_total' not in result:
                result['two_party_total'] = result['total_votes']
            if 'margin' not in result:
                result['margin'] = result['rep_votes'] - result['dem_votes']
            
            # Format margin_pct properly
            margin = result['margin_pct']
            if isinstance(margin, (int, float)):
                if margin > 0:
                    result['margin_pct'] = f"D+{abs(margin):.2f}"
                else:
                    result['margin_pct'] = f"R+{abs(margin):.2f}"
            
            # Add winner fields
            if 'winner' not in result:
                result['winner'] = result['winner_party'].upper()
            if 'winner_incumbent' not in result:
                result['winner_incumbent'] = False
            if 'winner_votes' not in result:
                result['winner_votes'] = result['rep_votes'] if result['winner_party'] == 'Republican' else result['dem_votes']
            
            # Fix competitiveness structure
            if 'competitiveness' in result:
                comp = result['competitiveness']
                if 'code' not in comp:
                    comp['code'] = f"{comp['party'].upper()}_{comp['category'].upper()}"
                if 'color' not in comp:
                    # Add color based on category
                    colors = {
                        'Annihilation': {'Republican': '#67000d', 'Democrat': '#08306b'},
                        'Dominant': {'Republican': '#a50f15', 'Democrat': '#08519c'},
                        'Stronghold': {'Republican': '#cb181d', 'Democrat': '#3182bd'},
                        'Safe': {'Republican': '#ef3b2c', 'Democrat': '#6baed6'},
                        'Likely': {'Republican': '#fb6a4a', 'Democrat': '#9ecae1'},
                        'Lean': {'Republican': '#fcae91', 'Democrat': '#c6dbef'},
                        'Tilt': {'Republican': '#fee8c8', 'Democrat': '#e1f5fe'},
                        'Tossup': {'Republican': '#f7f7f7', 'Democrat': '#f7f7f7'}
                    }
                    comp['color'] = colors.get(comp['category'], {}).get(comp['party'], '#f7f7f7')
            
            # Add all_parties
            if 'all_parties' not in result:
                result['all_parties'] = {
                    'REPUBLICAN': result['rep_votes'],
                    'DEMOCRAT': result['dem_votes']
                }
            
            # Fix candidates structure to match existing format
            if 'candidates' in result and isinstance(result['candidates'], list):
                # Convert list to dict
                candidates_dict = {}
                for candidate in result['candidates']:
                    candidates_dict[candidate['name']] = {
                        'votes': candidate['votes'],
                        'party': candidate['party'].upper(),
                        'incumbent': False
                    }
                result['candidates'] = candidates_dict
            
            # Add contest metadata
            if 'contest' not in result:
                result['contest'] = contest_info['contest']
            if 'county' not in result:
                result['county'] = county
            if 'year' not in result:
                result['year'] = contest_info['year']
        
        fixed_count = len(counties_to_fix)
        print(f"  ✓ Fixed {fixed_count} counties")

# Create backup
import os
backup_path = JSON_PATH.replace('.json', '.backup_before_structure_fix.json')
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
# Check 2008 runoff
print("\n2008 us_senate_runoff_2008 - Fulton:")
sample_2008 = data['results_by_year']['2008']['us_senate_runoff_2008']['results']['Fulton']
print(f"  dem_candidate: {sample_2008.get('dem_candidate', 'MISSING')}")
print(f"  rep_candidate: {sample_2008.get('rep_candidate', 'MISSING')}")
print(f"  winner_name: {sample_2008.get('winner_name', 'MISSING')}")
print(f"  margin_pct: {sample_2008.get('margin_pct', 'MISSING')}")
print(f"  candidates: {list(sample_2008.get('candidates', {}).keys())}")

# Check 2021 manually added counties
for year, contests in CONTESTS.items():
    if year == '2021':
        for contest_key in contests.keys():
            contest_data = data['results_by_year'][year][contest_key]
            sample = contest_data['results']['Camden']
            
            print(f"\n{year} {contest_key} - Camden:")
            print(f"  dem_candidate: {sample.get('dem_candidate', 'MISSING')}")
            print(f"  rep_candidate: {sample.get('rep_candidate', 'MISSING')}")
            print(f"  winner_name: {sample.get('winner_name', 'MISSING')}")
            print(f"  margin_pct: {sample.get('margin_pct', 'MISSING')}")
            print(f"  candidates: {list(sample.get('candidates', {}).keys())}")

print("\n✓ Structure fixed!")
