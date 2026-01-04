import csv

# List of all Georgia counties (normalized, no 'county' suffix, no spaces)
all_counties = [
    'appling', 'atkinson', 'bacon', 'baker', 'baldwin', 'banks', 'barrow', 'bartow', 'benhill', 'berrien', 'bibb', 'bleckley', 'brantley', 'brooks', 'bulloch', 'burke', 'butts', 'calhoun', 'camden', 'candler', 'carroll', 'catoosa', 'charlton', 'chatham', 'chattahoochee', 'chattooga', 'cherokee', 'clarke', 'clay', 'clayton', 'clinch', 'cobb', 'coffee', 'colquitt', 'columbia', 'cook', 'coweta', 'crisp', 'dade', 'dawson', 'decatur', 'dekalb', 'dodge', 'dooly', 'douglas', 'early', 'echols', 'effingham', 'elbert', 'emanuel', 'evans', 'fannin', 'fayette', 'floyd', 'forsyth', 'franklin', 'fulton', 'gilmer', 'glascock', 'glynn', 'gordon', 'grady', 'greene', 'gwinnett', 'habersham', 'hall', 'hancock', 'haralson', 'harris', 'hart', 'heard', 'henry', 'houston', 'irwin', 'jackson', 'jasper', 'jeffdavis', 'jefferson', 'jenkins', 'johnson', 'jones', 'lamar', 'lanier', 'laurens', 'lee', 'liberty', 'lincoln', 'long', 'lowndes', 'lumpkin', 'macon', 'madison', 'marion', 'mcduffie', 'mcintosh', 'meriwether', 'miller', 'mitchell', 'monroe', 'montgomery', 'morgan', 'murray', 'musco', 'newton', 'oconee', 'oglethorpe', 'paulding', 'peach', 'pickens', 'pierce', 'pike', 'polk', 'pulaski', 'putnam', 'quitman', 'rabun', 'randolph', 'richmond', 'rockdale', 'schley', 'screven', 'seminole', 'spalding', 'stephens', 'stewart', 'sumter', 'talbot', 'taliaferro', 'tattnall', 'taylor', 'telfair', 'terrell', 'thomas', 'tift', 'toombs', 'towns', 'treutlen', 'troup', 'turner', 'twiggs', 'union', 'upson', 'walker', 'walton', 'ware', 'warren', 'washington', 'wayne', 'webster', 'wheeler', 'white', 'whitfield', 'wilcox', 'wilkes', 'wilkinson', 'worth'
]

def normalize_county(name):
    return name.strip().lower().replace('county', '').replace(' ', '')

csv_path = 'data/20221206__ga__general_runoff__precinct.csv'  # Update path as needed
target_office = 'U.S. Senate'  # Change as needed

counties_in_csv = set()

with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        office = row['office'].strip().lower()
        county = normalize_county(row['county'])
        if target_office.lower() in office:
            counties_in_csv.add(county)

missing = [c for c in all_counties if c not in counties_in_csv]

print(f'Missing counties for {target_office}:')
for c in missing:
    print(c)
