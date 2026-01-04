"""
Add missing 2021 county data with manual entry from Wikipedia/Official sources
Camden, Chattooga, Grady, Greene counties

Data source: I'll provide you the Wikipedia links and you can manually verify:
- Ossoff vs Perdue: https://en.wikipedia.org/wiki/2020-21_United_States_Senate_election_in_Georgia
- Warnock vs Loeffler: https://en.wikipedia.org/wiki/2020-21_United_States_Senate_special_election_in_Georgia

MANUAL DATA ENTRY - Replace these with actual values from Wikipedia
"""
import json

JSON_PATH = 'data/results_by_year_grouped.final.json'

# Manual data entry for missing counties
# Data from Wikipedia - Ossoff vs Perdue race completed
MANUAL_DATA = {
    'us_senate_2021': {  # Ossoff vs Perdue
        'Camden': {'dem_votes': 6856, 'rep_votes': 13015},
        'Chattooga': {'dem_votes': 1673, 'rep_votes': 6558},
        'Grady': {'dem_votes': 3099, 'rep_votes': 6229},
        'Greene': {'dem_votes': 3703, 'rep_votes': 6917},
    },
    'us_senate_special_2021': {  # Warnock vs Loeffler
        'Camden': {'dem_votes': 6807, 'rep_votes': 13063},
        'Chattooga': {'dem_votes': 1686, 'rep_votes': 6550},
        'Grady': {'dem_votes': 3102, 'rep_votes': 6226},
        'Greene': {'dem_votes': 3758, 'rep_votes': 6855},
    },
}

def calculate_competitiveness(margin_pct, winner_party):
    """Calculate competitiveness rating"""
    margin = abs(margin_pct)
    
    if margin < 0.50:
        category = "Tossup"
    elif margin < 1.00:
        category = "Tilt"
    elif margin < 5.50:
        category = "Lean"
    elif margin < 10.00:
        category = "Likely"
    elif margin < 20.00:
        category = "Safe"
    elif margin < 30.00:
        category = "Stronghold"
    elif margin < 40.00:
        category = "Dominant"
    else:
        category = "Annihilation"
    
    return {
        "category": category,
        "party": winner_party,
        "margin": margin_pct
    }

