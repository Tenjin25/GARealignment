import json

# File paths
main_path = 'data/ga_county_results_trimmed.merged_final.cleaned.json'
senate2016_path = 'data/ga_senate_2016_by_county.categorized.json'
out_path = 'data/ga_county_results_trimmed.merged_final.with2016.json'

with open(main_path, encoding='utf-8') as f:
    main_data = json.load(f)
with open(senate2016_path, encoding='utf-8') as f:
    senate2016_data = json.load(f)

# Merge 2016 US Senate results into main_data
main_results = main_data['results_by_year']
senate_results = senate2016_data['results_by_year']['2016']['us_senate_2016']['results']

if '2016' not in main_results:
    main_results['2016'] = {}
main_results['2016']['us_senate_2016'] = {
    'contest_name': 'US Senate (2016)',
    'results': senate_results
}

with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(main_data, f, indent=2)

print(f"Merged 2016 US Senate results into {out_path}")
