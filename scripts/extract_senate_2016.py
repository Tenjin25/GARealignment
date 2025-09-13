import csv
import json
from collections import defaultdict

# Input CSV and output JSON paths
csv_path = 'data/cleaned/20161108__ga__general.csv'
json_path = 'data/ga_senate_2016_by_county.json'

# Output structure
senate_results = {}


# Competitiveness scale as per user specification
COMPETITIVENESS_SCALE = [
    # Republican
    (40, 'Annihilation', 'R', '#67000d'),
    (30, 'Dominant', 'R', '#a50f15'),
    (20, 'Stronghold', 'R', '#cb181d'),
    (10, 'Safe', 'R', '#ef3b2c'),
    (5.5, 'Likely', 'R', '#fb6a4a'),
    (1, 'Lean', 'R', '#fcae91'),
    (0.5, 'Tilt', 'R', '#fee8c8'),
    # Tossup
    (0.5, 'Tossup', 'T', '#f7f7f7'),
    # Democratic
    (1, 'Tilt', 'D', '#e1f5fe'),
    (5.5, 'Lean', 'D', '#c6dbef'),
    (10, 'Likely', 'D', '#9ecae1'),
    (20, 'Safe', 'D', '#6baed6'),
    (30, 'Stronghold', 'D', '#3182bd'),
    (40, 'Dominant', 'D', '#08519c'),
    (100, 'Annihilation', 'D', '#08306b'),
]

def get_category(margin_pct, winner_party):
    # margin_pct is always positive
    # winner_party: 'R' or 'D'
    abs_margin = abs(margin_pct)
    if abs_margin <= 0.5:
        return 'Tossup'
    if winner_party == 'R':
        if abs_margin > 40:
            return 'Annihilation'
        elif abs_margin > 30:
            return 'Dominant'
        elif abs_margin > 20:
            return 'Stronghold'
        elif abs_margin > 10:
            return 'Safe'
        elif abs_margin > 5.5:
            return 'Likely'
        elif abs_margin > 1:
            return 'Lean'
        elif abs_margin > 0.5:
            return 'Tilt'
    elif winner_party == 'D':
        if abs_margin > 40:
            return 'Annihilation'
        elif abs_margin > 30:
            return 'Dominant'
        elif abs_margin > 20:
            return 'Stronghold'
        elif abs_margin > 10:
            return 'Safe'
        elif abs_margin > 5.5:
            return 'Likely'
        elif abs_margin > 1:
            return 'Lean'
        elif abs_margin > 0.5:
            return 'Tilt'
    return 'Tossup'

with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        # Only process rows for "United States Senator"
        if len(row) < 8:
            continue
        office = row[1].strip()
        if office != 'United States Senator':
            continue
        county = row[0].strip().upper()
        party = row[3].strip().replace('(', '').replace(')', '')
        candidate = row[4].strip().replace(' (I)', '').replace('(I)', '')
        votes = int(row[5].replace(',', '').strip()) if row[5].strip() else 0
        # Aggregate by county
        if county not in senate_results:
            senate_results[county] = {
                'county': county,
                'year': 2016,
                'contest_name': 'US Senate (2016)',
                'all_parties': {},
                'rep_votes': 0,
                'dem_votes': 0,
                'other_votes': 0,
                'rep_candidate': '',
                'dem_candidate': '',
                'other_candidate': '',
            }
        # Assign votes by party
        if 'REP' in party:
            senate_results[county]['rep_votes'] += votes
            senate_results[county]['rep_candidate'] = candidate
        elif 'DEM' in party:
            senate_results[county]['dem_votes'] += votes
            senate_results[county]['dem_candidate'] = candidate
        else:
            senate_results[county]['other_votes'] += votes
            senate_results[county]['other_candidate'] = candidate
        senate_results[county]['all_parties'][candidate] = votes

# Now calculate margin, margin_pct, winner, category, two_party_total
for county, data in senate_results.items():
    rep = data['rep_votes']
    dem = data['dem_votes']
    other = data['other_votes']
    two_party_total = rep + dem
    total_votes = rep + dem + other
    data['two_party_total'] = two_party_total
    data['total_votes'] = total_votes
    # Determine winner and margin
    if rep > dem:
        winner = data['rep_candidate']
        loser = data['dem_candidate']
        margin = rep - dem
    else:
        winner = data['dem_candidate']
        loser = data['rep_candidate']
        margin = dem - rep
    data['winner'] = winner
    data['margin'] = margin
    data['margin_pct'] = round((margin / two_party_total) * 100, 2) if two_party_total else 0.0
    # Category (Safe/Lean/Likely/Tossup)
    winner_party = 'R' if rep > dem else 'D'
    data['category'] = get_category(data['margin_pct'], winner_party)

# Output as JSON in the map's expected format
output = {
    'results_by_year': {
        '2016': {
            'us_senate_2016': {
                'contest_name': 'US Senate (2016)',
                'results': senate_results
            }
        }
    }
}

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2)

print(f"Wrote {len(senate_results)} counties to {json_path}")
