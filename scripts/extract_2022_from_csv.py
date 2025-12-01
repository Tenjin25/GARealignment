import csv
import json
import os

print("Loading 2022 precinct data...")
with open('data/20221108__ga__general__precinct.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Clean up column names
cleaned_rows = []
for row in rows:
    cleaned = {}
    for k, v in row.items():
        key = k.strip() if k else 'unknown'
        val = v.strip() if (v and isinstance(v, str)) else (v if v else '')
        cleaned[key] = val
    cleaned_rows.append(cleaned)

rows = cleaned_rows
print(f"Cleaned {len(rows)} rows")
print(f"Sample row keys: {list(rows[0].keys())}")

# Load current election data
with open('data/results_by_year_grouped.final.json', 'r', encoding='utf-8') as f:
    election_data = json.load(f)

# Target contests to extract
target_contests = {
    'Commissioner of Agriculture': 'commissioner_of_agriculture_2022',
    'Commissioner of Insurance': 'commissioner_of_insurance_2022',
    'Commissioner of Labor': 'commissioner_of_labor_2022',
}

# Note: State School Superintendent is missing from the CSV entirely

def normalize_county(name):
    """Normalize county names to match our data format"""
    return name.strip()

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

# Process each contest
for office_name, contest_key in target_contests.items():
    print(f"\nProcessing {office_name}...")
    
    # Filter rows for this office
    office_rows = [r for r in rows if r.get('office') == office_name]
    print(f"  Found {len(office_rows)} rows for this office")
    
    if len(office_rows) > 0:
        print(f"  Sample row: {office_rows[0]}")
    
    # Group by county
    county_data = {}
    for row in office_rows:
        county = normalize_county(row.get('county', ''))
        if not county:
            continue
        
        if county not in county_data:
            county_data[county] = {}
        
        candidate = row.get('candidate', '').strip()
        party = row.get('party', '').strip()
        
        # Calculate total votes - handle malformed data
        try:
            election_day = int(row.get('election_day_votes', 0) or 0)
            advanced = int(row.get('advanced_votes', 0) or 0)
            absentee = int(row.get('absentee_by_mail_votes', 0) or 0)
            provisional = int(row.get('provisional_votes', 0) or 0)
            total_votes = election_day + advanced + absentee + provisional
        except (ValueError, TypeError) as e:
            # Skip malformed rows
            print(f"    Skipping malformed row: {e}")
            continue
        
        if party not in county_data[county]:
            county_data[county][party] = {
                'candidate': candidate,
                'votes': 0
            }
        
        county_data[county][party]['votes'] += total_votes
    
    print(f"  Aggregated data for {len(county_data)} counties")
    
    # Build contest results
    contest_results = {
        'contest_name': office_name,
        'results': {}
    }
    
    counties_processed = 0
    counties_skipped = 0
    
    for county, parties in county_data.items():
        dem_data = parties.get('DEM', {'candidate': '', 'votes': 0})
        rep_data = parties.get('REP', {'candidate': '', 'votes': 0})
        lib_data = parties.get('LIB', {'candidate': '', 'votes': 0})
        
        # Also check for 'Democratic' and 'Republican' party names
        if not dem_data['votes']:
            dem_data = parties.get('Democratic', {'candidate': '', 'votes': 0})
        if not rep_data['votes']:
            rep_data = parties.get('Republican', {'candidate': '', 'votes': 0})
        
        dem_candidate = dem_data['candidate']
        rep_candidate = rep_data['candidate']
        dem_votes = dem_data['votes']
        rep_votes = rep_data['votes']
        other_votes = lib_data['votes']  # Libertarian as "other"
        
        total_votes = dem_votes + rep_votes + other_votes
        
        if total_votes == 0:
            counties_skipped += 1
            continue
        
        counties_processed += 1
        
        # Calculate percentages
        dem_pct = (dem_votes / total_votes * 100) if total_votes > 0 else 0
        rep_pct = (rep_votes / total_votes * 100) if total_votes > 0 else 0
        
        # Calculate margin
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
        
        competitiveness = calculate_competitiveness(margin_pct, winner)
        
        contest_results['results'][county] = {
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
            'winner_incumbent': False,
            'competitiveness': competitiveness
        }
    
    print(f"  Processed {counties_processed} counties, skipped {counties_skipped} (no votes)")
    print(f"  Extracted {len(contest_results['results'])} counties")
    
    # Add to election data
    if '2022' not in election_data['results_by_year']:
        election_data['results_by_year']['2022'] = {}
    
    election_data['results_by_year']['2022'][contest_key] = contest_results

# Create backup
backup_path = 'data/results_by_year_grouped.final.backup_before_2022_addition.json'
if not os.path.exists(backup_path):
    with open('data/results_by_year_grouped.final.json', 'r', encoding='utf-8') as f:
        backup_data = json.load(f)
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, indent=2)
    print(f"\nBackup created: {backup_path}")

# Save updated data
with open('data/results_by_year_grouped.final.json', 'w', encoding='utf-8') as f:
    json.dump(election_data, f, indent=2)

print("\n[SUCCESS] Successfully added 2022 contests to data/results_by_year_grouped.final.json")
print("\nAll 2022 contests now:")
for key in sorted(election_data['results_by_year']['2022'].keys()):
    count = len(election_data['results_by_year']['2022'][key]['results'])
    print(f"  - {key}: {count} counties")

print("\n[NOTE] CSV data only includes ~116 counties for the new contests.")
print("   The remaining counties may not have had those races on their ballots,")
print("   or the data is missing from the OpenElections CSV file.")
