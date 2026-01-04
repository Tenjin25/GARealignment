import requests
import json

# Official GA SOS API endpoint for 2022 General Election
URL = "https://results.sos.ga.gov/results/public/api/elections/Georgia/2022NovGen/data"

response = requests.get(URL)
data = response.json()

# Save raw JSON for inspection
with open("ga_2022_sos_raw.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Raw GA SOS 2022 election data saved to ga_2022_sos_raw.json")

# Example: Extract county-level results for Governor contest
# The structure may be nested; inspect the raw file to find the correct path
# Here's a generic extraction template:

governor_results = []
for contest in data.get("contests", []):
    if "governor" in contest.get("name", "").lower():
        for county in contest.get("counties", []):
            county_name = county.get("name")
            candidates = county.get("candidates", [])
            result = {"county": county_name}
            for cand in candidates:
                result[cand.get("party", cand.get("name", "Candidate"))] = cand.get("votes")
            governor_results.append(result)

with open("ga_2022_governor_county_results_from_api.json", "w", encoding="utf-8") as f:
    json.dump(governor_results, f, indent=2, ensure_ascii=False)

print("County-level governor results saved to ga_2022_governor_county_results_from_api.json")
