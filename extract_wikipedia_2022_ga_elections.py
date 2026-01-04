
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json

CONTEST_URLS = {
    "Governor": "https://en.wikipedia.org/wiki/2022_Georgia_gubernatorial_election",
    "Lieutenant Governor": "https://en.wikipedia.org/wiki/2022_Georgia_lieutenant_gubernatorial_election",
    "Secretary of State": "https://en.wikipedia.org/wiki/2022_Georgia_Secretary_of_State_election",
    "Attorney General": "https://en.wikipedia.org/wiki/2022_Georgia_Attorney_General_election",
    "Commissioner of Agriculture": "https://en.wikipedia.org/wiki/2022_Georgia_Commissioner_of_Agriculture_election",
    "Commissioner of Insurance": "https://en.wikipedia.org/wiki/2022_Georgia_Commissioner_of_Insurance_election",
    "Commissioner of Labor": "https://en.wikipedia.org/wiki/2022_Georgia_Commissioner_of_Labor_election"
}

contests = []
for contest_name, url in CONTEST_URLS.items():
    print(f"Fetching {contest_name} from {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table")
    found = False
    for table in tables:
        try:
            df = pd.read_html(str(table))[0]
        except Exception:
            continue
        df.columns = [str(c).strip() for c in df.columns]
        # Check for candidate/results columns
        colset = set([c.lower() for c in df.columns])
        if any(x in colset for x in ["candidate", "nominee", "name", "party nominee"]):
            candidates = []
            for _, row in df.iterrows():
                candidate = str(row.get("Candidate") or row.get("Nominee") or row.get("Name") or row.get("Party nominee") or "").strip()
                party = str(row.get("Party") or row.get("Party affiliation") or row.get("Party") or "").strip()
                votes = str(row.get("Votes") or row.get("Popular vote") or row.get("Vote") or "").strip()
                pct = str(row.get("%") or row.get("Percentage") or row.get("%") or "").strip()
                if candidate:
                    candidates.append({
                        "candidate": candidate,
                        "party": party,
                        "votes": votes,
                        "pct": pct
                    })
            contests.append({
                "contest": contest_name,
                "candidates": candidates
            })
            found = True
            print(f"Extracted results for {contest_name}")
            break
    if not found:
        print(f"No results table found for {contest_name}")

with open("wikipedia_2022_ga_state_elections.json", "w", encoding="utf-8") as f:
    json.dump(contests, f, indent=2, ensure_ascii=False)

print("Extracted contests and candidates saved to wikipedia_2022_ga_state_elections.json")
