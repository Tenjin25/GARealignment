import json

INPUT_JSON = "data/ga_county_results_trimmed.merged_final.cleaned.filled2018.agg.json"
OUTPUT_JSON = "data/ga_county_results_trimmed.merged_final.cleaned.filled2018.agg.fixed.json"

# Map of 2018 contest names to Republican candidate names
REP_CANDIDATES = {
    "Governor": "Brian Kemp",
    "Attorney General": "Chris Carr",
    "Secretary of State": "Brad Raffensperger",
    "Lt. Governor": "Geoff Duncan",
    "Insurance Commissioner": "Jim Beck",
    "Agriculture Commissioner": "Gary Black",
    "Labor Commissioner": "Mark Butler",
    "State School Superintendent": "Richard Woods"
}

def fix_rep_fields(data):
    results_by_year = data["results_by_year"].get("2018", {})
    for contest_key, contest_obj in results_by_year.items():
        # Try to match contest name
        contest_name = contest_obj.get("contest_name") or contest_key.replace("_2018", "").replace("_", " ").title()
        rep_candidate = REP_CANDIDATES.get(contest_name)
        if not rep_candidate:
            continue
        for county, county_data in contest_obj.get("results", {}).items():
            # Fix all_parties key
            if "(REP" in county_data.get("all_parties", {}):
                county_data["all_parties"]["REP"] = county_data["all_parties"].pop("(REP")
            # Fill rep_votes and rep_candidate if possible
            rep_votes = county_data["all_parties"].get("REP", 0)
            county_data["rep_votes"] = rep_votes
            county_data["rep_candidate"] = rep_candidate if rep_votes > 0 else None
    return data

def main():
    with open(INPUT_JSON, encoding="utf-8") as f:
        data = json.load(f)
    data = fix_rep_fields(data)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Fixed REP fields and candidate names for all 2018 contests. Output: {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
