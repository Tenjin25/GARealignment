import json

FILLED_PATH = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data_files\results_by_year_grouped.filled.json"
ORIGINAL_PATH = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data_files\results_by_year_grouped.json"

def compare_all_years():
    with open(FILLED_PATH, 'r', encoding='utf-8') as f:
        filled = json.load(f)
    with open(ORIGINAL_PATH, 'r', encoding='utf-8') as f:
        original = json.load(f)
    filled_years = set(filled.get('results_by_year', {}).keys())
    original_years = set(original.get('results_by_year', {}).keys())
    print("Years in filled:", sorted(filled_years))
    print("Years in original:", sorted(original_years))
    for year in sorted(filled_years | original_years):
        filled_contests = set(filled.get('results_by_year', {}).get(year, {}).keys())
        original_contests = set(original.get('results_by_year', {}).get(year, {}).keys())
        print(f"\nYear: {year}")
        print("  Contests in filled:", sorted(filled_contests))
        print("  Contests in original:", sorted(original_contests))
        for contest in sorted(filled_contests | original_contests):
            filled_contest = filled.get('results_by_year', {}).get(year, {}).get(contest, {})
            original_contest = original.get('results_by_year', {}).get(year, {}).get(contest, {})
            filled_keys = set(filled_contest.keys())
            original_keys = set(original_contest.keys())
            if filled_keys != original_keys:
                print(f"    Contest: {contest} - Key mismatch!")
                print(f"      Filled keys: {sorted(filled_keys)}")
                print(f"      Original keys: {sorted(original_keys)}")
            # Optionally, check if 'results' counties match
            if 'results' in filled_contest and 'results' in original_contest:
                filled_counties = set(filled_contest['results'].keys())
                original_counties = set(original_contest['results'].keys())
                if filled_counties != original_counties:
                    print(f"    Contest: {contest} - County mismatch!")
                    print(f"      Counties in filled but not original: {sorted(filled_counties - original_counties)}")
                    print(f"      Counties in original but not filled: {sorted(original_counties - filled_counties)}")

if __name__ == "__main__":
    compare_all_years()
