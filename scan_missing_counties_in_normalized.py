import json

# Path to normalized results file
INPUT_PATH = "data/cleaned/ga_county_results.normalized.json"

# List of contests and counties to check
CONTESTS_2022 = [
    "governor_2022",
    "lieutenant_governor_2022",
    "secretary_of_state_2022",
    "attorney_general_2022",
    "commissioner_of_agriculture_2022",
    "commissioner_of_insurance_2022",
    "commissioner_of_labor_2022"
]
MISSING_COUNTIES = [
    'gwinnett', 'bartow', 'carroll', 'catoosa', 'chattahoochee', 'chattooga', 'cherokee', 'clayton', 'coweta', 'dade', 'dawson', 'douglas', 'fannin', 'fayette', 'floyd', 'forsyth', 'fulton', 'gilmer', 'gordon', 'haralson', 'harris', 'heard', 'lumpkin', 'macon', 'marion', 'murray', 'muscogee', 'paulding', 'pickens', 'polk', 'schley', 'stewart', 'sumter', 'talbot', 'taylor', 'troup', 'union', 'upson', 'walker', 'webster', 'whitfield', 'wilcox', 'ben hill', 'jeff davis'
]

def normalize_county(name):
    name = name.replace('_', ' ').replace('-', ' ').strip()
    name = ' '.join([w.capitalize() for w in name.split()])
    return name

def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    year_data = data["results_by_year"].get("2022", {})
    for contest in CONTESTS_2022:
        contest_data = year_data.get(contest, {})
        results = contest_data.get("results", {})
        print(f"\nChecking {contest}:")
        for county in MISSING_COUNTIES:
            norm_county = normalize_county(county)
            found = False
            for key in results.keys():
                key_match = key.replace(' ', '').replace('_', '').strip().lower()
                county_match = norm_county.replace(' ', '').replace('_', '').strip().lower()
                if key_match == county_match:
                    found = True
                    break
            if found:
                print(f"  FOUND: {norm_county.upper()}")
            else:
                print(f"  NOT FOUND: {norm_county.upper()}")

if __name__ == "__main__":
    main()
