import csv
import json
from collections import defaultdict

CSV_PATH = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data\20221108__ga__general__precinct.csv"
JSON_PATH = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data_files\results_by_year_grouped.filled.json"
OUTPUT_PATH = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data_files\results_by_year_grouped.filled_with_gwinnett.json"

COUNTY = "Gwinnett"
CONTESTS = [
    ("governor_2022", "Governor"),
    ("lieutenant_governor_2022", "Lieutenant Governor"),
    ("secretary_of_state_2022", "Secretary of State"),
    ("attorney_general_2022", "Attorney General"),
    ("commissioner_of_agriculture_2022", "Commissioner of Agriculture"),
    ("commissioner_of_insurance_2022", "Commissioner of Insurance"),
    ("commissioner_of_labor_2022", "Commissioner of Labor")
]

# Map contest JSON key to CSV office name
CONTEST_MAP = {k: v for k, v in CONTESTS}

# Helper to aggregate votes by candidate/party
def aggregate_gwinnett(csv_path, contest_office):
    results = defaultdict(lambda: defaultdict(int))
    candidates = {}
    parties = defaultdict(int)
    gwinnett_offices = set()
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        # Normalize fieldnames to strip whitespace
        reader.fieldnames = [fn.strip() for fn in reader.fieldnames]
        for row in reader:
            # Normalize keys in each row, skip None keys
            row = {k.strip(): v for k, v in row.items() if k is not None}
            if row['county'].strip().lower() == COUNTY.lower():
                gwinnett_offices.add(row['office'].strip())
            if row['county'].strip().lower() == COUNTY.lower() and row['office'].strip() == contest_office:
                cand = row['candidate'].strip()
                party = row['party'].strip()
                votes = sum(int(row[v].strip() or 0) for v in ['election_day_votes', 'advanced_votes', 'absentee_by_mail_votes', 'provisional_votes'])
                results[cand][party] += votes
                parties[party] += votes
                candidates[cand] = party
    # Debug print all unique office values for Gwinnett
    print(f"Unique office values for Gwinnett: {sorted(gwinnett_offices)}")
    return results, parties, candidates

# Helper to format JSON for one contest
def format_gwinnett_json(results, parties, candidates, contest, contest_office):
    dem_votes = sum(results[cand][party] for cand, party in candidates.items() if party == 'Democrat')
    rep_votes = sum(results[cand][party] for cand, party in candidates.items() if party == 'Republican')
    other_votes = sum(results[cand][party] for cand, party in candidates.items() if party not in ['Democrat', 'Republican'])
    total_votes = sum(parties.values())
    two_party_total = dem_votes + rep_votes
    margin = dem_votes - rep_votes
    margin_pct = None
    winner = None
    winner_name = None
    winner_party = None
    winner_votes = None
    if dem_votes > rep_votes:
        winner = "DEMOCRAT"
        winner_party = "DEMOCRAT"
        winner_name = next((cand for cand, party in candidates.items() if party == 'Democrat'), None)
        winner_votes = dem_votes
        margin_pct = f"D+{round(100 * margin / two_party_total, 2)}"
    elif rep_votes > dem_votes:
        winner = "REPUBLICAN"
        winner_party = "REPUBLICAN"
        winner_name = next((cand for cand, party in candidates.items() if party == 'Republican'), None)
        winner_votes = rep_votes
        margin_pct = f"R+{round(100 * abs(margin) / two_party_total, 2)}"
    else:
        winner = "TIE"
        winner_party = None
        winner_name = None
        winner_votes = None
        margin_pct = "TIE"
    competitiveness = {
        "category": "Tossup" if abs(margin_pct) < 5 else "Dominant",
        "party": winner_party,
        "code": f"{winner_party}_DOMINANT" if winner_party else "TOSSUP",
        "color": "#888" if abs(margin_pct) < 5 else ("#08519c" if winner_party == "DEMOCRAT" else "#a50f15")
    }
    all_parties = {party.upper(): votes for party, votes in parties.items()}
    candidates_json = {cand: {"votes": sum(results[cand].values()), "party": party, "incumbent": False} for cand, party in candidates.items()}
    return {
        "dem_candidate": next((cand for cand, party in candidates.items() if party == 'Democrat'), None),
        "rep_candidate": next((cand for cand, party in candidates.items() if party == 'Republican'), None),
        "dem_votes": dem_votes,
        "rep_votes": rep_votes,
        "other_votes": other_votes,
        "total_votes": total_votes,
        "two_party_total": two_party_total,
        "margin": margin,
        "margin_pct": margin_pct,
        "winner": winner,
        "winner_name": winner_name,
        "winner_party": winner_party,
        "winner_incumbent": False,
        "winner_votes": winner_votes,
        "competitiveness": competitiveness,
        "all_parties": all_parties,
        "candidates": candidates_json,
        "contest": contest_office,
        "county": COUNTY,
        "year": "2022"
    }

# Main script
if __name__ == "__main__":
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        results_json = json.load(f)
    for contest_key, contest_office in CONTESTS:
        results, parties, candidates = aggregate_gwinnett(CSV_PATH, contest_office)
        if not results:
            print(f"No data found for Gwinnett in {contest_office}")
            continue
        gwinnett_json = format_gwinnett_json(results, parties, candidates, contest_key, contest_office)
        # Inject into results JSON
        year_json = results_json['results_by_year'].setdefault("2022", {})
        contest_json = year_json.setdefault(contest_key, {})
        contest_json.setdefault('results', {})[COUNTY] = gwinnett_json
        print(f"Injected Gwinnett for {contest_key}")
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(results_json, f, indent=2)
    print(f"Done. Output written to {OUTPUT_PATH}")
