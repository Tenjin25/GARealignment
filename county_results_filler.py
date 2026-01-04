# county_results_filler.py
# Fills missing counties in results_by_year_grouped.json using county-level aggregates from cleaned CSVs
import json
import os

def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def save_json(obj, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2)

def get_county_aggregate_file(year, contest):
    # Look for files in data/county_aggregated_ncstyle matching year and contest
    agg_dir = os.path.join('data', 'county_aggregated_ncstyle')
    if not os.path.exists(agg_dir):
        return None
    files = [f for f in os.listdir(agg_dir) if f.endswith('_county.json') and year in f]
    for f in files:
        fpath = os.path.join(agg_dir, f)
        # Optionally, match contest name in file (if present)
        if contest.lower().replace(' ', '_') in f.lower():
            return fpath
    # Fallback: return first file for year
    return os.path.join(agg_dir, files[0]) if files else None

def fill_missing_counties(main_json_path, output_path, missing_dict_path):
    main_data = load_json(main_json_path)
    missing_dict = load_json(missing_dict_path)
    results_by_year = main_data.get('results_by_year', {})
    updated = False
    for year, contests in results_by_year.items():
        for contest, contest_obj in contests.items():
            county_results = contest_obj.get('results', {})
            missing_counties = missing_dict.get(year, {}).get(contest, [])
            if not missing_counties:
                continue
            agg_file = get_county_aggregate_file(year, contest)
            if not agg_file or not os.path.exists(agg_file):
                print(f"No aggregate file found for {year} {contest}")
                continue
            print(f"Using aggregate file for {year} {contest}: {agg_file}")
            agg_data = load_json(agg_file)
            for county in missing_counties:
                if county in county_results:
                    continue
                # Try to match county name (case-insensitive)
                match = next((c for c in agg_data.keys() if c.lower().replace(' county','') == county.lower().replace(' county','')), None)
                if match:
                    print(f"Filling missing county {county} in {contest} {year}")
                    county_results[county] = agg_data[match]
                    updated = True
            contest_obj['results'] = county_results
    if updated:
        save_json(main_data, output_path)
        print(f"Updated results written to {output_path}")
    else:
        print("No missing counties filled.")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 4:
        print("Usage: python county_results_filler.py main_results.json output.json missing_dict.json")
        sys.exit(1)
    fill_missing_counties(sys.argv[1], sys.argv[2], sys.argv[3])
