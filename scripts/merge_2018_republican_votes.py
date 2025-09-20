import csv
import json

# Update these paths as needed
CSV_PATH = "data/merged_precincts_2018.csv"  # Path to your 2018 CSV
JSON_PATH = "data/ga_county_results_trimmed.merged_final.cleaned.filled2018.json"  # Output from previous script
OUTPUT_JSON = "data/ga_county_results_trimmed.merged_final.cleaned.filled2018.votes.json"

# Map contest names in CSV to JSON contest names and Republican candidate names
CONTESTS = {
    "Governor": "Brian Kemp",
    "Attorney General": "Chris Carr",
    "Secretary of State": "Brad Raffensperger",
    "Lt. Governor": "Geoff Duncan",
    "Insurance Commissioner": "Jim Beck",
    "Agriculture Commissioner": "Gary Black",
    "Labor Commissioner": "Mark Butler",
    "State School Superintendent": "Richard Woods"
}

def load_csv_votes():
    """Returns: dict[contest][county] = (rep_name, rep_votes)"""
    votes = {contest: {} for contest in CONTESTS}
    with open(CSV_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            county = row.get("County") or row.get("county")
            for contest, rep_name in CONTESTS.items():
                # Try to find the correct columns for this contest
                cand_col = f"{contest} Republican Name"
                votes_col = f"{contest} Republican Votes"
                if cand_col in row and votes_col in row:
                    name = row[cand_col].strip() or rep_name
                    try:
                        v = int(row[votes_col].replace(",", ""))
                    except Exception:
                        v = 0
                    votes[contest][county] = (name, v)
    return votes

def update_json_with_votes(data, votes):
    year_data = data.get("results_by_year", {}).get("2018", {})
    for contest, contest_data in year_data.items():
        if contest not in votes:
            continue
        for county, county_data in contest_data.get("results", {}).items():
            rep_name, rep_votes = votes[contest].get(county, (None, None))
            found = False
            for cand in county_data.get("candidates", []):
                if cand.get("party") == "R":
                    cand["name"] = rep_name or cand.get("name")
                    cand["votes"] = rep_votes if rep_votes is not None else cand.get("votes", 0)
                    found = True
                    break
            if not found and rep_name:
                county_data.setdefault("candidates", []).append({
                    "name": rep_name,
                    "party": "R",
                    "votes": rep_votes if rep_votes is not None else 0
                })
    return data

def main():
    with open(JSON_PATH, encoding="utf-8") as f:
        data = json.load(f)
    votes = load_csv_votes()
    data = update_json_with_votes(data, votes)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Updated 2018 Republican vote totals. Output: {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
