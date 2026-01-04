import json
import csv

# Load the raw JSON
with open("ga_2022_sos_raw.json", "r", encoding="utf-8") as f:
    data = json.load(f)

rows = []
for contest in data.get("contests", []):
    contest_name = contest.get("name", "")
    for county in contest.get("counties", []):
        county_name = county.get("name", "")
        for candidate in county.get("candidates", []):
            candidate_name = candidate.get("name", "")
            party = candidate.get("party", "")
            votes = candidate.get("votes", "")
            rows.append({
                "contest": contest_name,
                "county": county_name,
                "candidate": candidate_name,
                "party": party,
                "votes": votes
            })

# Write to CSV
with open("ga_2022_sos_all_results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["contest", "county", "candidate", "party", "votes"])
    writer.writeheader()
    writer.writerows(rows)

print("All results saved to ga_2022_sos_all_results.csv")
