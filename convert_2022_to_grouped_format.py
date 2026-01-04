#!/usr/bin/env python3
"""
Convert aggregated 2022 data to match the results_by_year_grouped.final.json format
"""
import json
import os

# Load the aggregated data
aggregated_path = 'data_files/Election_Data_GA.v04/aggregated_by_county.json'
output_path = 'data/results_by_year_grouped.final.json'

print("Loading aggregated data...")
with open(aggregated_path, 'r', encoding='utf-8') as f:
    aggregated = json.load(f)

print("Loading existing results...")
with open(output_path, 'r', encoding='utf-8') as f:
    results = json.load(f)

# Office mappings to match the existing format
office_mapping = {
    'U.S. Senate': 'us_senate_2022',
    'Governor': 'governor_2022',
    'Lieutenant Governor': 'lieutenant_governor_2022',
    'Secretary of State': 'secretary_of_state_2022',
    'Attorney General': 'attorney_general_2022',
    'Commissioner of Agriculture': 'commissioner_of_agriculture_2022',
    'Commissioner of Insurance': 'commissioner_of_insurance_2022',
    'Commissioner of Labor': 'commissioner_of_labor_2022',
    'STATE SCHOOL SUPERINTENDENT': 'school_superintendent_2022',
}

# Contest name mappings
contest_names = {
    'us_senate_2022': 'U.S. Senate',
    'us_senate_runoff_2022': 'U.S. Senate Runoff',
    'governor_2022': 'Governor',
    'lieutenant_governor_2022': 'Lieutenant Governor',
    'secretary_of_state_2022': 'Secretary of State',
    'attorney_general_2022': 'Attorney General',
    'commissioner_of_agriculture_2022': 'Commissioner of Agriculture',
    'commissioner_of_insurance_2022': 'Commissioner of Insurance',
    'commissioner_of_labor_2022': 'Commissioner of Labor',
    'school_superintendent_2022': 'State School Superintendent',
}

# Ensure 2022 year exists
if 'results_by_year' not in results:
    results['results_by_year'] = {}

# Remove existing 2022 data to avoid duplicates
if '2022' in results['results_by_year']:
    print("Removing existing 2022 data to avoid duplicates...")
    del results['results_by_year']['2022']

results['results_by_year']['2022'] = {}

# County name fixes for consistency
def fix_county_name(name):
    """Standardize county names to match existing data"""
    name = name.strip()
    # Special cases for Mc/Mac counties
    if name.lower() == 'mcduffie':
        return 'McDuffie'
    elif name.lower() == 'mcintosh':
        return 'McIntosh'
    elif name.lower() == 'dekalb':
        return 'DeKalb'
    else:
        return name.title()

def fix_candidate_name(name):
    """Properly format candidate names"""
    if not name:
        return name
    
    # Handle special name patterns
    name = name.strip()
    
    # Split by space and capitalize each word
    parts = name.split()
    fixed_parts = []
    
    for part in parts:
        # Handle apostrophes (O'Brien, D'Angelo)
        if "'" in part:
            subparts = part.split("'")
            part = "'".join([sp.capitalize() for sp in subparts])
        # Handle hyphens (Mary-Jane)
        elif "-" in part:
            subparts = part.split("-")
            part = "-".join([sp.capitalize() for sp in subparts])
        # Handle McDonald, McIntosh, etc
        elif part.lower().startswith('mc') and len(part) > 2:
            part = 'Mc' + part[2:].capitalize()
        # Handle MacDonald, MacArthur, etc
        elif part.lower().startswith('mac') and len(part) > 3:
            part = 'Mac' + part[3:].capitalize()
        # Handle quotes (Jennifer "Jen" Jordan)
        elif '"' in part:
            part = part  # Keep as is
        else:
            part = part.capitalize()
        
        fixed_parts.append(part)
    
    return ' '.join(fixed_parts)

print("\nProcessing 2022 general election data...")

