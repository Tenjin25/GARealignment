"""
Process 2008 U.S. Senate Runoff data and add it to results_by_year_grouped.final.json
Race: Jim Martin (D) vs. Saxby Chambliss (R)
"""
import json
import csv
from collections import defaultdict

# File paths
CSV_PATH = 'data/20081202__ga__general__runoff.csv'
JSON_PATH = 'data/results_by_year_grouped.final.json'

def calculate_competitiveness(margin_pct, winner_party):
    """Calculate competitiveness rating based on margin"""
    margin = abs(margin_pct)
    
    # Correct thresholds matching index.html:
    # Tossup <0.5%, Tilt 0.5-0.99%, Lean 1-5.49%, Likely 5.5-9.99%, 
    # Safe 10-19.99%, Stronghold 20-29.99%, Dominant 30-39.99%, Annihilation 40%+
    if margin < 0.5:
        category = "Tossup"
    elif margin < 1:
        category = "Tilt"
    elif margin < 5.5:
        category = "Lean"
    elif margin < 10:
        category = "Likely"
    elif margin < 20:
        category = "Safe"
    elif margin < 30:
        category = "Stronghold"
    elif margin < 40:
        category = "Dominant"
    else:
        category = "Annihilation"
    
    return {
        "category": category,
        "party": winner_party,
        "margin": margin_pct
    }

def process_2008_senate_runoff():
    """Process the 2008 Senate Runoff CSV and aggregate by county"""
    
    print("Processing 2008 U.S. Senate Runoff data...")
    
    # Read and aggregate county results
    county_results = defaultdict(lambda: {'Democrat': 0, 'Republican': 0})
    candidates = {}
    
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            county = row['county'].strip().title()
            office = row['office'].strip()
            party = row['party'].strip()
            candidate = row['candidate'].strip()
            votes = int(row['votes'])
            
            # Only process U.S. Senate races
            if office == 'U.S. Senate':
                county_results[county][party] += votes
                if party not in candidates:
                    candidates[party] = candidate
    
    print(f"Found {len(county_results)} counties")
    print(f"Candidates: {candidates}")
    
    # Create structured results
    structured_results = {}
    
    for county, votes in county_results.items():
        dem_votes = votes['Democrat']
        rep_votes = votes['Republican']
        total_votes = dem_votes + rep_votes
        
        if total_votes == 0:
            continue
        
        dem_pct = (dem_votes / total_votes) * 100
        rep_pct = (rep_votes / total_votes) * 100
        margin_pct = dem_pct - rep_pct
        
        winner_party = 'Democrat' if dem_votes > rep_votes else 'Republican'
        winner_name = candidates['Democrat'] if winner_party == 'Democrat' else candidates['Republican']
        
        competitiveness = calculate_competitiveness(margin_pct, winner_party)
        
        structured_results[county] = {
            "dem_votes": dem_votes,
            "rep_votes": rep_votes,
            "total_votes": total_votes,
            "dem_pct": round(dem_pct, 2),
            "rep_pct": round(rep_pct, 2),
            "margin_pct": round(margin_pct, 2),
            "winner_party": winner_party,
            "winner_name": winner_name,
            "competitiveness": competitiveness,
            "candidates": [
                {
                    "name": candidates['Democrat'],
                    "party": "Democrat",
                    "votes": dem_votes,
                    "pct": round(dem_pct, 2)
                },
                {
                    "name": candidates['Republican'],
                    "party": "Republican",
                    "votes": rep_votes,
                    "pct": round(rep_pct, 2)
                }
            ]
        }
    
    return structured_results, candidates

def add_to_main_json(senate_results, candidates):
    """Add 2008 Senate Runoff to the main JSON file"""
    
    print(f"\nLoading {JSON_PATH}...")
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Check if 2008 year exists
    if '2008' not in data['results_by_year']:
        print("ERROR: 2008 not found in results_by_year")
        return
    
    # Add the Senate Runoff contest
    contest_key = 'us_senate_runoff_2008'
    
    data['results_by_year']['2008'][contest_key] = {
        "contest_name": "U.S. Senate Runoff",
        "contest_type": "us_senate",
        "year": 2008,
        "is_statewide": True,
        "candidates": [
            {
                "name": candidates['Democrat'],
                "party": "Democrat"
            },
            {
                "name": candidates['Republican'],
                "party": "Republican"
            }
        ],
        "results": senate_results
    }
    
    print(f"\n✓ Added {contest_key} with {len(senate_results)} counties")
    
    # Create backup
    import os
    backup_path = JSON_PATH.replace('.json', '.backup_before_2008_runoff.json')
    if not os.path.exists(backup_path):
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"✓ Created backup: {backup_path}")
    
    # Save updated data
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    print(f"✓ Saved to {JSON_PATH}")
    print(f"\n2008 contests now include:")
    for contest in data['results_by_year']['2008'].keys():
        count = len(data['results_by_year']['2008'][contest].get('results', {}))
        print(f"  - {contest}: {count} counties")

if __name__ == '__main__':
    senate_results, candidates = process_2008_senate_runoff()
    
    # Show sample results
    print("\nSample results:")
    for county in list(senate_results.keys())[:5]:
        result = senate_results[county]
        print(f"{county}: {result['winner_name']} {result['margin_pct']:+.2f}%")
    
    add_to_main_json(senate_results, candidates)
    
    print("\n✓ 2008 U.S. Senate Runoff successfully added!")
