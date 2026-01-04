import json
import os

# Paths to your files
ORIGINAL_PATH = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data_files\ga_county_results_trimmed.updated.json"
NEW_PATH = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data_files\results_by_year_grouped.json"
OUTPUT_PATH = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data_files\results_by_year_grouped.filled.json"

# List of years/contests to check (from your scan)
MISSING_INFO = {
    "2021": [
        "public_service_commissioner_2021",
        "us_senate_2021",
        "us_senate_special_2021"
    ],
    "2022": [
        "governor_2022",
        "lieutenant_governor_2022",
        "secretary_of_state_2022",
        "attorney_general_2022",
        "commissioner_of_agriculture_2022",
        "commissioner_of_insurance_2022",
        "commissioner_of_labor_2022"
    ]
}

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def fill_missing_counties():
    original = load_json(ORIGINAL_PATH)
    new = load_json(NEW_PATH)
    orig_by_year = original['results_by_year']
    new_by_year = new['results_by_year']
    filled_count = 0
    for year, contests in MISSING_INFO.items():
        if year not in new_by_year or year not in orig_by_year:
            continue
        for contest in contests:
            if contest not in new_by_year[year] or contest not in orig_by_year[year]:
                continue
            # Get county dicts from 'results' key
            orig_results = orig_by_year[year][contest].get('results', {})
            new_results = new_by_year[year][contest].get('results', {})
            new_counties = set(new_results.keys())
            orig_counties = set(orig_results.keys())
            missing = orig_counties - new_counties
            for county in missing:
                new_results[county] = orig_results[county]
                filled_count += 1
            # Save back the updated results dict
            new_by_year[year][contest]['results'] = new_results
            if missing:
                print(f"Year: {year}, Contest: {contest} - Added counties: {sorted(list(missing))}")
    save_json(new, OUTPUT_PATH)
    print(f"\nTotal counties filled: {filled_count}")
    print(f"Filled file saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    fill_missing_counties()
