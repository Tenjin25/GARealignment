# --- DEBUG: Script startup ---
import sys
print("\n==== DEBUG: Script fill_targeted_missing_counties.py started ====")
sys.stdout.flush()
# fill_targeted_missing_counties.py
# Fills only the targeted missing counties for each contest/year using cleaned files
import json
import csv
from collections import defaultdict

def normalize_county(name):
    return name.strip().lower().replace('county', '').replace(' ', '')

def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def save_json(obj, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2)

def get_cleaned_file(year):
    cleaned_dir = os.path.join('data', 'cleaned')
    # Explicitly add known filenames for 2021 and 2022
    if year == "2021":
        candidates = [
            "20210105__ga__runoff.csv",
            "20210105__ga__runoff_aggregated.json"
        ]
    elif year == "2022":
        candidates = [
            "20221108__ga__general__precinct.csv",
            "20221206__ga__general_runoff__precinct.csv",
            "20221206__ga__general_runoff_aggregated.json"
        ]
    elif year == "2024":
        candidates = [
            "20241105__ga__general__precinct-level.csv",
            "20241105__ga__general__county-level.csv"
        ]
    else:
        candidates = [
            f"{year}__ga__general.csv",
            f"{year}__ga__general__precinct.csv",
            f"{year}_merged_precincts.csv",
            f"{year}__ga__general__county-level.csv",
            f"{year}__ga__general_runoff__precinct.csv",
            f"{year}__ga__general_runoff_aggregated.json",
            f"{year}__ga__runoff.csv",
            f"{year}__ga__runoff_aggregated.json"
        ]
    import os
    import sys
    print(f"\n==== DEBUG: Year {year} candidate cleaned files ====")
    sys.stdout.flush()
    abs_cleaned_dir = os.path.abspath(cleaned_dir)
    print(f"  Absolute cleaned_dir: {abs_cleaned_dir}")
    sys.stdout.flush()
    print(f"  Current working directory: {os.getcwd()}")
    sys.stdout.flush()
    try:
        all_files = os.listdir(cleaned_dir)
        print(f"  All files in cleaned_dir:")
        for fname in all_files:
            print(f"    {fname}")
        sys.stdout.flush()
    except Exception as e:
        print(f"  Error listing cleaned_dir: {e}")
        sys.stdout.flush()
        return None
    files = []
    for fname in all_files:
        if fname.startswith(year):
            fpath = os.path.join(cleaned_dir, fname)
            files.append(fpath)
            print(f"  {fpath} FOUND (filename starts with year)")
            sys.stdout.flush()
        elif fname[:4] == year:
            fpath = os.path.join(cleaned_dir, fname)
            files.append(fpath)
            print(f"  {fpath} FOUND (first 4 digits match year)")
            sys.stdout.flush()
    if files:
        # Prefer CSV, then JSON
        for f in files:
            if f.endswith('.csv'):
                print(f"  Returning CSV file: {f}")
                sys.stdout.flush()
                return f
        for f in files:
            if f.endswith('.json'):
                print(f"  Returning JSON file: {f}")
                sys.stdout.flush()
                return f
        print(f"  Returning first file: {files[0]}")
        sys.stdout.flush()
        return files[0]
    # Fallback to candidate list
    found = None
    for fname in candidates:
        fpath = os.path.join(cleaned_dir, fname)
        print(f"  {fpath} {'FOUND' if os.path.exists(fpath) else 'NOT FOUND'}")
        sys.stdout.flush()
        if os.path.exists(fpath) and not found:
            found = fpath
    return found

