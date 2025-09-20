import json
import re

# Input/output file
infile = 'data/ga_county_results_trimmed.merged_final.json'
outfile = 'data/ga_county_results_trimmed.merged_final.cleaned.json'

# Remove only (I) from candidate names, keep (R)
paren_i_pattern = re.compile(r'\s*\(I\)\s*', re.IGNORECASE)

def clean_candidate(name):
    if not isinstance(name, str):
        return name
    return paren_i_pattern.sub(' ', name).replace('  ', ' ').strip()

with open(infile, encoding='utf-8') as f:
    data = json.load(f)

for year, year_data in data.get('results_by_year', {}).items():
    for contest, contest_data in year_data.items():
        results = contest_data.get('results', {})
        for county, county_data in results.items():
            # Clean dem_candidate and rep_candidate
            if 'dem_candidate' in county_data:
                county_data['dem_candidate'] = clean_candidate(county_data['dem_candidate'])
            if 'rep_candidate' in county_data:
                county_data['rep_candidate'] = clean_candidate(county_data['rep_candidate'])
            # Optionally clean all_parties keys if needed (not usually necessary)

with open(outfile, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f"Cleaned candidate names written to {outfile}")
