# fill_missing_counties_from_cleaned_safe.py
# Improved: Handles missing/invalid arguments and prints clear error messages
import json
import os
import csv
from collections import defaultdict
import sys

def normalize_county(name):
    return name.strip().upper().replace(" COUNTY", "")

def load_json(path):
    if not os.path.exists(path):
        print(f"ERROR: File not found: {path}")
        return None
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def save_json(obj, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2)

def get_cleaned_file(year):
    cleaned_dir = os.path.join('data', 'cleaned')
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
    for fname in candidates:
        fpath = os.path.join(cleaned_dir, fname)
        if os.path.exists(fpath):
            return fpath
    return None

def fill_missing_counties(main_json_path, output_path):
    main_data = load_json(main_json_path)
    if main_data is None:
        print("Aborting: main results file not found or invalid.")
        return
    results_by_year = main_data.get('results_by_year', {})
    updated = False
    for year, contests in results_by_year.items():
        cleaned_file = get_cleaned_file(year)
        if not cleaned_file:
            print(f"No cleaned file found for year {year}")
            continue
        print(f"Using cleaned file for {year}: {cleaned_file}")
        if cleaned_file.endswith('.json'):
            cleaned_data = load_json(cleaned_file)
            if cleaned_data is None:
                print(f"Skipping {cleaned_file}: file not found or invalid.")
                continue
            cleaned_results = cleaned_data.get('results_by_year', {}).get(year, {})
            for contest, contest_obj in contests.items():
                county_results = contest_obj.get('results', {})
                cleaned_contest_obj = cleaned_results.get(contest, {})
                cleaned_counties = cleaned_contest_obj.get('results', {}) if cleaned_contest_obj else {}
                for county_name, county_data in cleaned_counties.items():
                    norm_county = normalize_county(county_name)
                    if norm_county not in [normalize_county(c) for c in county_results.keys()]:
                        print(f"Filling missing county {county_name} in {contest} {year}")
                        county_results[county_name] = county_data
                        updated = True
                contest_obj['results'] = county_results
        elif cleaned_file.endswith('.csv'):
            try:
                with open(cleaned_file, encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    csv_lookup = defaultdict(lambda: defaultdict(dict))
                    for row in reader:
                        county = normalize_county(row.get('county') or row.get('County') or row.get('COUNTY') or "")
                        contest = row.get('contest') or row.get('Contest') or row.get('CONTEST') or ""
                        if not county or not contest:
                            continue
                        csv_lookup[contest][county] = row
                    for contest, contest_obj in contests.items():
                        county_results = contest_obj.get('results', {})
                        for county_name in csv_lookup.get(contest, {}):
                            norm_county = normalize_county(county_name)
                            if norm_county not in [normalize_county(c) for c in county_results.keys()]:
                                row = csv_lookup[contest][county_name]
                                county_data = {
                                    'contest': contest,
                                    'year': year,
                                    'dem_candidate': row.get('dem_candidate') or row.get('Democratic Candidate') or "",
                                    'rep_candidate': row.get('rep_candidate') or row.get('Republican Candidate') or "",
                                    'dem_votes': int(row.get('dem_votes') or row.get('Democratic Votes') or 0),
                                    'rep_votes': int(row.get('rep_votes') or row.get('Republican Votes') or 0),
                                    'other_votes': int(row.get('other_votes') or row.get('Other Votes') or 0),
                                    'total_votes': int(row.get('total_votes') or row.get('Total Votes') or 0),
                                    'margin': int(row.get('margin') or 0),
                                    'margin_pct': float(row.get('margin_pct') or 0.0),
                                    'winner': row.get('winner') or "",
                                    'competitiveness': {},
                                    'all_parties': {},
                                }
                                print(f"Filling missing county {county_name} in {contest} {year} from CSV")
                                county_results[county_name] = county_data
                                updated = True
                        contest_obj['results'] = county_results
            except Exception as e:
                print(f"Error reading CSV {cleaned_file}: {e}")
                continue
    if updated:
        save_json(main_data, output_path)
        print(f"Updated results written to {output_path}")
    else:
        print("No missing counties filled.")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python fill_missing_counties_from_cleaned_safe.py main_results.json output.json")
        print("Example: python fill_missing_counties_from_cleaned_safe.py data/results_by_year_grouped.json data/results_by_year_grouped.filled.json")
        sys.exit(1)
    fill_missing_counties(sys.argv[1], sys.argv[2])
