import json

# Load the current data
with open('data/results_by_year_grouped.final.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Get all Georgia counties from a contest with complete data
complete_contest = data['results_by_year']['2022']['governor_2022']
all_counties = set(complete_contest['results'].keys())
print(f"Total Georgia counties: {len(all_counties)}")

# Check which counties are missing from the new contests
for contest_key in ['commissioner_of_agriculture_2022', 'commissioner_of_insurance_2022', 'commissioner_of_labor_2022']:
    present_counties = set(data['results_by_year']['2022'][contest_key]['results'].keys())
    missing = sorted(all_counties - present_counties)
    
    print(f"\n{contest_key}:")
    print(f"  Present: {len(present_counties)}")
    print(f"  Missing: {len(missing)}")
    print(f"\nMissing counties:")
    for i, county in enumerate(missing, 1):
        print(f"  {i:2d}. {county}")
