import json

with open('data/results_by_year_grouped.final.json') as f:
    data = json.load(f)

# Check Johnson County in 2000 US Senate
us_senate_2000 = data['results_by_year']['2000']['us_senate_2000']

if 'Johnson' in us_senate_2000:
    johnson = us_senate_2000['Johnson']
    print('Johnson County 2000 US Senate:')
    print(f"  Dem votes: {johnson['dem_votes']}")
    print(f"  Rep votes: {johnson['rep_votes']}")
    print(f"  Winner: {johnson['winner']}")
    print(f"  Margin: {johnson['margin_pct']}")
    print(f"  Competitiveness: {johnson['competitiveness']}")
