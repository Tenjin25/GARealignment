#!/usr/bin/env python3
"""
Aggregate precinct CSV to county level and add 2022 data to results_by_year_grouped.json
with full candidate names and structure matching existing years.
"""
import csv
import json
import os
from collections import defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CSV_PATH = os.path.join(ROOT, 'data_files', 'Election_Data_GA.v04', 'election_data_GA.v04-aligned.csv')
JSON_PATH = os.path.join(ROOT, 'data', 'results_by_year_grouped.json')
GEOJSON_PATH = os.path.join(ROOT, 'tl_2020_13_county20.geojson')
OUT_PATH = os.path.join(ROOT, 'data', 'results_by_year_grouped.updated2022.json')

# 2022 candidate names by race
CANDIDATES_2022 = {
    'GOV': {'dem': 'Stacey Abrams', 'rep': 'Brian Kemp'},
    'SEN': {'dem': 'Raphael Warnock', 'rep': 'Herschel Walker'},
    'LTG': {'dem': 'Charlie Bailey', 'rep': 'Burt Jones'},
    'SOS': {'dem': 'Bee Nguyen', 'rep': 'Brad Raffensperger'},
    'AG': {'dem': 'Jen Jordan', 'rep': 'Chris Carr'},
}

# Contest name mapping from CSV prefix to JSON contest name
CONTEST_MAP = {
    'GOV': 'governor_2022',
    'SEN': 'us_senate_2022',
    'LTG': 'lieutenant_governor_2022',
    'SOS': 'secretary_of_state_2022',
    'AG': 'attorney_general_2022',
}

CONTEST_DISPLAY = {
    'GOV': 'Governor',
    'SEN': 'U.S. Senate',
    'LTG': 'Lieutenant Governor',
    'SOS': 'Secretary of State',
    'AG': 'Attorney General',
}

def calculate_competitiveness(margin_pct, winner_party):
    """Calculate competitiveness category based on margin using your 7-tier system"""
    margin = abs(margin_pct)
    
    if margin >= 40:
        category = "Annihilation"
        code = f"{winner_party}_ANNIHILATION"
        color = "#67000d" if winner_party == "REPUBLICAN" else "#08306b"
    elif margin >= 30:
        category = "Dominant"
        code = f"{winner_party}_DOMINANT"
        color = "#a50f15" if winner_party == "REPUBLICAN" else "#08519c"
    elif margin >= 20:
        category = "Stronghold"
        code = f"{winner_party}_STRONGHOLD"
        color = "#cb181d" if winner_party == "REPUBLICAN" else "#3182bd"
    elif margin >= 10:
        category = "Safe"
        code = f"{winner_party}_SAFE"
        color = "#ef3b2c" if winner_party == "REPUBLICAN" else "#6baed6"
    elif margin >= 5.5:
        category = "Likely"
        code = f"{winner_party}_LIKELY"
        color = "#fb6a4a" if winner_party == "REPUBLICAN" else "#9ecae1"
    elif margin >= 1:
        category = "Lean"
        code = f"{winner_party}_LEAN"
        color = "#fcae91" if winner_party == "REPUBLICAN" else "#c6dbef"
    elif margin >= 0.5:
        category = "Tilt"
        code = f"{winner_party}_TILT"
        color = "#fee8c8" if winner_party == "REPUBLICAN" else "#e1f5fe"
        party = winner_party
    else:
        category = "Tossup"
        code = "TOSSUP"
        color = "#f7f7f7"
        party = "TOSSUP"  # Neutral for true tossups
    
    return {
        "category": category,
        "party": party,
        "code": code,
        "color": color
    }

print('Loading county GeoJSON...')
with open(GEOJSON_PATH, 'r', encoding='utf-8') as f:
    geojson = json.load(f)

county_names = {}
county_names_lower = {}
for feature in geojson['features']:
    props = feature['properties']
    geoid = props.get('GEOID20')
    name = props.get('NAME20')
    if geoid and name:
        county_names[geoid] = name
        county_names_lower[geoid] = name.lower()