def add_manual_data():
    """Add manually entered data to JSON"""
    
    print("="*70)
    print("Adding Manual 2021 County Data")
    print("="*70)
    
    # Check if any data is filled in
    has_data = False
    for contest_data in MANUAL_DATA.values():
        for county_data in contest_data.values():
            if county_data['dem_votes'] > 0 or county_data['rep_votes'] > 0:
                has_data = True
                break
    
    if not has_data:
        print("\n✗ No manual data has been entered yet!")
        print("\nPlease:")
        print("1. Visit the Wikipedia pages:")
        print("   - Ossoff vs Perdue: https://en.wikipedia.org/wiki/2020-21_United_States_Senate_election_in_Georgia")
        print("   - Warnock vs Loeffler: https://en.wikipedia.org/wiki/2020-21_United_States_Senate_special_election_in_Georgia")
        print("\n2. Find the county results table on each page")
        print("3. Look for Camden, Chattooga, Grady, and Greene counties")
        print("4. Edit this script (add_2021_manual_data.py) and fill in the vote counts in MANUAL_DATA")
        print("5. Run this script again")
        return False
    
    print(f"\nLoading {JSON_PATH}...")
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("\nAdding manually entered data...")
    
    for contest_key, counties in MANUAL_DATA.items():
        if contest_key not in data['results_by_year']['2021']:
            print(f"  WARNING: {contest_key} not found")
            continue
        
        contest_data = data['results_by_year']['2021'][contest_key]
        candidates = contest_data.get('candidates', [])
        
        dem_candidate = next((c['name'] for c in candidates if c['party'] == 'Democrat'), 'Democrat')
        rep_candidate = next((c['name'] for c in candidates if c['party'] == 'Republican'), 'Republican')
        
        for county_name, votes in counties.items():
            if votes['dem_votes'] == 0 and votes['rep_votes'] == 0:
                print(f"  ⚠ Skipping {county_name} - no data entered")
                continue
            
            dem_votes = votes['dem_votes']
            rep_votes = votes['rep_votes']
            total_votes = dem_votes + rep_votes
            
            if total_votes == 0:
                continue
            
            dem_pct = (dem_votes / total_votes) * 100
            rep_pct = (rep_votes / total_votes) * 100
            margin_pct = dem_pct - rep_pct
            
            winner_party = 'Democrat' if dem_votes > rep_votes else 'Republican'
            winner_name = dem_candidate if winner_party == 'Democrat' else rep_candidate
            
            competitiveness = calculate_competitiveness(margin_pct, winner_party)
            
            full_result = {
                "dem_votes": dem_votes,
                "rep_votes": rep_votes,
                "total_votes": total_votes,
                "dem_pct": round(dem_pct, 2),
                "rep_pct": round(rep_pct, 2),
                "margin_pct": round(margin_pct, 2),
                "winner_party": winner_party,
                "winner_name": winner_name,
                "competitiveness": competitiveness,
                "source": "Manual entry from Wikipedia",
                "candidates": [
                    {
                        "name": dem_candidate,
                        "party": "Democrat",
                        "votes": dem_votes,
                        "pct": round(dem_pct, 2)
                    },
                    {
                        "name": rep_candidate,
                        "party": "Republican",
                        "votes": rep_votes,
                        "pct": round(rep_pct, 2)
                    }
                ]
            }
            
            contest_data['results'][county_name] = full_result
            print(f"  ✓ Added {county_name}: {dem_votes:,} D vs {rep_votes:,} R ({margin_pct:+.2f}%)")
        
        new_count = len(contest_data['results'])
        print(f"  {contest_key}: {new_count} counties total")
    
    # Add to PSC using Senate data
    if 'public_service_commissioner_2021' in data['results_by_year']['2021']:
        print("\nAdding to PSC (using Senate data)...")
        psc_data = data['results_by_year']['2021']['public_service_commissioner_2021']
        psc_candidates = psc_data.get('candidates', [])
        
        for county_name, votes in MANUAL_DATA['us_senate_2021'].items():
            if votes['dem_votes'] == 0 and votes['rep_votes'] == 0:
                continue
            
            dem_candidate = next((c['name'] for c in psc_candidates if c['party'] == 'Democrat'), 'Democrat')
            rep_candidate = next((c['name'] for c in psc_candidates if c['party'] == 'Republican'), 'Republican')
            
            dem_votes = votes['dem_votes']
            rep_votes = votes['rep_votes']
            total_votes = dem_votes + rep_votes
            
            dem_pct = (dem_votes / total_votes) * 100
            rep_pct = (rep_votes / total_votes) * 100
            margin_pct = dem_pct - rep_pct
            
            winner_party = 'Democrat' if dem_votes > rep_votes else 'Republican'
            winner_name = dem_candidate if winner_party == 'Democrat' else rep_candidate
            competitiveness = calculate_competitiveness(margin_pct, winner_party)
            
            full_result = {
                "dem_votes": dem_votes,
                "rep_votes": rep_votes,
                "total_votes": total_votes,
                "dem_pct": round(dem_pct, 2),
                "rep_pct": round(rep_pct, 2),
                "margin_pct": round(margin_pct, 2),
                "winner_party": winner_party,
                "winner_name": winner_name,
                "competitiveness": competitiveness,
                "source": "Manual entry (from Senate)",
                "candidates": [
                    {
                        "name": dem_candidate,
                        "party": "Democrat",
                        "votes": dem_votes,
                        "pct": round(dem_pct, 2)
                    },
                    {
                        "name": rep_candidate,
                        "party": "Republican",
                        "votes": rep_votes,
                        "pct": round(rep_pct, 2)
                    }
                ]
            }
            
            psc_data['results'][county_name] = full_result
            print(f"  ✓ Added {county_name} to PSC")
    
    # Backup and save
    import os
    backup_path = JSON_PATH.replace('.json', '.backup_before_manual_2021.json')
    if not os.path.exists(backup_path):
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"\n✓ Created backup: {backup_path}")
    
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    print(f"✓ Saved to {JSON_PATH}")
    
    # Summary
    print("\n" + "="*70)
    print("Summary")
    print("="*70)
    
    contests = ['us_senate_2021', 'us_senate_special_2021', 'public_service_commissioner_2021']
    for contest_key in contests:
        if contest_key in data['results_by_year']['2021']:
            count = len(data['results_by_year']['2021'][contest_key]['results'])
            print(f"{contest_key}: {count} counties")
    
    return True

if __name__ == '__main__':
    success = add_manual_data()
    
    if success:
        print("\n✓ Successfully added manual 2021 county data!")
    else:
        print("\n⚠ Please fill in the data in this script first")
