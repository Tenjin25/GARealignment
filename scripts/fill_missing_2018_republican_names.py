import json

# Map of 2018 contest names to Republican candidate names
REPUBLICAN_CANDIDATES_2018 = {
    "Governor": "Brian Kemp",
    "Attorney General": "Chris Carr",
    "Secretary of State": "Brad Raffensperger",
    "Lt. Governor": "Geoff Duncan",
    "Insurance Commissioner": "Jim Beck",
    "Agriculture Commissioner": "Gary Black",
    "Labor Commissioner": "Mark Butler",
    "State School Superintendent": "Richard Woods"
}

INPUT_JSON = "data/ga_county_results_trimmed.merged_final.cleaned.json"
OUTPUT_JSON = "data/ga_county_results_trimmed.merged_final.cleaned.filled2018.json"

def fill_missing_republican_names(data):
    year_data = data.get("results_by_year", {}).get("2018", {})
    for contest, contest_data in year_data.items():
        rep_name = REPUBLICAN_CANDIDATES_2018.get(contest)
        if not rep_name:
            continue  # Skip contests not in our list
        for county, county_data in contest_data.get("results", {}).items():
            # Find the Republican entry
            rep_entry = None
            for cand in county_data.get("candidates", []):
                if cand.get("party") == "R":
                    rep_entry = cand
                    break
            if rep_entry:
                if not rep_entry.get("name") or rep_entry["name"].strip() == "":
                    rep_entry["name"] = rep_name
            else:
                # If no Republican entry, add one with 0 votes
                county_data.setdefault("candidates", []).append({
                    "name": rep_name,
                    "party": "R",
                    "votes": 0
                })
    return data

def main():
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    data = fill_missing_republican_names(data)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Filled missing 2018 Republican candidate names. Output: {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
