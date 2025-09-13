import json

# Paths
main_json_path = 'data/ga_county_results_trimmed.json'
senate_json_path = 'data/ga_senate_2016_by_county.json'
gov2014_json_path = 'data/ga_2014_senate_governor_by_county.json'
output_json_path = 'data/ga_county_results_trimmed.merged.json'

# Load main results
with open(main_json_path, encoding='utf-8') as f:
    main_data = json.load(f)


# Load senate 2016 results
with open(senate_json_path, encoding='utf-8') as f:
    senate_data = json.load(f)

# Load 2014 senate/governor results
with open(gov2014_json_path, encoding='utf-8') as f:
    gov2014_data = json.load(f)

main_results_by_year = main_data['results_by_year']

# Merge 2016 Senate
senate_results_2016 = senate_data['results_by_year']['2016']['us_senate_2016']
if '2016' not in main_results_by_year:
    main_results_by_year['2016'] = {}
main_results_by_year['2016']['us_senate_2016'] = senate_results_2016

# Merge 2014 Senate and Governor
senate2014 = gov2014_data['results_by_year']['2014']['us_senate_2014']
governor2014 = gov2014_data['results_by_year']['2014']['governor_2014']
if '2014' not in main_results_by_year:
    main_results_by_year['2014'] = {}
main_results_by_year['2014']['us_senate_2014'] = senate2014
main_results_by_year['2014']['governor_2014'] = governor2014

# Write merged output
with open(output_json_path, 'w', encoding='utf-8') as f:
    json.dump(main_data, f, indent=2)

print(f"Merged 2016 Senate results into {output_json_path}")
