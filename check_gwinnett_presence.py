import json

FILLED_PATH = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data_files\results_by_year_grouped.filled.json"
CHECK_YEARS = ["2021", "2022"]
CHECK_CONTESTS = [
    "public_service_commissioner_2021",
    "us_senate_2021",
    "us_senate_special_2021",
    "governor_2022",
    "lieutenant_governor_2022",
    "secretary_of_state_2022",
    "attorney_general_2022",
    "commissioner_of_agriculture_2022",
    "commissioner_of_insurance_2022",
    "commissioner_of_labor_2022"
]

COUNTY_NAME = "Gwinnett"

# Try both original and normalized forms
COUNTY_NAMES = [COUNTY_NAME, COUNTY_NAME.upper(), COUNTY_NAME.lower(), COUNTY_NAME.capitalize()]

def check_gwinnett_presence():
    with open(FILLED_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    results_by_year = data.get('results_by_year', {})
    for year in CHECK_YEARS:
        for contest in CHECK_CONTESTS:
            contest_data = results_by_year.get(year, {}).get(contest, {})
            counties = contest_data.get('results', {})
            found = False
            for name in COUNTY_NAMES:
                if name in counties:
                    print(f"{year} {contest}: Gwinnett found as '{name}'")
                    found = True
                    break
            if not found:
                print(f"{year} {contest}: Gwinnett NOT found.")

if __name__ == "__main__":
    check_gwinnett_presence()
