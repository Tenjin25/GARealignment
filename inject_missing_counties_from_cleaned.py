import json

# Paths
CLEANED_JSON = r"data/cleaned/ga_county_results.normalized.json"
RESULTS_JSON = r"data_files/results_by_year_grouped.filled.json"
OUTPUT_JSON = r"data_files/results_by_year_grouped.filled_with_missing_counties.json"

# Contests and missing counties (all lowercase, two words for ben hill, jeff davis)
CONTESTS_2022 = [
    "governor_2022",
    "lieutenant_governor_2022",
    "secretary_of_state_2022",
    "attorney_general_2022",
    "commissioner_of_agriculture_2022",
    "commissioner_of_insurance_2022",
    "commissioner_of_labor_2022"
]
MISSING_COUNTIES_BY_CONTEST = {
    "governor_2022": ['gwinnett'],
    "lieutenant_governor_2022": ['gwinnett'],
    "secretary_of_state_2022": ['gwinnett'],
    "attorney_general_2022": ['gwinnett'],
    "commissioner_of_agriculture_2022": ['bartow', 'carroll', 'catoosa', 'chattahoochee', 'chattooga', 'cherokee', 'clayton', 'coweta', 'dade', 'dawson', 'douglas', 'fannin', 'fayette', 'floyd', 'forsyth', 'fulton', 'gilmer', 'gordon', 'gwinnett', 'haralson', 'harris', 'heard', 'lumpkin', 'macon', 'marion', 'murray', 'muscogee', 'paulding', 'pickens', 'polk', 'schley', 'stewart', 'sumter', 'talbot', 'taylor', 'troup', 'union', 'upson', 'walker', 'webster', 'whitfield', 'wilcox', 'ben hill', 'jeff davis'],
    "commissioner_of_insurance_2022": ['bartow', 'carroll', 'catoosa', 'chattahoochee', 'chattooga', 'cherokee', 'clayton', 'coweta', 'dade', 'dawson', 'douglas', 'fannin', 'fayette', 'floyd', 'forsyth', 'fulton', 'gilmer', 'gordon', 'gwinnett', 'haralson', 'harris', 'heard', 'lumpkin', 'macon', 'marion', 'murray', 'muscogee', 'paulding', 'pickens', 'polk', 'schley', 'stewart', 'sumter', 'talbot', 'taylor', 'troup', 'union', 'upson', 'walker', 'webster', 'whitfield', 'wilcox', 'ben hill', 'jeff davis'],
    "commissioner_of_labor_2022": ['bartow', 'carroll', 'catoosa', 'chattahoochee', 'chattooga', 'cherokee', 'clayton', 'coweta', 'dade', 'dawson', 'douglas', 'fannin', 'fayette', 'floyd', 'forsyth', 'fulton', 'gilmer', 'gordon', 'gwinnett', 'haralson', 'harris', 'heard', 'lumpkin', 'macon', 'marion', 'murray', 'muscogee', 'paulding', 'pickens', 'polk', 'schley', 'stewart', 'sumter', 'talbot', 'taylor', 'troup', 'union', 'upson', 'walker', 'webster', 'whitfield', 'wilcox', 'ben hill', 'jeff davis']
}

# Helper to normalize county names (two words, title case)
def normalize_county(name):
    name = name.replace('_', ' ').replace('-', ' ').strip()
    name = ' '.join([w.capitalize() for w in name.split()])
    return name

# Load cleaned county results
with open(CLEANED_JSON, 'r', encoding='utf-8') as f:
    cleaned = json.load(f)

# Load main results JSON
with open(RESULTS_JSON, 'r', encoding='utf-8') as f:
    results = json.load(f)


# Inject missing counties for each contest
year_json = results['results_by_year'].setdefault('2022', {})
for contest in CONTESTS_2022:
    contest_json = year_json.setdefault(contest, {})
    contest_results = contest_json.setdefault('results', {})
    cleaned_contest = cleaned['results_by_year']['2022'][contest]['results']
    missing_counties = MISSING_COUNTIES_BY_CONTEST.get(contest, [])
    for county in missing_counties:
        norm_county = normalize_county(county)
        found = None
        county_match = county.replace(' ', '').replace('_', '').strip().lower()
        norm_county_match = norm_county.replace(' ', '').replace('_', '').strip().lower()
        for key in cleaned_contest.keys():
            key_match = key.replace(' ', '').replace('_', '').strip().lower()
            if key_match == county_match or key_match == norm_county_match:
                found = cleaned_contest[key]
                break
        if found:
            contest_results[norm_county.upper()] = found
            print(f"Injected {norm_county.upper()} for {contest}")
        else:
            print(f"No data found for {norm_county.upper()} in {contest}")

# Write output
with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)
print(f"Done. Output written to {OUTPUT_JSON}")
