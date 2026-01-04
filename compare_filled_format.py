import json

FILLED_PATH = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data_files\results_by_year_grouped.filled.json"
ORIGINAL_PATH = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data_files\results_by_year_grouped.json"

def compare_structure():
    with open(FILLED_PATH, 'r', encoding='utf-8') as f:
        filled = json.load(f)
    with open(ORIGINAL_PATH, 'r', encoding='utf-8') as f:
        original = json.load(f)
    # Compare top-level keys
    print("Top-level keys in filled:", list(filled.keys()))
    print("Top-level keys in original:", list(original.keys()))
    # Compare structure for one year/contest
    year = "2022"
    contest = "governor_2022"
    filled_contest = filled.get('results_by_year', {}).get(year, {}).get(contest, {})
    original_contest = original.get('results_by_year', {}).get(year, {}).get(contest, {})
    print(f"\nFilled contest keys for {year} {contest}: {list(filled_contest.keys())}")
    print(f"Original contest keys for {year} {contest}: {list(original_contest.keys())}")
    # Check if 'results' key exists and is a dict
    if 'results' in filled_contest and isinstance(filled_contest['results'], dict):
        print(f"Filled 'results' counties: {list(filled_contest['results'].keys())[:5]} ...")
    if 'results' in original_contest and isinstance(original_contest['results'], dict):
        print(f"Original 'results' counties: {list(original_contest['results'].keys())[:5]} ...")
    # Compare a sample county's data structure
    sample_county = next(iter(filled_contest.get('results', {})), None)
    if sample_county:
        print(f"Filled sample county ({sample_county}) data type: {type(filled_contest['results'][sample_county])}")
        print(f"Original sample county ({sample_county}) data type: {type(original_contest['results'].get(sample_county))}")

if __name__ == "__main__":
    compare_structure()
