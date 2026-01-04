import json

ORIGINAL_PATH = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data_files\ga_county_results_trimmed.updated.json"

# Example: Print keys for 2022 governor_2022
YEAR = "2022"
CONTEST = "governor_2022"

def print_contest_keys():
    with open(ORIGINAL_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    contests = data.get('results_by_year', {}).get(YEAR, {})
    contest_data = contests.get(CONTEST, {})
    print(f"Structure for {YEAR} {CONTEST} in original file:")
    if isinstance(contest_data, dict):
        print(f"Top-level keys: {list(contest_data.keys())}")
        # Print first 3 key-value pairs for inspection
        for i, (k, v) in enumerate(contest_data.items()):
            print(f"  Key: {k}")
            if isinstance(v, dict):
                print(f"    Value type: dict, keys: {list(v.keys())[:5]}")
            elif isinstance(v, list):
                print(f"    Value type: list, length: {len(v)}")
            else:
                print(f"    Value type: {type(v).__name__}, value: {str(v)[:100]}")
            if i >= 2:
                break
    else:
        print(f"Contest data is type {type(contest_data).__name__}")

if __name__ == "__main__":
    print_contest_keys()
