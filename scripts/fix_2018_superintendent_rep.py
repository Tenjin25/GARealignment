import json

INPUT_JSON = "data/ga_county_results_trimmed.merged_final.cleaned.filled2018.agg.json"
OUTPUT_JSON = "data/ga_county_results_trimmed.merged_final.cleaned.filled2018.agg.fixed.json"

# The correct Republican candidate for 2018 State School Superintendent
REP_CANDIDATE = "Richard Woods"

with open(INPUT_JSON, encoding="utf-8") as f:
    data = json.load(f)

# Fix (REP to REP in all_parties, and fill rep_votes/rep_candidate
results = data["results_by_year"]["2018"]["state_school_superintendent_2018"]["results"]
for county, county_data in results.items():
    # Fix all_parties key
    if "(REP" in county_data.get("all_parties", {}):
        county_data["all_parties"]["REP"] = county_data["all_parties"].pop("(REP")
    # Fill rep_votes and rep_candidate if possible
    rep_votes = county_data["all_parties"].get("REP", 0)
    county_data["rep_votes"] = rep_votes
    county_data["rep_candidate"] = REP_CANDIDATE if rep_votes > 0 else None

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Fixed REP fields and candidate names. Output: {OUTPUT_JSON}")
