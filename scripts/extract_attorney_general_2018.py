import csv
import json
from collections import defaultdict

# Input CSV and output JSON paths
import glob
csv_files = glob.glob('data/2018/20181106__ga__general__*_precinct.csv')
out_json_path = 'data/ga_attorney_general_2018_by_county.json'

# Set correct candidate names
REP_CANDIDATE = 'Chris Carr'
DEM_CANDIDATE = None  # Will be filled from data

# Aggregate results by county
results_by_county = defaultdict(lambda: {'dem_votes': 0, 'rep_votes': 0, 'other_votes': 0, 'total_votes': 0, 'all_parties': {}})

for csv_path in csv_files:
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row.get('office','').strip().lower() != 'attorney general':
                continue
            county = row.get('county', 'UNKNOWN').strip().upper()
            party = row.get('party', '').strip().upper()
            candidate = row.get('candidate', '').strip()
            votes = int(row.get('votes', 0))
            # Set Democratic candidate name if not already
            if party == 'DEM' or party == 'DEMOCRAT':
                if not DEM_CANDIDATE:
                    DEM_CANDIDATE = candidate
                results_by_county[county]['dem_votes'] += votes
                results_by_county[county]['all_parties']['DEM'] = results_by_county[county]['all_parties'].get('DEM', 0) + votes
            elif party == 'REP' or party == 'REPUBLICAN' or party == '(REP':
                results_by_county[county]['rep_votes'] += votes
                results_by_county[county]['all_parties']['REP'] = results_by_county[county]['all_parties'].get('REP', 0) + votes
            else:
                results_by_county[county]['other_votes'] += votes
                if party:
                    results_by_county[county]['all_parties'][party] = results_by_county[county]['all_parties'].get(party, 0) + votes
            results_by_county[county]['total_votes'] += votes

# Build output JSON structure
output = {'results_by_year': {'2018': {'attorney_general_2018': {'results': {}}}}}
for county, data in results_by_county.items():
    dem = data['dem_votes']
    rep = data['rep_votes']
    other = data['other_votes']
    total = data['total_votes']
    margin = abs(dem - rep)
    margin_pct = (abs(dem - rep) / total * 100) if total else 0
    winner = 'DEM' if dem > rep else ('REP' if rep > dem else 'TIE')
    # Category logic (simple, can be replaced with your full system)
    if margin_pct >= 40:
        category = 'Annihilation ' + ('Democratic' if winner == 'DEM' else 'Republican')
    elif margin_pct >= 30:
        category = 'Dominant ' + ('Democratic' if winner == 'DEM' else 'Republican')
    elif margin_pct >= 20:
        category = 'Stronghold ' + ('Democratic' if winner == 'DEM' else 'Republican')
    elif margin_pct >= 10:
        category = 'Safe ' + ('Democratic' if winner == 'DEM' else 'Republican')
    elif margin_pct >= 5.5:
        category = 'Likely ' + ('Democratic' if winner == 'DEM' else 'Republican')
    elif margin_pct >= 1:
        category = 'Lean ' + ('Democratic' if winner == 'DEM' else 'Republican')
    elif margin_pct >= 0.5:
        category = 'Tilt ' + ('Democratic' if winner == 'DEM' else 'Republican')
    else:
        category = 'Tossup'
    output['results_by_year']['2018']['attorney_general_2018']['results'][county] = {
        'county': county,
        'year': 2018,
        'contest_name': 'Attorney General',
        'dem_votes': dem,
        'rep_votes': rep,
        'other_votes': other,
        'total_votes': total,
        'all_parties': data['all_parties'],
        'dem_candidate': DEM_CANDIDATE or 'Democratic',
        'rep_candidate': REP_CANDIDATE,
        'competitiveness': 'HIGH' if margin_pct < 10 else 'LOW',
        'margin': margin,
        'margin_pct': round(margin_pct, 2),
        'winner': winner,
        'category': category,
        'two_party_total': dem + rep
    }

with open(out_json_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2)

print(f"Wrote 2018 Attorney General results to {out_json_path}")
