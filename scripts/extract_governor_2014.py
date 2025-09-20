import csv
import json
import re

# Input and output paths
csv_path = 'data/20141104__ga__general.csv'
out_json_path = 'data/ga_governor_2014_by_county.json'

def parse_int(val):
    try:
        return int(val.replace(',', '').strip())
    except Exception:
        return 0

governor_results = {}
with open(csv_path, encoding='utf-8') as f:
    for line in f:
        # Only process lines for Governor
        if ', Governor' not in line:
            continue
        # Split by comma, but handle ragged spacing
        parts = [p.strip() for p in re.split(r',\s*', line)]
        if len(parts) < 10:
            continue
        county = parts[0].upper()
        office = parts[1].strip()
        party = parts[3].strip().upper()
        candidate = parts[4].strip()
        total_votes = parse_int(parts[5])
        # Normalize party
        if party in ['IR', 'R', 'REP', 'REPUBLICAN']:
            party_key = 'REP'
        elif party in ['D', 'DEM', 'DEMOCRAT']:
            party_key = 'DEM'
        else:
            party_key = party
        if county not in governor_results:
            governor_results[county] = {'rep_votes': 0, 'dem_votes': 0, 'other_votes': 0, 'total_votes': 0, 'all_parties': {}}
        # Assign votes by party
        if party_key == 'REP':
            governor_results[county]['rep_votes'] += total_votes
            governor_results[county]['all_parties']['REP'] = governor_results[county]['all_parties'].get('REP', 0) + total_votes
        elif party_key == 'DEM':
            governor_results[county]['dem_votes'] += total_votes
            governor_results[county]['all_parties']['DEM'] = governor_results[county]['all_parties'].get('DEM', 0) + total_votes
        else:
            governor_results[county]['other_votes'] += total_votes
            if party_key:
                governor_results[county]['all_parties'][party_key] = governor_results[county]['all_parties'].get(party_key, 0) + total_votes
        governor_results[county]['total_votes'] += total_votes

# Build output JSON structure
output = {'results_by_year': {'2014': {'governor_2014': {'results': {}}}}}
for county, data in governor_results.items():
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
    output['results_by_year']['2014']['governor_2014']['results'][county] = {
        'county': county,
        'year': 2014,
        'contest_name': 'Governor',
        'dem_votes': dem,
        'rep_votes': rep,
        'other_votes': other,
        'total_votes': total,
        'all_parties': data['all_parties'],
        'dem_candidate': 'Democratic',
        'rep_candidate': 'Nathan Deal',
        'competitiveness': 'HIGH' if margin_pct < 10 else 'LOW',
        'margin': margin,
        'margin_pct': round(margin_pct, 2),
        'winner': winner,
        'category': category,
        'two_party_total': dem + rep
    }

with open(out_json_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2)

print(f"Wrote 2014 Governor results to {out_json_path}")
