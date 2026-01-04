"""
Fill missing 2022 county data from the election_data_GA.v04-aligned.csv file
into the results_by_year_grouped JSON structure
"""

import json
import csv
import os

# File paths
CSV_PATH = r"c:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data_files\Election_Data_GA.v04\election_data_GA.v04-aligned.csv"
JSON_PATH = r"c:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data\results_by_year_grouped.json"
OUTPUT_PATH = r"c:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data\results_by_year_grouped.filled_2022.json"

# Mapping from CSV columns to contest names
CSV_TO_CONTEST = {
    'E_22_GOV': 'governor_2022',
    'E_22_LTG': 'lieutenant_governor_2022',
    'E_22_SOS': 'secretary_of_state_2022',
    'E_22_AG': 'attorney_general_2022',
    'E_22_SEN': 'us_senate_2022',
}

# Contest display names
CONTEST_DISPLAY_NAMES = {
    'governor_2022': 'Governor',
    'lieutenant_governor_2022': 'Lieutenant Governor',
    'secretary_of_state_2022': 'Secretary of State',
    'attorney_general_2022': 'Attorney General',
    'us_senate_2022': 'U.S. Senate',
}

# Known candidates for 2022
CANDIDATES_2022 = {
    'governor_2022': {
        'dem': {'name': 'Stacey Abrams', 'incumbent': False},
        'rep': {'name': 'Brian Kemp', 'incumbent': True}
    },
    'lieutenant_governor_2022': {
        'dem': {'name': 'Charlie Bailey', 'incumbent': False},
        'rep': {'name': 'Burt Jones', 'incumbent': False}
    },
    'secretary_of_state_2022': {
        'dem': {'name': 'Bee Nguyen', 'incumbent': False},
        'rep': {'name': 'Brad Raffensperger', 'incumbent': True}
    },
    'attorney_general_2022': {
        'dem': {'name': 'Jen Jordan', 'incumbent': False},
        'rep': {'name': 'Chris Carr', 'incumbent': True}
    },
    'us_senate_2022': {
        'dem': {'name': 'Raphael Warnock', 'incumbent': True},
        'rep': {'name': 'Herschel Walker', 'incumbent': False}
    }
}

def normalize_county_name(name):
    """Normalize county name for matching"""
    # Remove common prefixes/suffixes and clean up
    name = name.upper().strip()
    # Remove GEOID prefix patterns
    name = name.split(',')[-1].strip() if ',' in name else name
    # Handle special cases
    name = name.replace(' COUNTY', '')
    return name.title()

def calculate_competitiveness(margin_pct_value, winner_party):
    """Calculate competitiveness category based on margin"""
    margin = abs(margin_pct_value)
    
    if margin >= 30:
        category = "Dominant"
        code = f"{winner_party}_DOMINANT"
        color = "#a50f15" if winner_party == "REPUBLICAN" else "#08519c"
    elif margin >= 20:
        category = "Safe"
        code = f"{winner_party}_SAFE"
        color = "#ef3b2c" if winner_party == "REPUBLICAN" else "#3182bd"
    elif margin >= 10:
        category = "Likely"
        code = f"{winner_party}_LIKELY"
        color = "#fc9272" if winner_party == "REPUBLICAN" else "#6baed6"
    elif margin >= 5:
        category = "Lean"
        code = f"{winner_party}_LEAN"
        color = "#fcbba1" if winner_party == "REPUBLICAN" else "#9ecae1"
    else:
        category = "Toss-up"
        code = "TOSSUP"
        color = "#fee5d9" if winner_party == "REPUBLICAN" else "#c6dbef"
    
    return {
        "category": category,
        "party": winner_party,
        "code": code,
        "color": color
    }

