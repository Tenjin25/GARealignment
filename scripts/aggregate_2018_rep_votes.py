import csv
import json
from collections import defaultdict

CSV_PATH = "data/merged_precincts_2018.csv"
JSON_PATH = "data/ga_county_results_trimmed.merged_final.cleaned.filled2018.json"
OUTPUT_JSON = "data/ga_county_results_trimmed.merged_final.cleaned.filled2018.agg.json"

# Map office names in CSV to JSON contest names
CONTESTS = {
    "Governor": "Governor",
    "Attorney General": "Attorney General",
    "Secretary of State": "Secretary of State",
    "Lt. Governor": "Lt. Governor",
    "Insurance Commissioner": "Insurance Commissioner",
    "Agriculture Commissioner": "Agriculture Commissioner",
    "Labor Commissioner": "Labor Commissioner",
    "State School Superintendent": "State School Superintendent"
}

def aggregate_rep_votes():
    # Structure: contest -> county -> {name, votes}
    agg = {contest: defaultdict(lambda: {"votes": 0, "name": None}) for contest in CONTESTS}
    with open(CSV_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            office = row.get("office")
            party = row.get("party")
            county = row.get("county") or row.get("County")
            candidate = row.get("candidate")
            votes = row.get("votes")
            if office in CONTESTS and party == "REP":
                try:
                    v = int(float(votes.replace(",", "")))
                except Exception:
                    v = 0
                c = agg[office][county]
                c["votes"] += v
                c["name"] = candidate.title() if candidate else c["name"]
    return agg

def update_json_with_agg(data, agg):
    year_data = data.get("results_by_year", {}).get("2018", {})
    for contest, contest_data in year_data.items():
        if contest not in agg:
            continue
        for county, county_data in contest_data.get("results", {}).items():
            rep_info = agg[contest].get(county)
            if not rep_info:
                continue
            found = False
            for cand in county_data.get("candidates", []):
                if cand.get("party") == "R":
                    cand["name"] = rep_info["name"] or cand.get("name")
                    cand["votes"] = rep_info["votes"]
                    found = True
                    break
            if not found and rep_info["name"]:
                county_data.setdefault("candidates", []).append({
                    "name": rep_info["name"],
                    "party": "R",
                    "votes": rep_info["votes"]
                })
    return data

def main():
    agg = aggregate_rep_votes()
    with open(JSON_PATH, encoding="utf-8") as f:
        data = json.load(f)
    data = update_json_with_agg(data, agg)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Aggregated and updated 2018 REP votes. Output: {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