# Get 2022 general data
if '2022_general' in aggregated['results']:
    general_data = aggregated['results']['2022_general']
    
    for county_raw, offices in general_data.items():
        county = fix_county_name(county_raw)
        
        for office, candidates_dict in offices.items():
            if office not in office_mapping:
                continue
            
            contest_key = office_mapping[office]
            
            # Initialize contest if not exists
            if contest_key not in results['results_by_year']['2022']:
                results['results_by_year']['2022'][contest_key] = {'results': {}}
            
            # Parse candidates
            dem_candidate = None
            rep_candidate = None
            dem_votes = 0
            rep_votes = 0
            all_parties = {}
            candidates = {}
            
            for key, votes in candidates_dict.items():
                if '_' not in key:
                    continue
                party, candidate_raw = key.split('_', 1)
                candidate = fix_candidate_name(candidate_raw)
                
                candidates[candidate] = {
                    'votes': votes,
                    'party': party.upper(),
                    'incumbent': False  # Would need to look this up
                }
                
                if party.upper() not in all_parties:
                    all_parties[party.upper()] = 0
                all_parties[party.upper()] += votes
                
                if party.upper() == 'DEMOCRAT':
                    dem_candidate = candidate
                    dem_votes += votes
                elif party.upper() == 'REPUBLICAN':
                    rep_candidate = candidate
                    rep_votes += votes
            
            # Calculate totals and margins
            total_votes = sum(all_parties.values())
            two_party_total = dem_votes + rep_votes
            other_votes = total_votes - two_party_total
            
            # Determine winner first
            winner_party = 'REPUBLICAN' if rep_votes > dem_votes else 'DEMOCRAT'
            winner_name = rep_candidate if rep_votes > dem_votes else dem_candidate
            winner_votes = max(rep_votes, dem_votes)
            
            # Margin of victory (winner's votes - loser's votes)
            margin = rep_votes - dem_votes if winner_party == 'REPUBLICAN' else dem_votes - rep_votes
            
            if two_party_total > 0:
                margin_pct = (margin / two_party_total) * 100
                margin_str = f"{'R' if winner_party == 'REPUBLICAN' else 'D'}+{margin_pct:.2f}"
            else:
                margin_str = "N/A"
            
            # Determine competitiveness based on margin percentage
            if two_party_total > 0:
                margin_pct_value = (margin / two_party_total) * 100
                
                if margin_pct_value >= 40:
                    comp_category = "Annihilation"
                    color = "#67000d" if winner_party == "REPUBLICAN" else "#08306b"
                    code = f"{winner_party}_ANNIHILATION"
                elif margin_pct_value >= 30:
                    comp_category = "Dominant"
                    color = "#a50f15" if winner_party == "REPUBLICAN" else "#08519c"
                    code = f"{winner_party}_DOMINANT"
                elif margin_pct_value >= 20:
                    comp_category = "Stronghold"
                    color = "#cb181d" if winner_party == "REPUBLICAN" else "#3182bd"
                    code = f"{winner_party}_STRONGHOLD"
                elif margin_pct_value >= 10:
                    comp_category = "Safe"
                    color = "#ef3b2c" if winner_party == "REPUBLICAN" else "#6baed6"
                    code = f"{winner_party}_SAFE"
                elif margin_pct_value >= 5.5:
                    comp_category = "Likely"
                    color = "#fb6a4a" if winner_party == "REPUBLICAN" else "#9ecae1"
                    code = f"{winner_party}_LIKELY"
                elif margin_pct_value >= 1.0:
                    comp_category = "Lean"
                    color = "#fcae91" if winner_party == "REPUBLICAN" else "#c6dbef"
                    code = f"{winner_party}_LEAN"
                elif margin_pct_value >= 0.5:
                    comp_category = "Tilt"
                    color = "#fee8c8" if winner_party == "REPUBLICAN" else "#e1f5fe"
                    code = f"{winner_party}_TILT"
                else:
                    comp_category = "Tossup"
                    color = "#f7f7f7"
                    code = "TOSSUP"
            else:
                comp_category = "Unknown"
                color = "#cccccc"
                code = "UNKNOWN"
            
            # Build county result
            county_result = {
                'dem_candidate': dem_candidate,
                'rep_candidate': rep_candidate,
                'dem_votes': dem_votes,
                'rep_votes': rep_votes,
                'other_votes': other_votes,
                'total_votes': total_votes,
                'two_party_total': two_party_total,
                'margin': margin,
                'margin_pct': margin_str,
                'winner': winner_party,
                'winner_name': winner_name,
                'winner_party': winner_party,
                'winner_incumbent': False,
                'winner_votes': winner_votes,
                'competitiveness': {
                    'category': comp_category,
                    'party': winner_party if comp_category != 'Tossup' else None,
                    'code': code,
                    'color': color
                },
                'all_parties': all_parties,
                'candidates': candidates,
                'contest': contest_names.get(contest_key, office),
                'county': county,
                'year': '2022'
            }
            
            results['results_by_year']['2022'][contest_key]['results'][county] = county_result

print(f"\nProcessed {len(results['results_by_year']['2022'])} contests for 2022 general")

# Process 2022 runoff (U.S. Senate)
print("\nProcessing 2022 Senate runoff...")

