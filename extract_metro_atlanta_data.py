import json

# Load the data
with open('data/results_by_year_grouped.final.json', 'r') as f:
    data = json.load(f)

counties = ['Fulton', 'Dekalb', 'Gwinnett', 'Cobb', 'Forsyth', 'Cherokee', 'Fayette', 'Henry']
years = ['2000', '2004', '2008', '2012', '2016', '2020', '2024']

for county in counties:
    print(f"\n{county} County Presidential Results:")
    print("=" * 80)
    for year in years:
        if year in data['results_by_year']:
            # 2016 uses different key format
            if year == '2016':
                contest_key = f"president_of_the_united_states_{year}"
            else:
                contest_key = f"president_{year}"
            
            if contest_key in data['results_by_year'][year]:
                if county in data['results_by_year'][year][contest_key]['results']:
                    result = data['results_by_year'][year][contest_key]['results'][county]
                    print(f"{year}: {result['margin_pct']:>8} ({result['competitiveness']['category']:>13} {result['competitiveness']['party']:>10}) - {result['dem_votes']:>7,} D vs {result['rep_votes']:>7,} R")