def fill_targeted_missing(main_json_path, output_path, missing_dict):
    main_data = load_json(main_json_path)
    results_by_year = main_data.get('results_by_year', {})
    updated = False
    for year, contests in results_by_year.items():
        cleaned_file = get_cleaned_file(year)
        if not cleaned_file:
            print(f"No cleaned file found for year {year}")
            continue
        print(f"Using cleaned file for {year}: {cleaned_file}")
        # Build lookup from cleaned file
        cleaned_lookup = defaultdict(lambda: defaultdict(dict))
        available_contests = set()
        available_counties = set()
        if cleaned_file.endswith('.json'):
            cleaned_data = load_json(cleaned_file)
            cleaned_results = cleaned_data.get('results_by_year', {}).get(year, {})
            for contest, contest_obj in cleaned_results.items():
                available_contests.add(contest)
                for county_name, county_data in contest_obj.get('results', {}).items():
                    cleaned_lookup[contest][normalize_county(county_name)] = county_data
                    available_counties.add(normalize_county(county_name))
        elif cleaned_file.endswith('.csv'):
            # Aggregate by county, office, candidate (sum across all parties and precincts)
            aggregation = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
            with open(cleaned_file, encoding='utf-8') as f:
                reader = csv.DictReader(f)
                header = reader.fieldnames
                if header:
                    print(f"  CSV header for {year}: {[h.strip() for h in header]}")
                for row in reader:
                    row = {k.strip(): (v.strip() if v is not None else v) for k, v in row.items()}
                    county = normalize_county(row.get('county') or row.get('County') or row.get('COUNTY') or "")
                    office = (row.get('office') or row.get('Office') or row.get('CONTEST') or row.get('contest') or "").strip()
                    candidate = (row.get('candidate') or row.get('Candidate') or "").strip()
                    if not county or not office or not candidate:
                        continue
                    # Sum vote columns
                    total_votes = 0
                    for vcol in ['election_day_votes', 'advanced_votes', 'absentee_by_mail_votes', 'provisional_votes']:
                        try:
                            total_votes += int(row.get(vcol, '0') or '0')
                        except ValueError:
                            pass
                    aggregation[office][county][candidate] += total_votes
                    available_contests.add(office)
                    available_counties.add(county)
            # Build cleaned_lookup: contest -> county -> {candidate: total_votes}
            for office in aggregation:
                for county in aggregation[office]:
                    cleaned_lookup[office][county] = dict(aggregation[office][county])
        print(f"  Available contests in cleaned file for {year}: {sorted(list(available_contests))}")
        print(f"  Example counties in cleaned file for {year}: {sorted(list(available_counties))[:10]} ...")
        # Fill only targeted missing counties
        for contest, contest_obj in contests.items():
            county_results = contest_obj.get('results', {})
            missing_counties = missing_dict.get(year, {}).get(contest, [])
            for county in missing_counties:
                norm_county = normalize_county(county)
                if norm_county in [normalize_county(c) for c in county_results.keys()]:
                    continue
                # Try to match contest to office name in cleaned_lookup
                contest_key = contest
                if contest_key not in cleaned_lookup:
                    # Try fuzzy match (case-insensitive, strip spaces)
                    for k in cleaned_lookup.keys():
                        if normalize_county(k) == normalize_county(contest_key):
                            contest_key = k
                            break
                if norm_county in cleaned_lookup.get(contest_key, {}):
                    candidate_votes = cleaned_lookup[contest_key][norm_county]
                    if not isinstance(candidate_votes, dict):
                        continue
                    # Build full county result structure
                    # Identify party/candidate mapping
                    party_map = {}
                    for cand, votes in candidate_votes.items():
                        # Try to infer party from candidate name (if possible)
                        party = None
                        if 'biden' in cand.lower() or 'gore' in cand.lower() or 'clinton' in cand.lower() or 'obama' in cand.lower():
                            party = 'DEMOCRAT'
                        elif 'trump' in cand.lower() or 'bush' in cand.lower() or 'mccain' in cand.lower() or 'romney' in cand.lower() or 'dole' in cand.lower() or 'kemp' in cand.lower():
                            party = 'REPUBLICAN'
                        elif 'libertarian' in cand.lower() or 'brown' in cand.lower():
                            party = 'LIBERTARIAN'
                        elif 'independent' in cand.lower() or 'buchanan' in cand.lower():
                            party = 'INDEPENDENT'
                        party_map[cand] = party
                    # Assign dem/rep/other candidates
                    dem_candidate = next((c for c, p in party_map.items() if p == 'DEMOCRAT'), None)
                    rep_candidate = next((c for c, p in party_map.items() if p == 'REPUBLICAN'), None)
                    dem_votes = candidate_votes.get(dem_candidate, 0) if dem_candidate else 0
                    rep_votes = candidate_votes.get(rep_candidate, 0) if rep_candidate else 0
                    other_votes = sum(v for c, v in candidate_votes.items() if party_map.get(c) not in ['DEMOCRAT', 'REPUBLICAN'])
                    total_votes = sum(candidate_votes.values())
                    two_party_total = dem_votes + rep_votes
                    margin = rep_votes - dem_votes
                    margin_pct = None
                    if two_party_total > 0:
                        margin_pct_val = 100.0 * abs(margin) / two_party_total
                        margin_pct = f"{'R' if margin > 0 else 'D'}+{margin_pct_val:.2f}"
                    winner = None
                    winner_name = None
                    winner_party = None
                    winner_votes = None
                    if candidate_votes:
                        winner_name = max(candidate_votes, key=lambda k: candidate_votes[k])
                        winner_votes = candidate_votes[winner_name]
                        winner_party = party_map.get(winner_name, None)
                        winner = winner_party if winner_party else 'OTHER'
                    # Simple competitiveness
                    competitiveness = {
                        "category": "Dominant" if abs(margin) > 1000 else "Safe" if abs(margin) > 500 else "Competitive",
                        "party": winner_party if winner_party else "OTHER",
                        "code": f"{winner_party}_DOMINANT" if abs(margin) > 1000 else f"{winner_party}_SAFE" if abs(margin) > 500 else f"{winner_party}_COMPETITIVE",
                        "color": "#a50f15" if winner_party == "REPUBLICAN" else "#08519c" if winner_party == "DEMOCRAT" else "#cccccc"
                    }
                    # all_parties
                    all_parties = {}
                    for cand, votes in candidate_votes.items():
                        party = party_map.get(cand, "OTHER")
                        all_parties[party] = all_parties.get(party, 0) + votes
                    # candidates
                    candidates = {}
                    for cand, votes in candidate_votes.items():
                        candidates[cand] = {
                            "votes": votes,
                            "party": party_map.get(cand, "OTHER"),
                            "incumbent": False
                        }
                    # Build result dict
                    county_result = {
                        "dem_candidate": dem_candidate,
                        "rep_candidate": rep_candidate,
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
                        "candidates": candidates,
                        "contest": contest,
                        "county": county,
                        "year": year
                    }
                    print(f"Filling targeted missing county {county} in {contest} {year} with full structure")
                    county_results[county] = county_result
                    updated = True
            contest_obj['results'] = county_results
    if updated:
        save_json(main_data, output_path)
        print(f"Updated results written to {output_path}")
    else:
        print("No targeted missing counties filled.")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 4:
        print("Usage: python fill_targeted_missing_counties.py main_results.json output.json missing_dict.json")
        sys.exit(1)
    with open(sys.argv[3], 'r', encoding='utf-8') as f:
        missing_dict = json.load(f)
    fill_targeted_missing(sys.argv[1], sys.argv[2], missing_dict)
