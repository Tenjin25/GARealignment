import csv
import json
from collections import defaultdict

# Input CSV and output JSON paths
csv_path = 'data/cleaned/20210105__ga__runoff.csv'
json_path = 'data/cleaned/20210105__ga__runoff_aggregated.json'

# Define mapping for the two Senate runoffs
senate_races = {
    'Warnock': {
        'office': 'United States Senate',
        'candidate': 'Raphael Warnock',
        'opponent': 'Kelly Loeffler',
        'opponent_party': 'Republican',
        'json_key': 'us_senate_2021_warnock',
    },
    'Ossoff': {
        'office': 'United States Senate',
        'candidate': 'Jon Ossoff',
        'opponent': 'David Perdue',
        'opponent_party': 'Republican',
        'json_key': 'us_senate_2021_ossoff',
    }
}

# Prepare aggregation structure
data = {race['json_key']: defaultdict(lambda: defaultdict(int)) for race in senate_races.values()}


with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    # Strip whitespace from fieldnames
    reader.fieldnames = [f.strip() for f in reader.fieldnames]
    for row in reader:
        # Also strip whitespace from keys in each row
        row = {k.strip(): v for k, v in row.items()}
        office = row['office'].strip()
        candidate = row['candidate'].strip()
        county = row['county'].strip().upper()
        party = row['party'].strip()
        total_votes = sum(int(row[col]) for col in ['election_day_votes', 'advanced_votes', 'absentee_by_mail_votes', 'provisional_votes'])

        # Warnock vs Loeffler (Special Election)
        if office == 'U.S. Senate (Special)' and candidate in ['Raphael Warnock', 'Kelly Loeffler']:
            key = 'us_senate_2021_warnock'
            cand_key = 'dem_votes' if candidate == 'Raphael Warnock' else 'rep_votes'
            data[key][county][cand_key] += total_votes
            data[key][county]['county'] = county
            data[key][county]['year'] = 2021
            data[key][county]['contest_name'] = 'U.S. Senate Runoff (Warnock vs. Loeffler)'
            data[key][county]['dem_candidate'] = 'Raphael Warnock'
            data[key][county]['rep_candidate'] = 'Kelly Loeffler'
        # Ossoff vs Perdue
        elif office == 'U.S. Senate' and candidate in ['Jon Ossoff', 'David A. Perdue']:
            key = 'us_senate_2021_ossoff'
            cand_key = 'dem_votes' if candidate == 'Jon Ossoff' else 'rep_votes'
            data[key][county][cand_key] += total_votes
            data[key][county]['county'] = county
            data[key][county]['year'] = 2021
            data[key][county]['contest_name'] = 'U.S. Senate Runoff (Ossoff vs. Perdue)'
            data[key][county]['dem_candidate'] = 'Jon Ossoff'
            data[key][county]['rep_candidate'] = 'David A. Perdue'

# Post-process: add totals, margins, etc.
for key, counties in data.items():
    for county, result in counties.items():
        dem = result.get('dem_votes', 0)
        rep = result.get('rep_votes', 0)
        result['total_votes'] = dem + rep
        result['other_votes'] = 0
        result['margin'] = dem - rep
        result['margin_pct'] = round(100 * (dem - rep) / (dem + rep), 2) if (dem + rep) else 0
        result['winner'] = 'DEM' if dem > rep else 'REP'
        result['office'] = 'U.S. Senate'
        # Set party for each candidate
        result['dem_party'] = 'DEM'
        result['rep_party'] = 'REP'
        result['two_party_total'] = dem + rep
        # Add all_parties field
        result['all_parties'] = {
            'DEM': dem,
            'REP': rep
        }
        # Add competitiveness and category fields using legend breakpoints
        margin_pct = abs(result['margin_pct'])
        winner = result['winner']
        # Assign competitiveness (for reference, not used in legend)
        if margin_pct <= 0.5:
            result['competitiveness'] = 'HIGH'
        elif margin_pct <= 5.5:
            result['competitiveness'] = 'MEDIUM'
        else:
            result['competitiveness'] = 'LOW'

        # Assign category based on winner and margin
        if margin_pct <= 0.5:
            result['category'] = 'Tossup'
        elif margin_pct <= 1:
            result['category'] = 'Tilt Democratic' if winner == 'DEM' else 'Tilt Republican'
        elif margin_pct <= 5.5:
            result['category'] = 'Lean Democratic' if winner == 'DEM' else 'Lean Republican'
        elif margin_pct <= 10:
            result['category'] = 'Likely Democratic' if winner == 'DEM' else 'Likely Republican'
        elif margin_pct <= 20:
            result['category'] = 'Safe Democratic' if winner == 'DEM' else 'Safe Republican'
        elif margin_pct <= 30:
            result['category'] = 'Stronghold Democratic' if winner == 'DEM' else 'Stronghold Republican'
        elif margin_pct <= 40:
            result['category'] = 'Dominant Democratic' if winner == 'DEM' else 'Dominant Republican'
        else:
            result['category'] = 'Annihilation Democratic' if winner == 'DEM' else 'Annihilation Republican'

# Output structure for JSON
output = {
    'us_senate_2021_warnock': {'results': data['us_senate_2021_warnock'], 'contest_name': 'U.S. Senate Runoff (Warnock vs. Loeffler)'},
    'us_senate_2021_ossoff': {'results': data['us_senate_2021_ossoff'], 'contest_name': 'U.S. Senate Runoff (Ossoff vs. Perdue)'}
}

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2)

print(f'Aggregated results written to {json_path}')
