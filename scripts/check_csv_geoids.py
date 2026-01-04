import csv

csv_path = r'c:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data_files\Election_Data_GA.v04\election_data_GA.v04-aligned.csv'

with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = [{k.strip(): v for k, v in r.items() if k} for r in reader]

print(f'Total rows: {len(rows)}')
print('\nFirst 10 entries:')
for i in range(min(10, len(rows))):
    geoid = rows[i]['GEOID20']
    name = rows[i]['Name']
    county_code = geoid[:5] if len(geoid) >= 5 else geoid
    print(f'{geoid:<15} -> County: {county_code:<7} {name[:50]}')

# Check unique county codes
county_codes = set()
for r in rows:
    geoid = r['GEOID20']
    if len(geoid) >= 5:
        county_codes.add(geoid[:5])

print(f'\nUnique county codes found: {len(county_codes)}')
print(f'Expected: 159 (GA has 159 counties)')
