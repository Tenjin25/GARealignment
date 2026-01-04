import json

with open(r'c:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data\results_by_year_grouped.updated2022.json') as f:
    d = json.load(f)

counties = sorted(d['results_by_year']['2022']['governor_2022']['results'].keys())
print(f'Total counties: {len(counties)}')

# Compare with GeoJSON
with open(r'c:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\tl_2020_13_county20.geojson') as f:
    geo = json.load(f)

geojson_counties = sorted([f['properties']['NAME20'] for f in geo['features']])
print(f'GeoJSON counties: {len(geojson_counties)}')

# Find differences
extra_in_result = set(counties) - set(geojson_counties)
missing_from_result = set(geojson_counties) - set(counties)

if extra_in_result:
    print(f'\nExtra in results (not in GeoJSON): {len(extra_in_result)}')
    for c in sorted(extra_in_result):
        print(f'  - {c}')

if missing_from_result:
    print(f'\nMissing from results (in GeoJSON): {len(missing_from_result)}')
    for c in sorted(missing_from_result):
        print(f'  - {c}')
