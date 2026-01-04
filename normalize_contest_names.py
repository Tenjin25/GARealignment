import json
import re

# Path to your results JSON file
INPUT_PATH = "data/cleaned/ga_county_results.json"
OUTPUT_PATH = "data/cleaned/ga_county_results.normalized.json"

def normalize_contest_name(name):
    # Remove leading/trailing whitespace and collapse multiple spaces
    return re.sub(r"\s+", " ", name.strip())

def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Recursively normalize all contest_name fields
    for year, contests in data.get("results_by_year", {}).items():
        for contest_key, contest_data in contests.items():
            if isinstance(contest_data, dict) and "results" in contest_data:
                for county, county_data in contest_data["results"].items():
                    if isinstance(county_data, dict) and "contest_name" in county_data:
                        old_name = county_data["contest_name"]
                        new_name = normalize_contest_name(old_name)
                        county_data["contest_name"] = new_name

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Normalized contest_name fields written to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
