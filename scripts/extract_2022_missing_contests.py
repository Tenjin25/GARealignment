import json
import os

# Load the raw 2022 data
with open('ga_2022_sos_raw2.json', 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

# Load the current election data
with open('data/results_by_year_grouped.final.json', 'r', encoding='utf-8') as f:
    election_data = json.load(f)

# Target contests to extract (indices 5-8 from the ballot items list)
target_contests = {
    5: 'commissioner_of_agriculture_2022',
    6: 'commissioner_of_insurance_2022',
    7: 'state_school_superintendent_2022',
    8: 'commissioner_of_labor_2022'
}

ballot_items = raw_data.get('ballotItems', [])
localities = raw_data.get('jurisdiction', {}).get('childLocalities', [])

# Create a map of locality IDs to names
locality_map = {}
for loc in localities:
    loc_id = loc.get('id')
    loc_name_obj = loc.get('name', [{}])
    if isinstance(loc_name_obj, list) and len(loc_name_obj) > 0:
        loc_name = loc_name_obj[0].get('text', '')
        # Clean county name (remove " County")
        loc_name = loc_name.replace(' County', '')
        locality_map[loc_id] = loc_name

print(f"Found {len(locality_map)} counties")

# Process each target contest
for idx, contest_key in target_contests.items():
    if idx >= len(ballot_items):
        print(f"Warning: Index {idx} out of range")
        continue
    
    contest = ballot_items[idx]
    contest_name_obj = contest.get('name', [{}])
    if isinstance(contest_name_obj, list) and len(contest_name_obj) > 0:
        contest_name = contest_name_obj[0].get('text', '')
    else:
        contest_name = ''
    
    print(f"\nProcessing: {contest_name} -> {contest_key}")
    
    # Initialize contest structure
    contest_data = {
        'contest_name': contest_name,
        'results': {}
    }
    
    # Get the breakdown for this contest
    breakdown_id = contest.get('id')
    breakdown_data = None
    
    # Find the breakdown data
    for item in raw_data.get('ballotItemWithBreakdown', []):
        if item.get('id') == breakdown_id:
            breakdown_data = item
            break
    
    if not breakdown_data:
        print(f"  Warning: No breakdown data found for {contest_name}")
        continue
    
    # Process county results
    local_results = breakdown_data.get('localityResults', [])
    
    for loc_result in local_results:
        locality_id = loc_result.get('localityId')
        county_name = locality_map.get(locality_id, 'Unknown')
        
        if county_name == 'Unknown':
            continue
        
        candidates_data = loc_result.get('candidates', [])
        
        # Find Democratic and Republican candidates
        dem_candidate = None
        rep_candidate = None
        dem_votes = 0
        rep_votes = 0
        other_votes = 0
        total_votes = 0
        
        for cand in candidates_data:
            party_obj = cand.get('party', [{}])
            if isinstance(party_obj, list) and len(party_obj) > 0:
                party = party_obj[0].get('text', '')
            else:
                party = ''
            
            name_obj = cand.get('name', [{}])
            if isinstance(name_obj, list) and len(name_obj) > 0:
                name = name_obj[0].get('text', '')
            else:
                name = ''
            
            votes = int(cand.get('votes', 0) or 0)
            total_votes += votes
            
            if party == 'Democratic' or party == 'Democrat':
                dem_candidate = name
                dem_votes = votes
            elif party == 'Republican':
                rep_candidate = name
                rep_votes = votes
            else:
                other_votes += votes
        
        if total_votes == 0:
            continue
        
        # Calculate percentages and margin
        dem_pct = (dem_votes / total_votes * 100) if total_votes > 0 else 0
        rep_pct = (rep_votes / total_votes * 100) if total_votes > 0 else 0
        margin = rep_votes - dem_votes
        margin_pct = abs(margin) / total_votes * 100 if total_votes > 0 else 0
        
        # Determine winner
        if rep_votes > dem_votes:
            winner = 'Republican'
            winner_party = 'REPUBLICAN'
            winner_name = rep_candidate
            winner_votes = rep_votes
        else:
            winner = 'Democratic'
            winner_party = 'DEMOCRATIC'
            winner_name = dem_candidate
            winner_votes = dem_votes
        
        # Calculate competitiveness
        def get_competitiveness(margin_pct, winner):
            if margin_pct >= 40:
                return f"{winner} Annihilation"
            elif margin_pct >= 30:
                return f"{winner} Dominant"
            elif margin_pct >= 20:
                return f"{winner} Stronghold"
            elif margin_pct >= 10:
                return f"{winner} Safe"
            elif margin_pct >= 5.5:
                return f"{winner} Likely"
            elif margin_pct >= 1:
                return f"{winner} Lean"
            elif margin_pct >= 0.5:
                return f"{winner} Tilt"
            else:
                return "Tossup"
        
        competitiveness = get_competitiveness(margin_pct, winner)
        
        # Store county result
        contest_data['results'][county_name] = {
            'dem_candidate': dem_candidate,
            'rep_candidate': rep_candidate,
            'dem_votes': dem_votes,
            'rep_votes': rep_votes,
            'other_votes': other_votes,
            'total_votes': total_votes,
            'dem_pct': round(dem_pct, 2),
            'rep_pct': round(rep_pct, 2),
            'margin': margin,
            'margin_pct': round(margin_pct, 2),
            'winner': winner,
            'winner_party': winner_party,
            'winner_name': winner_name,
            'winner_votes': winner_votes,
            'winner_incumbent': False,  # We don't have incumbent data
            'competitiveness': competitiveness
        }
    
    print(f"  Extracted {len(contest_data['results'])} counties")
    
    # Add to election data
    if '2022' not in election_data['results_by_year']:
        election_data['results_by_year']['2022'] = {}
    
    election_data['results_by_year']['2022'][contest_key] = contest_data

# Create backup
backup_path = 'data/results_by_year_grouped.final.backup_before_2022_addition.json'
if not os.path.exists(backup_path):
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(election_data, f, indent=2)
    print(f"\nBackup created: {backup_path}")

# Save updated data
with open('data/results_by_year_grouped.final.json', 'w', encoding='utf-8') as f:
    json.dump(election_data, f, indent=2)

print("\n✓ Successfully added missing 2022 contests to data/results_by_year_grouped.final.json")
print("\nNew 2022 contests:")
for key in sorted(election_data['results_by_year']['2022'].keys()):
    print(f"  - {key}")