def create_county_result(county_name, contest_key, dem_votes, rep_votes):
    """Create a county result entry in the proper format"""
    total_votes = dem_votes + rep_votes
    two_party_total = total_votes  # For now, assuming only dem/rep
    margin = abs(rep_votes - dem_votes)
    margin_pct_value = (margin / two_party_total * 100) if two_party_total > 0 else 0
    
    winner = "REPUBLICAN" if rep_votes > dem_votes else "DEMOCRAT"
    winner_votes = max(rep_votes, dem_votes)
    
    # Get candidate info
    candidates_info = CANDIDATES_2022.get(contest_key, {})
    dem_candidate = candidates_info.get('dem', {}).get('name', 'Unknown')
    rep_candidate = candidates_info.get('rep', {}).get('name', 'Unknown')
    dem_incumbent = candidates_info.get('dem', {}).get('incumbent', False)
    rep_incumbent = candidates_info.get('rep', {}).get('incumbent', False)
    
    winner_name = rep_candidate if winner == "REPUBLICAN" else dem_candidate
    winner_incumbent = rep_incumbent if winner == "REPUBLICAN" else dem_incumbent
    
    margin_pct = f"{winner[0]}+{margin_pct_value:.2f}"
    
    competitiveness = calculate_competitiveness(margin_pct_value, winner)
    
    result = {
        "dem_candidate": dem_candidate,
        "rep_candidate": rep_candidate,
        "dem_votes": dem_votes,
        "rep_votes": rep_votes,
        "other_votes": 0,
        "total_votes": total_votes,
        "two_party_total": two_party_total,
        "margin": margin,
        "margin_pct": margin_pct,
        "winner": winner,
        "winner_name": winner_name,
        "winner_party": winner,
        "winner_incumbent": winner_incumbent,
        "winner_votes": winner_votes,
        "competitiveness": competitiveness,
        "all_parties": {
            "DEMOCRAT": dem_votes,
            "REPUBLICAN": rep_votes
        },
        "candidates": {
            dem_candidate: {
                "votes": dem_votes,
                "party": "DEMOCRAT",
                "incumbent": dem_incumbent
            },
            rep_candidate: {
                "votes": rep_votes,
                "party": "REPUBLICAN",
                "incumbent": rep_incumbent
            }
        },
        "contest": CONTEST_DISPLAY_NAMES.get(contest_key, contest_key),
        "county": county_name,
        "year": "2022"
    }
    
    return result

def main():
    print("Loading JSON data...")
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Ensure 2022 year exists
    if '2022' not in data['results_by_year']:
        data['results_by_year']['2022'] = {}
    
    # Ensure all contests exist
    for contest_key in CSV_TO_CONTEST.values():
        if contest_key not in data['results_by_year']['2022']:
            data['results_by_year']['2022'][contest_key] = {'results': {}}
        elif 'results' not in data['results_by_year']['2022'][contest_key]:
            data['results_by_year']['2022'][contest_key]['results'] = {}
    
    print("Reading CSV data...")
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        # Clean up header - remove extra spaces
        reader.fieldnames = [name.strip() for name in reader.fieldnames]
        
        rows_processed = 0
        for row in reader:
            # Get county name from the 'Name' column
            county_raw = row.get('Name', '').strip()
            if not county_raw:
                continue
            
            county_name = normalize_county_name(county_raw)
            
            # Process each contest
            for csv_prefix, contest_key in CSV_TO_CONTEST.items():
                try:
                    # Get the column names
                    total_col = f'{csv_prefix}_Total'
                    dem_col = f'{csv_prefix}_Dem'
                    rep_col = f'{csv_prefix}_Rep'
                    
                    # Check if data exists
                    if total_col not in row or not row[total_col].strip():
                        continue
                    
                    total = int(row[total_col].strip())
                    if total == 0:
                        continue
                    
                    dem_votes = int(row[dem_col].strip()) if row[dem_col].strip() else 0
                    rep_votes = int(row[rep_col].strip()) if row[rep_col].strip() else 0
                    
                    # Check if county already exists (don't overwrite)
                    existing = data['results_by_year']['2022'][contest_key]['results'].get(county_name)
                    if existing:
                        # Skip if already has data
                        continue
                    
                    # Create the result entry
                    result = create_county_result(county_name, contest_key, dem_votes, rep_votes)
                    
                    # Add to data
                    data['results_by_year']['2022'][contest_key]['results'][county_name] = result
                    rows_processed += 1
                    
                except (KeyError, ValueError) as e:
                    print(f"Error processing {county_name} for {contest_key}: {e}")
                    continue
    
    print(f"Processed {rows_processed} county-contest entries")
    
    # Write output
    print(f"Writing to {OUTPUT_PATH}...")
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("Done!")
    
    # Print summary
    print("\nSummary of 2022 contests:")
    for contest_key in CSV_TO_CONTEST.values():
        county_count = len(data['results_by_year']['2022'][contest_key]['results'])
        print(f"  {contest_key}: {county_count} counties")

if __name__ == '__main__':
    main()
