import json

# Load the data
with open('data/results_by_year_grouped.final.json', 'r') as f:
    data = json.load(f)

regions = {
    'Southwest (Black-majority)': ['Dougherty', 'Mitchell', 'Terrell', 'Randolph', 'Clay', 'Quitman', 'Stewart', 'Webster'],
    'Black Belt': ['Macon', 'Hancock', 'Warren', 'Baldwin', 'Washington', 'Jefferson'],
    'Middle GA Urban': ['Bibb', 'Houston', 'Muscogee'],
    'Northeast Mountains': ['Hall', 'Jackson', 'Banks'],
    'Northwest Appalachia': ['Floyd', 'Whitfield', 'Murray'],
    'South GA Agriculture': ['Colquitt', 'Lowndes', 'Tift'],
    'Coastal': ['Chatham', 'Glynn', 'Camden']
}

years = ['2000', '2004', '2008', '2012', '2016', '2020', '2024']

for region, counties in regions.items():
    print(f"\n{region}:")
    print("=" * 80)
    for county in counties:
        print(f"\n  {county} County:")
        for year in years:
            if year in data['results_by_year']:
                contest_key = f"president_of_the_united_states_{year}" if year == '2016' else f"president_{year}"
                
                if contest_key in data['results_by_year'][year]:
                    if county in data['results_by_year'][year][contest_key]['results']:
                        result = data['results_by_year'][year][contest_key]['results'][county]
                        print(f"    {year}: {result['margin_pct']:>8} ({result['competitiveness']['category']:>13} {result['competitiveness']['party']:>10}) - {result['dem_votes']:>6,} D vs {result['rep_votes']:>6,} R")
