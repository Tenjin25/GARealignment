import json

# Paths to your files
main_json_path = 'data/cleaned/ga_county_results.json'
runoff_json_path = 'data/cleaned/20210105__ga__runoff_aggregated.json'

# Load main results
with open(main_json_path, 'r', encoding='utf-8') as f:
    main_data = json.load(f)

# Load runoff results
with open(runoff_json_path, 'r', encoding='utf-8') as f:
    runoff_data = json.load(f)

# Ensure 'results_by_year' and '2021' exist
if 'results_by_year' not in main_data:
    main_data['results_by_year'] = {}
if '2021' not in main_data['results_by_year']:
    main_data['results_by_year']['2021'] = {}

# Add/replace the runoff contests
main_data['results_by_year']['2021']['us_senate_2021_warnock'] = runoff_data['us_senate_2021_warnock']
main_data['results_by_year']['2021']['us_senate_2021_ossoff'] = runoff_data['us_senate_2021_ossoff']

# Write back to the main file (backup first if you want)
with open(main_json_path, 'w', encoding='utf-8') as f:
    json.dump(main_data, f, indent=2)

print('2021 Senate runoff results merged into main JSON.')
