import json

infile = 'data/ga_senate_2016_by_county.json'
outfile = 'data/ga_senate_2016_by_county.categorized.json'

# Category logic with party
CATEGORY_THRESHOLDS = [
    (40, 'Annihilation'),
    (30, 'Dominant'),
    (20, 'Stronghold'),
    (10, 'Safe'),
    (5.5, 'Likely'),
    (1, 'Lean'),
    (0.5, 'Tilt'),
    (0, 'Tossup')
]

def get_category(margin_pct, winner_party):
    for threshold, label in CATEGORY_THRESHOLDS:
        if margin_pct >= threshold:
            if label == 'Tossup':
                return f'Tossup ({winner_party} Win)'
            return f'{label} {winner_party}'
    return f'Tossup ({winner_party} Win)'

def get_winner_party(rep_votes, dem_votes):
    if rep_votes > dem_votes:
        return 'Republican'
    elif dem_votes > rep_votes:
        return 'Democratic'
    else:
        return 'Tie'

with open(infile, encoding='utf-8') as f:
    data = json.load(f)

results = data['results_by_year']['2016']['us_senate_2016']['results']
for county, entry in results.items():
    rep_votes = entry.get('rep_votes', 0)
    dem_votes = entry.get('dem_votes', 0)
    margin = abs(rep_votes - dem_votes)
    total = rep_votes + dem_votes
    margin_pct = (margin / total * 100) if total else 0
    winner_party = get_winner_party(rep_votes, dem_votes)
    # Update winner field to party
    entry['winner'] = winner_party
    entry['margin'] = margin
    entry['margin_pct'] = round(margin_pct, 2)
    entry['category'] = get_category(margin_pct, winner_party)

with open(outfile, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f"Updated 2016 US Senate results with category and winning party in {outfile}")
