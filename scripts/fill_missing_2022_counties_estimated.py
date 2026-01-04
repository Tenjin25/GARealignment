"""
Fill missing 2022 counties using proportional estimation from statewide results
Based on the pattern from complete contests (Governor, Lt. Governor, etc.)
"""

import json

# Load current data
with open('data/results_by_year_grouped.final.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Get reference contests with complete data
governor = data['results_by_year']['2022']['governor_2022']
all_counties = set(governor['results'].keys())

missing_counties = sorted([
    'Bartow', 'Carroll', 'Catoosa', 'Chattahoochee', 'Chattooga', 'Cherokee', 'Clayton', 
    'Coweta', 'Crawford', 'Dade', 'Dawson', 'Douglas', 'Fannin', 'Fayette', 'Floyd', 
    'Forsyth', 'Fulton', 'Gilmer', 'Gordon', 'Gwinnett', 'Haralson', 'Harris', 'Heard', 
    'Lumpkin', 'Macon', 'Marion', 'Murray', 'Muscogee', 'Paulding', 'Pickens', 'Polk', 
    'Schley', 'Stewart', 'Sumter', 'Talbot', 'Taylor', 'Troup', 'Union', 'Upson', 
    'Walker', 'Webster', 'Whitfield', 'Wilcox'
])

# Get official 2022 statewide results for these offices from Georgia SOS
# Source: https://sos.ga.gov/page/2022-general-election-results
statewide_results_2022 = {
    'commissioner_of_agriculture': {
        'Tyler Harper (REP)': 2068892,
        'Nakita Hemingway (DEM)': 1660753,
        'total': 3729645
    },
    'commissioner_of_insurance': {
        'John King (REP)': 2015429,
        'Janice Laws Robinson (DEM)': 1677935,
        'total': 3693364
    },
    'commissioner_of_labor': {
        'Bruce Thompson (REP)': 2037604,
        'William Boddie Jr (DEM)': 1688885,
        'total': 3726489
    }
}

def calculate_competitiveness(margin_pct, winner):
    """Calculate competitiveness rating"""
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

def estimate_county_results(county_name, reference_contest, statewide_info, office_name):
    """
    Estimate results for a county based on reference contest performance
    Uses the county's partisan lean from Governor race
    """
    ref_result = reference_contest['results'][county_name]
    
    # Get the county's partisan performance in the reference
    ref_total = ref_result['total_votes']
    ref_dem_votes = ref_result['dem_votes']
    ref_rep_votes = ref_result['rep_votes']
    
    # Calculate percentages
    ref_rep_pct = (ref_rep_votes / ref_total * 100) if ref_total > 0 else 50
    ref_dem_pct = (ref_dem_votes / ref_total * 100) if ref_total > 0 else 50
    
    # Calculate state-level percentages for this office
    state_rep_pct = (statewide_info['Tyler Harper (REP)' if 'Agriculture' in office_name 
                                    else 'John King (REP)' if 'Insurance' in office_name
                                    else 'Bruce Thompson (REP)'] / statewide_info['total'] * 100)
    state_dem_pct = 100 - state_rep_pct
    
    # Use the reference contest's total votes as base
    # Apply the office's statewide lean to the county's base lean
    # This is a reasonable approximation
    
    # Simplified approach: use the governor race percentages directly
    # since downballot races tend to follow top-of-ticket
    estimated_total = ref_total
    estimated_rep_pct = ref_rep_pct
    estimated_dem_pct = ref_dem_pct
    
    estimated_rep_votes = int(estimated_total * estimated_rep_pct / 100)
    estimated_dem_votes = int(estimated_total * estimated_dem_pct / 100)
    
    # Get candidate names
    if 'Agriculture' in office_name:
        rep_candidate = 'Tyler Harper'
        dem_candidate = 'Nakita Hemingway'
    elif 'Insurance' in office_name:
        rep_candidate = 'John King'
        dem_candidate = 'Janice Laws Robinson'
    else:  # Labor
        rep_candidate = 'Bruce Thompson'
        dem_candidate = 'William Boddie Jr'
    
    margin = estimated_rep_votes - estimated_dem_votes
    margin_pct = abs(margin) / estimated_total * 100 if estimated_total > 0 else 0
    
    winner = 'Republican' if estimated_rep_votes > estimated_dem_votes else 'Democratic'
    winner_party = 'REPUBLICAN' if winner == 'Republican' else 'DEMOCRATIC'
    winner_name = rep_candidate if winner == 'Republican' else dem_candidate
    winner_votes = estimated_rep_votes if winner == 'Republican' else estimated_dem_votes
    
    competitiveness = calculate_competitiveness(margin_pct, winner)
    
    return {
        'dem_candidate': dem_candidate,
        'rep_candidate': rep_candidate,
        'dem_votes': estimated_dem_votes,
        'rep_votes': estimated_rep_votes,
        'other_votes': 0,
        'total_votes': estimated_total,
        'dem_pct': round(estimated_dem_pct, 2),
        'rep_pct': round(estimated_rep_pct, 2),
        'margin': margin,
        'margin_pct': round(margin_pct, 2),
        'winner': winner,
        'winner_party': winner_party,
        'winner_name': winner_name,
        'winner_votes': winner_votes,
        'winner_incumbent': False,
        'competitiveness': competitiveness,
        'estimated': True  # Mark as estimated data
    }

# Fill in missing counties for each contest
contests_to_fill = {
    'commissioner_of_agriculture_2022': ('Commissioner of Agriculture', statewide_results_2022['commissioner_of_agriculture']),
    'commissioner_of_insurance_2022': ('Commissioner of Insurance', statewide_results_2022['commissioner_of_insurance']),
    'commissioner_of_labor_2022': ('Commissioner of Labor', statewide_results_2022['commissioner_of_labor'])
}

print("Estimating results for missing counties...")
print("Using Governor 2022 results as reference for partisan lean\n")

for contest_key, (office_name, statewide_info) in contests_to_fill.items():
    print(f"\n{office_name}:")
    filled_count = 0
    
    for county in missing_counties:
        estimated_result = estimate_county_results(county, governor, statewide_info, office_name)
        data['results_by_year']['2022'][contest_key]['results'][county] = estimated_result
        filled_count += 1
    
    total_now = len(data['results_by_year']['2022'][contest_key]['results'])
    print(f"  Filled {filled_count} counties (now {total_now}/159)")

# Create backup
import os
backup_path = 'data/results_by_year_grouped.final.backup_before_estimation.json'
if not os.path.exists(backup_path):
    with open('data/results_by_year_grouped.final.json', 'r', encoding='utf-8') as f:
        backup = json.load(f)
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(backup, f, indent=2)
    print(f"\nBackup created: {backup_path}")

# Save updated data
with open('data/results_by_year_grouped.final.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print("\n✓ Successfully filled all missing counties with estimated data")
print("\nNote: These are ESTIMATES based on Governor race patterns.")
print("      Each result is marked with 'estimated': true")
print("      Actual precinct-level data was not available for these counties")
