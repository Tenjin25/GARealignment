import json

FILLED_PATH = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data_files\results_by_year_grouped.filled.json"
# Only check contests/years that were filled
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

EXPECTED_KEYS = [
    "dem_candidate", "rep_candidate", "dem_votes", "rep_votes", "other_votes", "total_votes", "two_party_total", "margin", "margin_pct", "winner", "winner_name", "winner_party", "winner_incumbent", "winner_votes", "competitiveness", "all_parties", "candidates", "contest", "county", "year"
]

def validate_county_format():
    with open(FILLED_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    results_by_year = data.get('results_by_year', {})
    for year in CHECK_YEARS:
        for contest in CHECK_CONTESTS:
            contest_data = results_by_year.get(year, {}).get(contest, {})
            counties = contest_data.get('results', {})
            if not counties:
                print(f"{year} {contest}: No counties found.")
                continue
            # Check one sample county
            sample_county = next(iter(counties))
            county_data = counties[sample_county]
            missing_keys = [k for k in EXPECTED_KEYS if k not in county_data]
            extra_keys = [k for k in county_data if k not in EXPECTED_KEYS]
            print(f"{year} {contest} - Sample county: {sample_county}")
            print(f"  Missing keys: {missing_keys}")
            print(f"  Extra keys: {extra_keys}")
            print(f"  Types: {{k: type(county_data[k]).__name__ for k in county_data}}\n")

if __name__ == "__main__":
    validate_county_format()
