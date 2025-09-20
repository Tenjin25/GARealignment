import json

# Paths
main_json_path = 'data/ga_county_results_trimmed.json'  # Main file to update
input_json_path = 'data/ga_2014_2018_by_county.json'    # File with 2014 and 2018 contests
output_json_path = 'data/ga_county_results_trimmed.merged_2014_2018.json'

def fix_lean_category(results):
    for county, data in results.items():
        # Treat 'IR' as 'R' in all_parties and candidate/party fields
        all_parties = data.get('all_parties', {})
        if 'IR' in all_parties:
            all_parties['REP'] = all_parties.get('REP', 0) + all_parties['IR']
            del all_parties['IR']
        # If party fields exist, replace 'IR' with 'R'
        if 'party' in data and data['party'] == 'IR':
            data['party'] = 'R'
        if 'rep_party' in data and data['rep_party'] == 'IR':
            data['rep_party'] = 'R'
        if 'rep_candidate' in data and 'IR' in data.get('rep_candidate',''):
            data['rep_candidate'] = data['rep_candidate'].replace('IR', 'R')
        # Fix Lean category and handle Tossup
        cat = data.get('category', '')
        dem = data.get('dem_votes', 0)
        rep = data.get('rep_votes', 0)
        if cat.strip() == 'Lean':
            if dem > rep:
                data['category'] = 'Lean Democratic'
            elif rep > dem:
                data['category'] = 'Lean Republican'
            else:
                data['category'] = 'Tossup'
        elif cat.strip() == 'Tossup':
            if dem > rep:
                data['category'] = 'Tossup (Democratic Win)'
            elif rep > dem:
                data['category'] = 'Tossup (Republican Win)'
            else:
                data['category'] = 'Tossup'

# Load main results
with open(main_json_path, encoding='utf-8') as f:
    main_data = json.load(f)

# Load 2014/2018 results
with open(input_json_path, encoding='utf-8') as f:
    input_data = json.load(f)

main_results_by_year = main_data['results_by_year']
input_results_by_year = input_data['results_by_year']

# Merge 2014 and 2018 contests
for year in ['2014', '2018']:
    if year in input_results_by_year:
        for contest, contest_obj in input_results_by_year[year].items():
            fix_lean_category(contest_obj['results'])
            if year not in main_results_by_year:
                main_results_by_year[year] = {}
            main_results_by_year[year][contest] = contest_obj

# Write merged output
with open(output_json_path, 'w', encoding='utf-8') as f:
    json.dump(main_data, f, indent=2)

print(f"Merged 2014 and 2018 contests into {output_json_path}")
