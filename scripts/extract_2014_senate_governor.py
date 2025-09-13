import csv
import json
from collections import defaultdict

csv_path = 'data/cleaned/20141104__ga__general.csv'
out_path = 'data/ga_2014_senate_governor_by_county.json'

contests = {
    'us_senate_2014': {
        'contest_name': 'US Senate (2014)',
        'results': {}
    },
    'governor_2014': {
        'contest_name': 'Governor (2014)',
        'results': {}
    }
}

# Helper for margin category
CATEGORY_SCALE = [
    (40, 'Annihilation'), (30, 'Dominant'), (20, 'Stronghold'), (10, 'Safe'),
    (5.5, 'Likely'), (1, 'Lean'), (0.5, 'Tilt'), (0, 'Tossup')
]
def get_category(margin_pct, winner_party):
    abs_margin = abs(margin_pct)
    if abs_margin <= 0.5:
        return 'Tossup'
    if winner_party == 'R':
        if abs_margin > 40: return 'Annihilation'
        elif abs_margin > 30: return 'Dominant'
        elif abs_margin > 20: return 'Stronghold'
        elif abs_margin > 10: return 'Safe'
        elif abs_margin > 5.5: return 'Likely'
        elif abs_margin > 1: return 'Lean'
        elif abs_margin > 0.5: return 'Tilt'
    elif winner_party == 'D':
        if abs_margin > 40: return 'Annihilation'
        elif abs_margin > 30: return 'Dominant'
        elif abs_margin > 20: return 'Stronghold'
        elif abs_margin > 10: return 'Safe'
        elif abs_margin > 5.5: return 'Likely'
        elif abs_margin > 1: return 'Lean'
        elif abs_margin > 0.5: return 'Tilt'
    return 'Tossup'

# Data structure: contests[contest]['results'][county] = {...}
with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    # Normalize fieldnames
    reader.fieldnames = [h.strip() for h in reader.fieldnames]
    for row in reader:
        # Normalize keys for each row
        row = {k.strip(): v for k, v in row.items()}
        office = row['office'].strip()
        county = row['county'].strip().upper() if row['county'].strip() else ''
        party = row['party'].strip()
        candidate = row['candidate'].strip()
        votes = int(row['votes'].replace(',', '').strip()) if row['votes'].strip() else 0
        # US Senate
        if 'United States Senator' in office:
            contest = 'us_senate_2014'
        # Governor
        elif office == 'Governor':
            contest = 'governor_2014'
        else:
            continue
        if county not in contests[contest]['results']:
            contests[contest]['results'][county] = {
                'county': county,
                'year': 2014,
                'contest_name': contests[contest]['contest_name'],
                'all_parties': {},
                'rep_votes': 0,
                'dem_votes': 0,
                'other_votes': 0,
                'rep_candidate': '',
                'dem_candidate': '',
                'other_candidate': '',
            }
        # Assign votes by party (treat 'IR' as Republican)
        if party in ('R', 'IR'):
            contests[contest]['results'][county]['rep_votes'] += votes
            contests[contest]['results'][county]['rep_candidate'] = candidate
        elif party == 'D':
            contests[contest]['results'][county]['dem_votes'] += votes
            contests[contest]['results'][county]['dem_candidate'] = candidate
        else:
            contests[contest]['results'][county]['other_votes'] += votes
            contests[contest]['results'][county]['other_candidate'] = candidate
        contests[contest]['results'][county]['all_parties'][candidate] = votes

# Calculate statewide totals and margin/category for each contest
for contest in contests:
    statewide = {
        'county': '',
        'year': 2014,
        'contest_name': contests[contest]['contest_name'],
        'all_parties': {},
        'rep_votes': 0,
        'dem_votes': 0,
        'other_votes': 0,
        'rep_candidate': '',
        'dem_candidate': '',
        'other_candidate': '',
    }
    for county, data in contests[contest]['results'].items():
        if county == '':
            continue
        statewide['rep_votes'] += data['rep_votes']
        statewide['dem_votes'] += data['dem_votes']
        statewide['other_votes'] += data['other_votes']
        for cand, v in data['all_parties'].items():
            statewide['all_parties'][cand] = statewide['all_parties'].get(cand, 0) + v
        if data['rep_candidate']:
            statewide['rep_candidate'] = data['rep_candidate']
        if data['dem_candidate']:
            statewide['dem_candidate'] = data['dem_candidate']
        if data['other_candidate']:
            statewide['other_candidate'] = data['other_candidate']
    # Margin/category
    rep = statewide['rep_votes']
    dem = statewide['dem_votes']
    other = statewide['other_votes']
    two_party_total = rep + dem
    total_votes = rep + dem + other
    statewide['two_party_total'] = two_party_total
    statewide['total_votes'] = total_votes
    if rep > dem:
        winner = statewide['rep_candidate']
        margin = rep - dem
        winner_party = 'R'
    else:
        winner = statewide['dem_candidate']
        margin = dem - rep
        winner_party = 'D'
    statewide['winner'] = winner
    statewide['margin'] = margin
    statewide['margin_pct'] = round((margin / two_party_total) * 100, 2) if two_party_total else 0.0
    statewide['category'] = get_category(statewide['margin_pct'], winner_party)
    contests[contest]['results'][''] = statewide
    # Now do margin/category for each county
    for county, data in contests[contest]['results'].items():
        rep = data['rep_votes']
        dem = data['dem_votes']
        other = data['other_votes']
        two_party_total = rep + dem
        total_votes = rep + dem + other
        data['two_party_total'] = two_party_total
        data['total_votes'] = total_votes
        if rep > dem:
            winner = data['rep_candidate']
            margin = rep - dem
            winner_party = 'R'
        else:
            winner = data['dem_candidate']
            margin = dem - rep
            winner_party = 'D'
        data['winner'] = winner
        data['margin'] = margin
        data['margin_pct'] = round((margin / two_party_total) * 100, 2) if two_party_total else 0.0
        data['category'] = get_category(data['margin_pct'], winner_party)

# Output as JSON
output = {'results_by_year': {'2014': contests}}
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2)
print(f"Wrote 2014 Senate and Governor results to {out_path}")
