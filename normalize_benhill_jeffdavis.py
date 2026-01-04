import json
import re

RESULTS_JSON = r"data_files/results_by_year_grouped.filled.json"
OUTPUT_JSON = r"data_files/results_by_year_grouped.filled_normalized.json"

# County normalization mapping
COUNTY_NORMALIZATION = {
    re.compile(r"^ben[_ ]?hill$", re.IGNORECASE): "BEN HILL",
    re.compile(r"^jeff[_ ]?davis$", re.IGNORECASE): "JEFF DAVIS"
}

def normalize_county_key(key):
    for pattern, norm in COUNTY_NORMALIZATION.items():
        if pattern.match(key.replace(' ', '').replace('_', '')):
            return norm
    return key

with open(RESULTS_JSON, 'r', encoding='utf-8') as f:
    results = json.load(f)

for year, contests in results.get('results_by_year', {}).items():
    for contest, contest_data in contests.items():
        if 'results' in contest_data:
            counties = list(contest_data['results'].keys())
            for county in counties:
                norm_county = normalize_county_key(county)
                if norm_county != county:
                    contest_data['results'][norm_county] = contest_data['results'].pop(county)
                    print(f"Renamed {county} to {norm_county} in {year}, {contest}")

with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)
print(f"Done. Output written to {OUTPUT_JSON}")