print(f'Loaded {len(county_names)} counties from GeoJSON')

print('Reading CSV and aggregating by county...')
with open(CSV_PATH, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = [{k.strip(): v for k, v in r.items() if k} for r in reader]

# Aggregate by county (first 5 digits of GEOID20)
county_data = defaultdict(lambda: defaultdict(int))

for row in rows:
    geoid = row.get('GEOID20', '')
    if len(geoid) < 5:
        continue
    
    county_geoid = geoid[:5]
    
    # Aggregate all numeric columns with '22' in them
    for col, value in row.items():
        if '22' in col or '16-22' in col:
            try:
                county_data[county_geoid][col] += int(value)
            except (ValueError, TypeError):
                pass

print(f'Aggregated data for {len(county_data)} counties')

# Load existing JSON
print('Loading existing results JSON...')
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Build 2022 contest results - replace any existing data
data['results_by_year']['2022'] = {}

for race_code, contest_name in CONTEST_MAP.items():
    data['results_by_year']['2022'][contest_name] = {'results': {}}
    
    results = data['results_by_year']['2022'][contest_name]['results']
    
    dem_col = f'E_22_{race_code}_Dem'
    rep_col = f'E_22_{race_code}_Rep'
    total_col = f'E_22_{race_code}_Total'
    
    for county_geoid, aggregated in county_data.items():
        county_name = county_names.get(county_geoid, 'Unknown')
        if county_name == 'Unknown':
            continue
        
        dem_votes = aggregated.get(dem_col, 0)
        rep_votes = aggregated.get(rep_col, 0)
        total_votes = aggregated.get(total_col, 0)
        other_votes = max(0, total_votes - dem_votes - rep_votes)
        two_party_total = dem_votes + rep_votes
        
        if two_party_total == 0:
            continue
        
        margin = abs(rep_votes - dem_votes)
        margin_pct = (margin / two_party_total * 100) if two_party_total > 0 else 0
        
        winner_party = "REPUBLICAN" if rep_votes > dem_votes else "DEMOCRAT"
        winner_votes = max(rep_votes, dem_votes)
        winner_name = CANDIDATES_2022[race_code]['rep'] if winner_party == "REPUBLICAN" else CANDIDATES_2022[race_code]['dem']
        
        margin_str = f"{winner_party[0]}+{margin_pct:.2f}"
        
        competitiveness = calculate_competitiveness(margin_pct, winner_party)
        
        county_result = {
            "dem_candidate": CANDIDATES_2022[race_code]['dem'],
            "rep_candidate": CANDIDATES_2022[race_code]['rep'],
            "dem_votes": dem_votes,
            "rep_votes": rep_votes,
            "other_votes": other_votes,
            "total_votes": total_votes,
            "two_party_total": two_party_total,
            "margin": margin,
            "margin_pct": margin_str,
            "winner": winner_party,
            "winner_name": winner_name,
            "winner_party": winner_party,
            "winner_incumbent": False,
            "winner_votes": winner_votes,
            "competitiveness": competitiveness,
            "all_parties": {
                "DEMOCRAT": dem_votes,
                "REPUBLICAN": rep_votes
            },
            "candidates": {
                CANDIDATES_2022[race_code]['dem']: {
                    "votes": dem_votes,
                    "party": "DEMOCRAT",
                    "incumbent": False
                },
                CANDIDATES_2022[race_code]['rep']: {
                    "votes": rep_votes,
                    "party": "REPUBLICAN",
                    "incumbent": False
                }
            },
            "contest": CONTEST_DISPLAY[race_code],
            "county": county_name,
            "year": "2022"
        }
        
        results[county_name] = county_result

# Write output
print(f'Writing updated JSON to {OUT_PATH}...')
with open(OUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print('\nDone!')
print(f'Updated 2022 contests:')
for race_code, contest_name in CONTEST_MAP.items():
    count = len(data['results_by_year']['2022'][contest_name]['results'])
    print(f'  {CONTEST_DISPLAY[race_code]}: {count} counties')
