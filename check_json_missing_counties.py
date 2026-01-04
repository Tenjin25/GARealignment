import json

# List of all Georgia counties (normalized, no 'county' suffix, no spaces)
all_counties = [
    'appling', 'atkinson', 'bacon', 'baker', 'baldwin', 'banks', 'barrow', 'bartow', 'benhill', 'berrien', 'bibb', 'bleckley', 'brantley', 'brooks', 'bulloch', 'burke', 'butts', 'calhoun', 'camden', 'candler', 'carroll', 'catoosa', 'charlton', 'chatham', 'chattahoochee', 'chattooga', 'cherokee', 'clarke', 'clay', 'clayton', 'clinch', 'cobb', 'coffee', 'colquitt', 'columbia', 'cook', 'coweta', 'crisp', 'dade', 'dawson', 'decatur', 'dekalb', 'dodge', 'dooly', 'douglas', 'early', 'echols', 'effingham', 'elbert', 'emanuel', 'evans', 'fannin', 'fayette', 'floyd', 'forsyth', 'franklin', 'fulton', 'gilmer', 'glascock', 'glynn', 'gordon', 'grady', 'greene', 'gwinnett', 'habersham', 'hall', 'hancock', 'haralson', 'harris', 'hart', 'heard', 'henry', 'houston', 'irwin', 'jackson', 'jasper', 'jeffdavis', 'jefferson', 'jenkins', 'johnson', 'jones', 'lamar', 'lanier', 'laurens', 'lee', 'liberty', 'lincoln', 'long', 'lowndes', 'lumpkin', 'macon', 'madison', 'marion', 'mcduffie', 'mcintosh', 'meriwether', 'miller', 'mitchell', 'monroe', 'montgomery', 'morgan', 'murray', 'muscogee', 'newton', 'oconee', 'oglethorpe', 'paulding', 'peach', 'pickens', 'pierce', 'pike', 'polk', 'pulaski', 'putnam', 'quitman', 'rabun', 'randolph', 'richmond', 'rockdale', 'schley', 'screven', 'seminole', 'spalding', 'stephens', 'stewart', 'sumter', 'talbot', 'taliaferro', 'tattnall', 'taylor', 'telfair', 'terrell', 'thomas', 'tift', 'toombs', 'towns', 'treutlen', 'troup', 'turner', 'twiggs', 'union', 'upson', 'walker', 'walton', 'ware', 'warren', 'washington', 'wayne', 'webster', 'wheeler', 'white', 'whitfield', 'wilcox', 'wilkes', 'wilkinson', 'worth'
]

def normalize_county(name):
    name = name.strip().lower().replace('county', '').replace(' ', '')
    if name == 'musco':
        return 'muscogee'
    return name

json_path = 'data/results_by_year_grouped.json'

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for year, contests in data.get('results_by_year', {}).items():
    for contest, contest_obj in contests.items():
        print(f'Year: {year}, Contest: {contest}')
        results = contest_obj.get('results', contest_obj)
        counties_in_results = set()
        for county_name in results.keys():
            counties_in_results.add(normalize_county(county_name))
        missing = [c for c in all_counties if c not in counties_in_results]
        if missing:
            print(f'  Missing counties ({len(missing)}): {missing}')
        else:
            print('  All counties present.')
