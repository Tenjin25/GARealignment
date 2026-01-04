import json

ORIGINAL_PATH = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data_files\ga_county_results_trimmed.updated.json"
CHECK_YEAR = "2022"
CHECK_CONTESTS = [
    "governor_2022",
    "lieutenant_governor_2022",
    "secretary_of_state_2022",
    "attorney_general_2022",
    "commissioner_of_agriculture_2022",
    "commissioner_of_insurance_2022",
    "commissioner_of_labor_2022"
]
COUNTY_NAME = "Gwinnett"
COUNTY_NAMES = [COUNTY_NAME, COUNTY_NAME.upper(), COUNTY_NAME.lower(), COUNTY_NAME.capitalize()]

def scan_original_for_gwinnett():
    with open(ORIGINAL_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    results_by_year = data.get('results_by_year', {})
    for contest in CHECK_CONTESTS:
        contest_data = results_by_year.get(CHECK_YEAR, {}).get(contest, {})
        counties = contest_data.get('results', {})
        found = False
        for name in COUNTY_NAMES:
            if name in counties:
                print(f"{CHECK_YEAR} {contest}: Gwinnett found as '{name}'")
                found = True
                break
        if not found:
            print(f"{CHECK_YEAR} {contest}: Gwinnett NOT found.")

if __name__ == "__main__":
    scan_original_for_gwinnett()
