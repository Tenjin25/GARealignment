import requests
import json
from bs4 import BeautifulSoup
import pandas as pd

# Example: Governor contest results page
URL = "https://results.sos.ga.gov/results/public/Georgia/elections/2022NovGen/ballot-items/01000000-39b2-c225-39a9-08dd132698cd"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

# Find the county results table
county_table = soup.find("table")
if not county_table:
    print("No county results table found.")
    exit(1)

# Parse table into DataFrame
try:
    df = pd.read_html(str(county_table))[0]
except Exception as e:
    print(f"Error parsing table: {e}")
    exit(1)

# Clean up columns
columns = [str(c).strip() for c in df.columns]
df.columns = columns

# Extract county results
county_results = []
for _, row in df.iterrows():
    county = str(row.get("County") or row.get("COUNTY") or "").strip()
    dem_votes = row.get("Abrams, Stacey (DEM)")
    rep_votes = row.get("Kemp, Brian (REP)")
    lib_votes = row.get("Hazel, Shane (LIB)")
    total_votes = row.get("Total Votes")
    if county:
        county_results.append({
            "county": county,
            "dem_votes": int(dem_votes) if pd.notnull(dem_votes) else None,
            "rep_votes": int(rep_votes) if pd.notnull(rep_votes) else None,
            "lib_votes": int(lib_votes) if pd.notnull(lib_votes) else None,
            "total_votes": int(total_votes) if pd.notnull(total_votes) else None
        })

with open("ga_2022_governor_county_results.json", "w", encoding="utf-8") as f:
    json.dump(county_results, f, indent=2, ensure_ascii=False)

print("Extracted county results saved to ga_2022_governor_county_results.json")