if '2022_runoff' in aggregated['results']:
    runoff_data = aggregated['results']['2022_runoff']
    contest_key = 'us_senate_runoff_2022'
    
    # Initialize contest
    results['results_by_year']['2022'][contest_key] = {'results': {}}
    
    for county_raw, offices in runoff_data.items():
        county = fix_county_name(county_raw)
        
        # Look for U.S. Senate in the offices
        for office, candidates_dict in offices.items():
            if 'Senate' not in office:
                continue
            
            # Parse candidates (same logic as before)
            dem_candidate = None
            rep_candidate = None
            dem_votes = 0
            rep_votes = 0
            all_parties = {}
            candidates = {}
            
            for key, votes in candidates_dict.items():
                if '_' not in key:
                    continue
                party, candidate_raw = key.split('_', 1)
                candidate = fix_candidate_name(candidate_raw)
                
                candidates[candidate] = {
                    'votes': votes,
                    'party': party.upper(),
                    'incumbent': False
                }
                
                if party.upper() not in all_parties:
                    all_parties[party.upper()] = 0
                all_parties[party.upper()] += votes
                
                if party.upper() == 'DEMOCRAT':
                    dem_candidate = candidate
                    dem_votes += votes
                elif party.upper() == 'REPUBLICAN':
                    rep_candidate = candidate
                    rep_votes += votes
            
            # Calculate totals and margins
            total_votes = sum(all_parties.values())
            two_party_total = dem_votes + rep_votes
            other_votes = total_votes - two_party_total
            
            # Determine winner first
            winner_party = 'REPUBLICAN' if rep_votes > dem_votes else 'DEMOCRAT'
            winner_name = rep_candidate if rep_votes > dem_votes else dem_candidate
            winner_votes = max(rep_votes, dem_votes)
            
            # Margin of victory (winner's votes - loser's votes)
            margin = rep_votes - dem_votes if winner_party == 'REPUBLICAN' else dem_votes - rep_votes
            
            if two_party_total > 0:
                margin_pct = (margin / two_party_total) * 100
                margin_str = f"{'R' if winner_party == 'REPUBLICAN' else 'D'}+{margin_pct:.2f}"
            else:
                margin_str = "N/A"
            
            # Determine competitiveness based on margin percentage
            if two_party_total > 0:
                margin_pct_value = (margin / two_party_total) * 100
                
                if margin_pct_value >= 40:
                    comp_category = "Annihilation"
                    color = "#67000d" if winner_party == "REPUBLICAN" else "#08306b"
                    code = f"{winner_party}_ANNIHILATION"
                elif margin_pct_value >= 30:
                    comp_category = "Dominant"
                    color = "#a50f15" if winner_party == "REPUBLICAN" else "#08519c"
                    code = f"{winner_party}_DOMINANT"
                elif margin_pct_value >= 20:
                    comp_category = "Stronghold"
                    color = "#cb181d" if winner_party == "REPUBLICAN" else "#3182bd"
                    code = f"{winner_party}_STRONGHOLD"
                elif margin_pct_value >= 10:
                    comp_category = "Safe"
                    color = "#ef3b2c" if winner_party == "REPUBLICAN" else "#6baed6"
                    code = f"{winner_party}_SAFE"
                elif margin_pct_value >= 5.5:
                    comp_category = "Likely"
                    color = "#fb6a4a" if winner_party == "REPUBLICAN" else "#9ecae1"
                    code = f"{winner_party}_LIKELY"
                elif margin_pct_value >= 1.0:
                    comp_category = "Lean"
                    color = "#fcae91" if winner_party == "REPUBLICAN" else "#c6dbef"
                    code = f"{winner_party}_LEAN"
                elif margin_pct_value >= 0.5:
                    comp_category = "Tilt"
                    color = "#fee8c8" if winner_party == "REPUBLICAN" else "#e1f5fe"
                    code = f"{winner_party}_TILT"
                else:
                    comp_category = "Tossup"
                    color = "#f7f7f7"
                    code = "TOSSUP"
            else:
                comp_category = "Unknown"
                color = "#cccccc"
                code = "UNKNOWN"
            
            # Build county result
            county_result = {
                'dem_candidate': dem_candidate,
                'rep_candidate': rep_candidate,
                'dem_votes': dem_votes,
                'rep_votes': rep_votes,
                'other_votes': other_votes,
                'total_votes': total_votes,
                'two_party_total': two_party_total,
                'margin': margin,
                'margin_pct': margin_str,
                'winner': winner_party,
                'winner_name': winner_name,
                'winner_party': winner_party,
                'winner_incumbent': False,
                'winner_votes': winner_votes,
                'competitiveness': {
                    'category': comp_category,
                    'party': winner_party if comp_category != 'Tossup' else None,
                    'code': code,
                    'color': color
                },
                'all_parties': all_parties,
                'candidates': candidates,
                'contest': 'U.S. Senate Runoff',
                'county': county,
                'year': '2022'
            }
            
            results['results_by_year']['2022'][contest_key]['results'][county] = county_result

print(f"\nProcessed {len(results['results_by_year']['2022'])} total contests for 2022")

# Save updated results
print(f"\nSaving to {output_path}...")
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print("✓ Done!")

# Print summary
for contest_key in sorted(results['results_by_year']['2022'].keys()):
    count = len(results['results_by_year']['2022'][contest_key]['results'])
    print(f"  {contest_key}: {count} counties")
