import csv
import json
from collections import defaultdict

# Input CSV and output JSON paths for 2022 runoff
csv_path = 'data/cleaned/20221206__ga__general_runoff__precinct.csv'
json_path = 'data/cleaned/20221206__ga__general_runoff_aggregated.json'

# Define mapping for the 2022 Senate runoff
senate_race = {
    'office': 'U.S. Senate',
    'dem_candidate': 'Raphael Warnock',
    'rep_candidate': 'Herschel Walker',
    'json_key': 'us_senate_2022_warnock',
    'contest_name': 'U.S. Senate Runoff (Warnock vs. Walker)',
    'year': 2022
}

data = defaultdict(lambda: defaultdict(int))

with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    reader.fieldnames = [f.strip() for f in reader.fieldnames]
    for row in reader:
        row = {k.strip(): v for k, v in row.items()}
        office = row['office'].strip()
        candidate = row['candidate'].strip()
        county = row['county'].strip().upper()
        party = row['party'].strip()
        # Only sum vote columns if they are numeric, skip if not
        vote_cols = ['election_day_votes', 'advanced_votes', 'absentee_by_mail_votes', 'provisional_votes']
        total_votes = 0
        for col in vote_cols:
            val = row.get(col, '').strip()
            try:
                total_votes += int(val)
            except (ValueError, TypeError):
                # If not numeric, skip (could be a header or bad row)
                continue

        if office == senate_race['office'] and candidate in [senate_race['dem_candidate'], senate_race['rep_candidate']]:
            cand_key = 'dem_votes' if candidate == senate_race['dem_candidate'] else 'rep_votes'
            data[county][cand_key] += total_votes
            data[county]['county'] = county
            data[county]['year'] = senate_race['year']
            data[county]['contest_name'] = senate_race['contest_name']
            data[county]['dem_candidate'] = senate_race['dem_candidate']
            data[county]['rep_candidate'] = senate_race['rep_candidate']

# Post-process: add totals, margins, categories, etc.
for county, result in data.items():
    dem = result.get('dem_votes', 0)
    rep = result.get('rep_votes', 0)
    result['total_votes'] = dem + rep
    result['other_votes'] = 0
    result['margin'] = dem - rep
    result['margin_pct'] = round(100 * (dem - rep) / (dem + rep), 2) if (dem + rep) else 0
    result['winner'] = 'DEM' if dem > rep else 'REP'
    result['office'] = senate_race['office']
    result['dem_party'] = 'DEM'
    result['rep_party'] = 'REP'
    result['two_party_total'] = dem + rep
    result['all_parties'] = {'DEM': dem, 'REP': rep}
    margin_pct = abs(result['margin_pct'])
    winner = result['winner']
    # Assign competitiveness (for reference)
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
    senate_race['json_key']: {
        'results': data,
        'contest_name': senate_race['contest_name']
    }
}

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2)

print(f'Aggregated results written to {json_path}')
