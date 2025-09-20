import json

# Filenames
prev_file = 'data/ga_county_results_trimmed.merged.json'  # Change if your previous file has a different name
new_file = 'data/ga_county_results_trimmed.updated.json'
out_file = 'data/ga_county_results_trimmed.merged_final.json'

# Load both files
def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(obj, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

prev_data = load_json(prev_file)
new_data = load_json(new_file)

# Merge results_by_year, preferring new_data on conflict
merged = prev_data.copy()
if 'results_by_year' not in merged:
    merged['results_by_year'] = {}
for year, contests in new_data.get('results_by_year', {}).items():
    if year not in merged['results_by_year']:
        merged['results_by_year'][year] = contests
    else:
        # Merge contests for this year
        for contest, contest_data in contests.items():
            merged['results_by_year'][year][contest] = contest_data  # Always prefer new_data

save_json(merged, out_file)
print(f"Merged file written to {out_file}")
